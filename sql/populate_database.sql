
-- all the price join with regions and ports
select p1.code, p1.name,r1.parent_slug as region_orig,
       prices.price, prices.day,
       p2.code, p2.name, r2.parent_slug as region_dest
    from prices
    left join ports p1 on
        p1.code = prices.orig_code
    left join ports p2 on
        p2.code = prices.dest_code
    inner join regions r1 on
        p1.parent_slug = r1.slug
    inner join regions r2 on
        p2.parent_slug = r2.slug;

select * from ports
    inner join prices p on
        ports.code = p.orig_code
    and ports.code = 'CNCWN'
    inner join ports p2 on
        p2.code = p.dest_code
    and p2.code = 'NOTRD';

select * from ports
    inner join prices p on
        ports.code = p.orig_code
    and ports.name = 'Chiwan'
    inner join ports p2 on
        p2.code = p.dest_code
    and p2.code = 'NOTRD';


select p1.code, p1.name,regions.slug, regions.parent_slug
    from regions
     inner join ports p1 on
        regions.slug = p1.parent_slug
;


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
                    select day, avg(price) from ports
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
                    order by day;


           WITH RECURSIVE regions_contained_destiny AS (
                    select * from regions where slug in ('north_europe_main')
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
                        and ports.name = 'Shanghai'

                    -- Filtering by a date
                       and day BETWEEN '2016-01-27' AND '2016-01-30'
                    inner join ports prt on
                    prt.code = p1.dest_code and
                    prt.parent_slug in (select slug from regions_contained_destiny)
                group by day
                order by day;


-- query for getting all the prices from a region a to region b
WITH RECURSIVE regions_contained_origin AS (
    select
        *
    from
        regions
    where
        slug in ('china_main')
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
    select
        *
    from
        regions
    where
        slug in ('baltic')
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
select day, avg(price)
         from regions_contained_origin
    inner join ports on
        ports.parent_slug = regions_contained_origin.slug
    inner join prices p1 on
        ports.code = p1.orig_code
        -- filter price by dates
       and p1.day BETWEEN '2016-01-27' AND '2016-01-30'
    inner join ports p2 on
        p2.code = p1.dest_code
    and p2.parent_slug in (select slug from regions_contained_destiny)
group by day;

  select day, avg(price), ROUND(STDDEV(price), 2) from ports
                        inner join prices p on
                            ports.code = p.orig_code
                        and ports.code = 'CNGGZ'
                        inner join ports p2 on
                            p2.code = p.dest_code
                        and p2.code = 'EETLL'
                    group by day;



select day, avg(price) from ports
    inner join prices p on
        ports.code = p.orig_code
    -- by origin
    and ports.code = 'china_main'
    -- by date
    and day BETWEEN '2016-01-01' AND '2016-01-30'
    inner join ports p2 on
        p2.code = p.dest_code
    and p2.code = 'EETLL'
group by day;


-- query for getting all the prices from a region a to a code or name
WITH RECURSIVE regions_contained_origin AS (
    select
        *
    from
        regions
    where
        slug in ('china_main')
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
select *--day, avg(price)
         from regions_contained_origin
    inner join ports on
        ports.parent_slug = regions_contained_origin.slug
    inner join prices p1 on
        ports.code = p1.orig_code
        -- filter price by dates
       and p1.day BETWEEN '2016-01-27' AND '2016-01-30'
    inner join ports p2 on
        p2.code = p1.dest_code
    and ( p2.name = 'Måløy');
group by day;


-- from code or name to region
WITH RECURSIVE regions_contained_destiny AS (
    select
        *
    from
        regions
    where
        slug in ('north_europe_main')
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
select  *
         from ports
    inner join prices  p1 on
        ports.code = p1.orig_code
        and ports.code = 'CNCWN'
        -- filter price by dates
       -- and p1.day BETWEEN '2016-01-27' AND '2016-01-30'
    inner join ports prt on
    prt.code = p1.dest_code and
    prt.parent_slug in (select slug from regions_contained_destiny);




CREATE RECURSIVE VIEW regions_contained_origin AS (
    select
        *
    from
        regions
    union
        select
            regions.slug,
            regions.name,
            regions.parent_slug
        from
            regions
        inner join regions_contained_origin on
            regions_contained_origin.slug = regions.parent_slug
);
select * from regions_contained_origin;

select count(*) from prices where prices.orig_code in ('CNCWN','CNYAT','CNSNZ','CNSHK','HKHKG','CNNBO','CNDAL','CNSGH','CNHDG','CNGGZ','CNQIN','CNLYG','CNTXG','CNXAM' ,'CNYTN');

WITH RECURSIVE regions_contained_destiny AS (
    select
        *
    from
        regions
    where
        slug = 'baltic'
    union
        select
            regions.slug,
            regions.name,
            regions.parent_slug
        from
            regions
        inner join regions_contained_destiny on
            regions_contained_destiny.slug = regions.parent_slug
);

-- curl "http://127.0.0.1/rates?
-- date_from=2016-01-01&date_to=2016-01-10&
-- origin=CNSGH&destination=north_europe_main"
select code, name, parent_slug from ports;

select slug, length(slug) from regions order by length(slug) desc;


CREATE EXTENSION fuzzystrmatch;

SELECT levenshtein('Marcuzzz', 'Markus');

SELECT code, name, parent_slug
    FROM ports
    WHERE levenshtein('amsterDam', parent_slug) <= 1 or
          levenshtein('amsterDam', name) <= 1 or
          levenshtein('amsterDam', code) <= 1;


select (select true from ports where ports.code = 'DKAAL'), (select true from ports where ports.code = 'DKAAxL'), (select true from ports where ports.code = 'DKxAAL');