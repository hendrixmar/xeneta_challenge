import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.database import Session

client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        (
            "/rates?date_from=2016-30-1",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "date_from"],
                        "msg": "invalid date format",
                        "type": "value_error.date",
                    }
                ]
            },
        ),
        (
            "/rates?date_to=2016-30-1",
            422,
            {
                "detail": [
                    {
                        "loc": ["query", "date_to"],
                        "msg": "invalid date format",
                        "type": "value_error.date",
                    }
                ]
            },
        ),
        (
            "/rates?aggregate_functions=AVGG&aggregate_functions=MAX",
            422,
            {
                "detail": [
                    {
                        "ctx": {
                            "enum_values": ["AVG", "SUM", "COUNT", "MAX", "MIN", "STD"]
                        },
                        "loc": ["query", "aggregate_functions", 0],
                        "msg": "value is not a valid enumeration member; permitted: "
                        "'AVG', 'SUM', 'COUNT', 'MAX', 'MIN', 'STD'",
                        "type": "type_error.enum",
                    }
                ]
            },
        ),
    ],
)
def test_query_parameter_validation(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_invalid_date():
    response = client.get("/rates", params={"date_from": "2016-30-1"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "date_from"],
                "msg": "invalid date format",
                "type": "value_error.date",
            }
        ]
    }


@pytest.mark.parametrize(
    "path, expected_status, expected_response",
    [
        (
            "/rates?destination=changai",
            404,
            {"detail": "The parameter changai isn't related with any port"},
        ),
        (
            "/rates?destination=CNSGHH",
            404,
            {"detail": "The parameter CNSGHH isn't related with any port"},
        ),
        (
            "/rates?destination=china_eas_main",
            404,
            {"detail": "The parameter china_eas_main isn't related with any port"},
        ),
        (
            "/rates?origin=changai",
            404,
            {"detail": "The parameter changai isn't related with any port"},
        ),
        (
            "/rates?origin=CNSGHH",
            404,
            {"detail": "The parameter CNSGHH isn't related with any port"},
        ),
        (
            "/rates?origin=china_eas_main",
            404,
            {"detail": "The parameter china_eas_main isn't related with any port"},
        ),
    ],
)
def test_destination_origin_validation(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_integration_date_from_region_to_region():
    """
    Compare results of rates from one region to another of the function get_rates

    """

    response = client.get(
        "/rates?date_from=2016-1-27&date_to=2016-1-30&origin=china_main&destination=baltic"
    )
    assert response.status_code == 200
    query = text(
        """
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
                select day, 
                    CASE WHEN count(*) > 3  
                        THEN round(avg(price),2) 
                        ELSE null
                    END 
                    as average_price from regions_contained_origin
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

    for query_resu, resp_resu in zip(query_result, response.json()):
        assert str(query_resu.get("day")) == str(resp_resu.get("day")) and str(
            query_resu.get("average_price")
        ) == str(
            resp_resu.get("average_price")
        ), f"The result of the function ({resp_resu}) not equal ({query_resu}) "
