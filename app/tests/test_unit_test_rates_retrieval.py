from typing import List

from sqlalchemy import text
from sqlalchemy.engine.row import Row
from fastapi.testclient import TestClient

from app.main import app
from app.database import Session
from app.rates.service import get_rates
from app.rates.utils import PortColumn
from datetime import date

client = TestClient(app)


def test_date_from_region_to_region():
    """
    Compare results of rates from one region to another of the function get_rates

    """

    function_result: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("china_main", PortColumn.PARENT_SLUG),
        ("baltic", PortColumn.PARENT_SLUG),
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
        ),
            regions_contained_destiny AS (
            select * from regions where slug in ('baltic')
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
        select day, round(avg(price), 2) as average_price from regions_contained_origin
            inner join ports on
                ports.parent_slug = regions_contained_origin.slug
            inner join prices p1 on
                ports.code = p1.orig_code
                -- filter price by dates
               and p1.day BETWEEN '2016-01-27' and '2016-01-30'
            inner join ports p2 on
                p2.code = p1.dest_code and 
                p2.parent_slug in (select slug from regions_contained_destiny)
            group by day
            order by day
            """
    )

    with Session() as session:
        query_result = [dict(row) for row in session.execute(query).fetchall()]

    assert len(function_result) == len(
        query_result
    ), "The results have different lengths"

    for func_resu, query_resu in zip(function_result, query_result):
        assert (
            func_resu == query_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "


def test_rates_from_region_to_port_with_name():
    """
    Compare results of rates from one region to a specific port by using the name of the port

    """
    function_result_by_name: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("china_main", PortColumn.PARENT_SLUG),
        ("Tallinn", PortColumn.NAME),
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
                    select day, round(avg(price), 2) as average_price
                             from regions_contained_origin
                        inner join ports on
                            ports.parent_slug = regions_contained_origin.slug
                        inner join prices p1 on
                            ports.code = p1.orig_code
                            -- filter price by dates
                           and p1.day BETWEEN '2016-01-27' and '2016-01-30'
                        inner join ports p2 on
                            p2.code = p1.dest_code
                        -- filtering prices by code, name 
                            and p2.name = 'Tallinn' 
                        group by day
                        order by day
                    """
    )

    with Session() as session:
        query_result_by_name = [dict(row) for row in session.execute(query).fetchall()]

    assert len(query_result_by_name) == len(function_result_by_name)

    for query_resu, func_resu in zip(query_result_by_name, function_result_by_name):
        assert (
            query_resu == func_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "


def test_rates_from_region_to_port_with_code():
    """
    Compare results of rates from one region to a specific port by using the code or name of the port

    """
    function_result_by_code: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("china_main", PortColumn.PARENT_SLUG),
        ("EETLL", PortColumn.CODE),
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
                select day, round(avg(price), 2) as average_price
                         from regions_contained_origin
                    inner join ports on
                        ports.parent_slug = regions_contained_origin.slug
                    inner join prices p1 on
                        ports.code = p1.orig_code
                        -- filter price by dates
                       and p1.day BETWEEN '2016-01-27' and '2016-01-30'
                    inner join ports p2 on
                        p2.code = p1.dest_code
                    -- filtering prices by code, name 
                        and p2.code = 'EETLL' 
                    group by day
                    order by day
                """
    )

    query_by_name = text(
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
                    select day, round(avg(price), 2) as average_price
                             from regions_contained_origin
                        inner join ports on
                            ports.parent_slug = regions_contained_origin.slug
                        inner join prices p1 on
                            ports.code = p1.orig_code
                            -- filter price by dates
                           and p1.day BETWEEN '2016-01-27' and '2016-01-30'
                        inner join ports p2 on
                            p2.code = p1.dest_code
                        -- filtering prices by code, name 
                            and p2.name = 'Tallinn' 
                        group by day
                        order by day
                    """
    )

    with Session() as session:
        query_result_by_code = [dict(row) for row in session.execute(query).fetchall()]

    assert len(query_result_by_code) == len(function_result_by_code)

    for query_resu, func_resu in zip(query_result_by_code, function_result_by_code):
        assert (
            query_resu == func_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "


def test_rates_from_port_to_region_using_name():
    """
    Compare results of rates from one region to a specific port by using the code or name of the port

    """

    function_result_by_name: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("Shanghai", PortColumn.NAME),
        ("finland_main", PortColumn.PARENT_SLUG),
    )

    query = text(
        f"""
                    WITH RECURSIVE regions_contained_destiny AS (
                        select * from regions where slug in ('finland_main')
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
                    select day, round(avg(price), 2) as average_price from ports
                        inner join prices p1 on
                            ports.code = p1.orig_code
                        -- filtering origin of prices by code, name 
                            and ports.name = 'Shanghai' 

                        -- Filtering by a date
                           and p1.day BETWEEN '2016-01-27' and '2016-01-30'
                        inner join ports prt on
                        prt.code = p1.dest_code and
                        prt.parent_slug in (select slug from regions_contained_destiny)
                    group by day
                    order by day
            """
    )

    with Session() as session:
        query_result_by_name = [dict(row) for row in session.execute(query).fetchall()]

    assert len(query_result_by_name) == len(function_result_by_name)

    for query_resu, func_resu in zip(
        query_result_by_name,
        function_result_by_name,
    ):
        assert (
            query_resu == func_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "


def test_rates_from_port_to_region_using_code():
    """
    Compare results of rates from one region to a specific port by using the code or name of the port

    """

    function_result_by_code: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("CNSGH", PortColumn.CODE),
        ("finland_main", PortColumn.PARENT_SLUG),
    )

    query = text(
        f"""
                    WITH RECURSIVE regions_contained_destiny AS (
                        select * from regions where slug in ('finland_main')
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
                    select day, round(avg(price), 2) as average_price from ports
                        inner join prices p1 on
                            ports.code = p1.orig_code
                        -- filtering origin of prices by code, name 
                            and ports.code = 'CNSGH' 

                        -- Filtering by a date
                           and p1.day BETWEEN '2016-01-27' and '2016-01-30'
                        inner join ports prt on
                        prt.code = p1.dest_code and
                        prt.parent_slug in (select slug from regions_contained_destiny)
                    group by day
                    order by day
            """
    )

    with Session() as session:
        query_result_by_code = [dict(row) for row in session.execute(query).fetchall()]

    assert len(query_result_by_code) == len(function_result_by_code)

    for query_resu, func_resu in zip(query_result_by_code, function_result_by_code):
        assert (
            query_resu == func_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "


def test_rates_from_port_to_port_using_code():
    """
    Compare results of rates from one region to a specific port by using the code or name of the port

    """

    function_result_by_code: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("CNSGH", PortColumn.CODE),
        ("RULUG", PortColumn.CODE),
    )

    query = text(
        f"""
                    select day, round(avg(price), 2) as average_price from ports
                        inner join prices p on
                            ports.code = p.orig_code
                        -- by origin
                        and ports.code = 'CNSGH'
                        -- by date
                       and p.day BETWEEN '2016-01-27' and '2016-01-30'
                        inner join ports p2 on
                            p2.code = p.dest_code
                        and p2.code = 'RULUG'

                    group by day
                    order by day
            """
    )

    with Session() as session:
        query_result_by_code = [dict(row) for row in session.execute(query).fetchall()]

    assert len(query_result_by_code) == len(function_result_by_code)

    for query_resu, func_resu in zip(query_result_by_code, function_result_by_code):
        assert (
            query_resu == func_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "


def test_rates_from_port_to_port_using_name():
    """
    Compare results of rates from one region to a specific port by using the code or name of the port

    """

    function_result_by_name: List[Row] = get_rates(
        date(2016, 1, 27),
        date(2016, 1, 30),
        ("Shanghai", PortColumn.NAME),
        ("Lugovoye", PortColumn.NAME),
    )

    query = text(
        f"""
                    select day, round(avg(price), 2) from ports
                        inner join prices p on
                            ports.code = p.orig_code
                        -- by origin
                        and ports.name = 'Shanghai'
                        -- by date
                       and p.day BETWEEN '2016-01-27' and '2016-01-30'
                        inner join ports p2 on
                            p2.code = p.dest_code
                        and p2.name = 'Lugovoye'
                        
                    group by day
                    order by day
            """
    )

    with Session() as session:
        query_result_by_name = [dict(row) for row in session.execute(query).fetchall()]

    assert len(query_result_by_name) == len(function_result_by_name)

    for query_resu, func_resu in zip(query_result_by_name, function_result_by_name):
        assert (
            query_resu == func_resu
        ), f"The result of the function ({func_resu}) not equal ({query_resu}) "
