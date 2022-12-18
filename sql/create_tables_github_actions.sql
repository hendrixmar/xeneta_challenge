--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tasks; Type: SCHEMA; Schema: -; Owner: -
--

-- CREATE SCHEMA tasks;


-- SET search_path = tasks, pg_catalog;

SET default_with_oids = false;


--
-- Name: ports; Type: TABLE; Schema: tasks; Owner: -
--

CREATE TABLE ports (
    code text NOT NULL,
    name text NOT NULL,
    parent_slug text NOT NULL
);


--
-- Name: prices; Type: TABLE; Schema: tasks; Owner: -
--

CREATE TABLE prices (
    orig_code text NOT NULL,
    dest_code text NOT NULL,
    day date NOT NULL,
    price NUMERIC(20, 2) NOT NULL
);


--
-- Name: regions; Type: TABLE; Schema: tasks; Owner: -
--

CREATE TABLE regions (
    slug text NOT NULL,
    name text NOT NULL,
    parent_slug text
);


--
-- Import the file ports.csv to fill the table ports
--

COPY ports(code, name, parent_slug)
FROM 'sql/ports.csv'
DELIMITER ','
CSV HEADER
NULL as 'NULL';

--
-- Import the file regions.csv to fill the table regions
--

COPY regions(slug, name, parent_slug)
FROM 'sql/regions.csv'
DELIMITER ','
CSV HEADER
NULL as 'NULL';

--
-- Import the file prices.csv to fill the table prices
--

COPY prices(orig_code, dest_code, day, price)
FROM 'sql/prices.csv'
DELIMITER ','
CSV HEADER
NULL as 'NULL';

---
--- Name: prices idx_date; Type: INDEX; Schema: tasks; Owner: Hendrik
---

CREATE INDEX idx_date
ON prices(day);


--
-- Name: ports ports_pkey; Type: CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (code);


--
-- Name: regions regions_pkey; Type: CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY regions
    ADD CONSTRAINT regions_pkey PRIMARY KEY (slug);


--
-- Name: ports ports_parent_slug_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY ports
    ADD CONSTRAINT ports_parent_slug_fkey FOREIGN KEY (parent_slug) REFERENCES regions(slug);


--
-- Name: prices prices_dest_code_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY prices
    ADD CONSTRAINT prices_dest_code_fkey FOREIGN KEY (dest_code) REFERENCES ports(code);


--
-- Name: prices prices_orig_code_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY prices
    ADD CONSTRAINT prices_orig_code_fkey FOREIGN KEY (orig_code) REFERENCES ports(code);


--
-- Name: regions regions_parent_slug_fkey; Type: FK CONSTRAINT; Schema: tasks; Owner: -
--

ALTER TABLE ONLY regions
    ADD CONSTRAINT regions_parent_slug_fkey FOREIGN KEY (parent_slug) REFERENCES regions(slug);

