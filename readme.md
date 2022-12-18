# Xeneta challenge


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Hi xeneta team. I present you my project I hope you like what I have done. The main tecnology used for the are the following

- [PostgreSql]
- [FastAPI]
- [Docker Compose]
- [SQLAlchemy]
- [Pytest]
- [coverage]


## Setup
To setup the whole project you have to execute the following command after cloning the respository:

```sh
$ docker compose up
```

if anything is working fine you should see a swagger UI in you browser when you go to this [link](http://0.0.0.0:8000/docs)

![alt text](images/swagger.png)
## Features

- You can retrieve rates by using code, name, region
- Added more aggregate function like SUM, COUNT, MIN, MAX, and STD
- A port searcher using fuzzy matching (in case you forgot the exact name of the port you want to analyze)
- A little script for converting txt file to a csv file to fill the database



## Project structure



I structured this project using [fastapi best practices](https://github.com/zhanymkanov/fastapi-best-practices)  resource.
The projected as followed:
```
app
├── db
│   ├── get_rate_region_to_region.sql
│   ├── init_db.py
│   └── __init__.py
├── db.py
├── __init__.py
├── main.py
├── ports
│   ├── __init__.py
│   ├── router.py
│   └── service.py
├── rates
│   ├── __init__.py
│   ├── router.py
│   ├── service.py
│   └── utils.py
├── tests
│   ├── __init__.py
│   ├── test_integration.py
│   └── test_unit_test_rates_retrieval.py
└── tools
    ├── __init__.py
    ├── settings.py
    └── utils.py
```

## Test Coverage

I created several unit test and integrations test and got the following test coverage results
```
Name                                          Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------
app/__init__.py                                   0      0   100%
app/config.py                                    11      0   100%
app/db/__init__.py                                0      0   100%
app/db/init_db.py                                 5      0   100%
app/main.py                                       9      1    89%   10
app/ports/__init__.py                             0      0   100%
app/ports/router.py                               9      1    89%   14
app/ports/service.py                              9      4    56%   10-17
app/ports/utils.py                               24      4    83%   56-60
app/rates/__init__.py                             0      0   100%
app/rates/router.py                              18      4    78%   17-21
app/rates/service.py                             57     11    81%   32-45, 55-60, 79, 92, 96
app/rates/utils.py                               21      0   100%
app/tests/__init__.py                             0      0   100%
app/tests/test_integration.py                    33      0   100%
app/tests/test_unit_test_rates_retrieval.py      67      2    97%   370, 412
app/tools/__init__.py                             0      0   100%
app/tools/utils.py                                9      0   100%
---------------------------------------------------------------------------
TOTAL                                           272     27    90%
```


Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [SQLAlchemy]: <https://github.com/sqlalchemy>
   [coverage]: <https://coverage.readthedocs.io/en/6.5.0/>
   [Docker Compose]: <https://docs.docker.com/compose/>
   [FastAPI]: <https://fastapi.tiangolo.com/>
   [Pytest]: <https://docs.pytest.org/en/7.2.x/>
   [PostgreSql]: <https://www.postgresql.org/docs/>


