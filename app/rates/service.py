from typing import Optional, Tuple, List, Iterable, Callable

from pydantic.types import date
from rapidfuzz import process, fuzz
from sqlalchemy import text

from app.db.init_db import Session
from app.rates.utils import PortColumn


def fuzzy_search_port(
        string_search: str, list_of_ports: list[dict], number_of_best_candidates: int
) -> list[dict]:
    """
    Find the port that is most similar to the string_search by comparing code, name, parent slug using
    fuzzy matching using the library rapidfuzz.

        Parameters:
                    string_search (str): The word you want to match with the ports
                    list_of_ports (list[dict]): A list of port ports represented as a dictionary
                    number_of_best_candidates (int): Limit the number of results

        Returns:
                best_results (list[List[dict]]): The n number

    """

    # The fuzzy search is applied for each of the dictionary of the list, and it will return a list of
    # tuple for each key word of the dictionary. The tuples have the following structure
    # (value of the key, score from 0 to 100, key of the value)
    # the similarity fuzzy search is done by each value of the dictionary
    list_of_scores = (
        process.extract(string_search, dict(row), scorer=fuzz.WRatio) for row in list_of_ports
    )

    # Then sort the tokens based on each of the value have the most score
    # by taking the highest score of the list of tuples as the sort argument
    sorted_scores = sorted(
        list_of_scores,
        key=lambda list_of_tuples: max(element[1] for element in list_of_tuples),
        reverse=True,
    )

    return sorted_scores[:number_of_best_candidates]


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


def generate_port_filter(column_type: PortColumn, column_name: str, value: str) -> str:
    if column_type == PortColumn.NAME:
        return f"and {column_name}.name = '{value}'"
    if column_type == PortColumn.CODE:
        return f"and {column_name}.code = '{value}'"

    return ""


def formatter(sequence: Iterable, element_modifier: Callable) -> Iterable:
    return (element_modifier(element) for element in sequence)


def generate_rates_query(
        origin: Tuple[str, PortColumn] | None,
        destination: Tuple[str, PortColumn] | None,
        range_date: Tuple[date | None, date | None],
) -> str:
    origin_value, origin_column = origin
    destination_value, destination_column = destination

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
            select day, avg(price) from regions_contained_origin
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
                select day, avg(price)
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
    elif (
            origin_column in (PortColumn.CODE, PortColumn.NAME, PortColumn.NONE)
            and destination_column == PortColumn.PARENT_SLUG
    ):

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
                select day, avg(price) from ports
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
                   select day, avg(price) from ports
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


from typing import Tuple


def get_rates(
        date_from: Optional[date] | None,
        date_to: Optional[date] | None,
        origin: Tuple[str, PortColumn] | None,
        destination: Tuple[str, PortColumn] | None,
):
    query = generate_rates_query(origin, destination, (date_from, date_to))
    with Session() as session:
        results = session.execute(query).fetchall()

    return results
