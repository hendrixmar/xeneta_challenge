WITH RECURSIVE regions_contained_origin AS (
                select * from regions
                    where
                        slug in ('{origin_value}')
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
                    slug in ('{destination_value}')
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
            select * from regions_contained_origin
                inner join ports on
                    ports.parent_slug = regions_contained_origin.slug
                inner join prices p1 on
                    ports.code = p1.orig_code
                    -- filter price by dates
                   {filter_by_date}
                inner join ports p2 on
                    p2.code = p1.dest_code
                and p2.parent_slug in (select slug from regions_contained_destiny);