from typing import Optional, Tuple, List

from pydantic.types import date
from sqlalchemy import text

from app.database import Session
from app.ports.utils import generate_port_filter
from app.rates.utils import PortColumn, AggregateFunctions

def generate_date_filter(
        column_parameter: str,
        date_from: Optional[date] | None,
        date_to: Optional[date] | None,
) -> str:
    if date_from and date_to:
        return f"and {column_parameter} BETWEEN '{date_from}' AND '{date_to}'"
    if date_from:
        return f"and '{date_from}' <= {column_parameter}"
    if date_to:
        return f"and {column_parameter} <= '{date_to}'"

    return ""


def generate_aggregate_funct(
        aggregate_functions: Optional[List[AggregateFunctions]] | None = None,
        column_name: str = "price",
) -> str:
    result = []
    naming = {
        "AVG": f"ROUND(AVG({column_name}),2)  as average_{column_name}",
        "SUM": f"SUM({column_name})  as total_{column_name}",
        "MAX": f"MAX({column_name})  as largest_{column_name}",
        "MIN": f"MIN({column_name})  as lowest_{column_name}",
        "COUNT": f"COUNT({column_name})  as number_of_{column_name}",
        "STD": f"ROUND(STDDEV({column_name}), 2)  as standard_deviation_{column_name}",
    }
    for agg_func in aggregate_functions:

        if agg_func == AggregateFunctions.COUNT:
            result.append(f"{agg_func.value}(*)")
        else:
            result.append(f"{agg_func.value}({column_name})")

    return ",".join(naming[agg_func.name] for agg_func in aggregate_functions)




def generate_rates_query(
        origin: Tuple[str, PortColumn] | None,
        destination: Tuple[str, PortColumn] | None,
        range_date: Tuple[date | None, date | None],
        aggregate_functions: Optional[List[AggregateFunctions]] | None = None,
) -> str:
    origin_value, origin_column = origin
    destination_value, destination_column = destination

    agg_query_str = generate_aggregate_funct(aggregate_functions, "price")

    filter_by_date = generate_date_filter("day", *range_date)
    # query for all prices rates from one region to another region
    if (origin_column, destination_column) == (
            PortColumn.PARENT_SLUG,
            PortColumn.PARENT_SLUG,
    ):
        query = text(
            f"""
            WITH RECURSIVE regions_contained_origin AS (
                select * from regions where slug in ('{origin_value}')
                union all
                    select
                        regions.slug,
                        regions.name,
                        regions.parent_slug
                    from
                        regions
                    inner join regions_contained_origin on
                        regions_contained_origin.slug = regions.parent_slug
            ),
                regions_contained_destiny AS (
                select * from regions where slug in ('{destination_value}')
                union all
                    select
                        regions.slug,
                        regions.name,
                        regions.parent_slug
                    from
                        regions
                    inner join regions_contained_destiny on
                        regions_contained_destiny.slug = regions.parent_slug
            )
            select day, {agg_query_str} from regions_contained_origin
                inner join ports on
                    ports.parent_slug = regions_contained_origin.slug
                inner join prices p1 on
                    ports.code = p1.orig_code
                    -- filter price by dates
                   {filter_by_date}
                inner join ports p2 on
                    p2.code = p1.dest_code and
                    p2.parent_slug in (select slug from regions_contained_destiny)
                group by day
                order by day
        """
        )
    # query for all prices rates from one region to specific port name or code
    elif origin_column == PortColumn.PARENT_SLUG and destination_column in (
            PortColumn.CODE,
            PortColumn.NAME,
            PortColumn.NONE,
    ):

        filter_by_destiny = generate_port_filter(
            destination_column, "p2", destination_value
        )

        query = text(
            f"""
                WITH RECURSIVE regions_contained_origin AS (
                    select * from regions where slug in ('china_main')
                    union all
                        select
                            regions.slug,
                            regions.name,
                            regions.parent_slug
                        from
                            regions
                        inner join regions_contained_origin on
                            regions_contained_origin.slug = regions.parent_slug
                )
                select day, {agg_query_str}
                         from regions_contained_origin
                    inner join ports on
                        ports.parent_slug = regions_contained_origin.slug
                    inner join prices p1 on
                        ports.code = p1.orig_code
                        -- filter price by dates
                       {filter_by_date}
                    inner join ports p2 on
                        p2.code = p1.dest_code
                    -- filtering prices by code, name
                        {filter_by_destiny}
                    group by day
                    order by day
                """
        )
    # query for all prices rates from a port name or code to a specific region
    elif origin_column in (PortColumn.CODE, PortColumn.NAME, PortColumn.NONE) and \
            destination_column == PortColumn.PARENT_SLUG:

        filter_by_origin = generate_port_filter(origin_column, "ports", origin_value)
        query = text(
            f"""
                WITH RECURSIVE regions_contained_destiny AS (
                    select * from regions where slug in ('{destination_value}')
                    union
                        select
                            regions.slug,
                            regions.name,
                            regions.parent_slug
                        from
                            regions
                        inner join regions_contained_destiny on
                            regions_contained_destiny.slug = regions.parent_slug
                )
                select day, {agg_query_str} from ports
                    inner join prices p1 on
                        ports.code = p1.orig_code
                    -- filtering origin of prices by code, name
                        {filter_by_origin}
                    -- Filtering by a date
                       {filter_by_date}
                    inner join ports prt on
                    prt.code = p1.dest_code and
                    prt.parent_slug in (select slug from regions_contained_destiny)
                group by day
                order by day
        """
        )
    # query for all prices rates from a port name or code to another port name or code
    else:
        filter_by_origin = generate_port_filter(origin_column, "ports", origin_value)
        filter_by_destiny = generate_port_filter(
            destination_column, "p2", destination_value
        )
        query = text(
            f"""
                   select day, {agg_query_str} from ports
                        inner join prices p on
                            ports.code = p.orig_code
                        -- by origin
                        {filter_by_origin}
                        -- by date
                        {filter_by_date}
                        inner join ports p2 on
                            p2.code = p.dest_code
                        {filter_by_destiny}
                    group by day
                    order by day
                """
        )

    return query


def get_rates(
        date_from: Optional[date] | None,
        date_to: Optional[date] | None,
        origin: Tuple[str, PortColumn] | None,
        destination: Tuple[str, PortColumn] | None,
        aggregate_functions: Optional[List[AggregateFunctions]] | None = [AggregateFunctions.AVG]
):
    query = generate_rates_query(
        origin, destination, (date_from, date_to), aggregate_functions
    )
    with Session() as session:
        results = session.execute(query).fetchall()

    return [dict(row) for row in results]
