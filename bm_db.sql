--
-- PostgreSQL database dump
--

-- Dumped from database version 10.8 (Ubuntu 10.8-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.8 (Ubuntu 10.8-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

--COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: binance_order; Type: TABLE; Schema: public; Owner: xnpio
--

CREATE TABLE public.binance_order (
    order_id integer NOT NULL,
    transaction_id integer,
    price numeric(13,8),
    type integer,
    state integer
);


ALTER TABLE public.binance_order OWNER TO xnpio;

--
-- Name: binance_order_order_id_seq; Type: SEQUENCE; Schema: public; Owner: xnpio
--

CREATE SEQUENCE public.binance_order_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.binance_order_order_id_seq OWNER TO xnpio;

--
-- Name: binance_order_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: xnpio
--

ALTER SEQUENCE public.binance_order_order_id_seq OWNED BY public.binance_order.order_id;


--
-- Name: dates; Type: TABLE; Schema: public; Owner: xnpio
--

CREATE TABLE public.dates (
    date_id integer NOT NULL,
    order_id integer,
    init_date timestamp without time zone,
    open_date timestamp without time zone,
    done_date timestamp without time zone
);


ALTER TABLE public.dates OWNER TO xnpio;

--
-- Name: dates_date_id_seq; Type: SEQUENCE; Schema: public; Owner: xnpio
--

CREATE SEQUENCE public.dates_date_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dates_date_id_seq OWNER TO xnpio;

--
-- Name: dates_date_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: xnpio
--

ALTER SEQUENCE public.dates_date_id_seq OWNED BY public.dates.date_id;


--
-- Name: state; Type: TABLE; Schema: public; Owner: xnpio
--

CREATE TABLE public.state (
    state_id integer NOT NULL,
    name character varying(128)
);


ALTER TABLE public.state OWNER TO xnpio;

--
-- Name: transaction; Type: TABLE; Schema: public; Owner: xnpio
--

CREATE TABLE public.transaction (
    transaction_id integer NOT NULL,
    symbol character varying(16)
);


ALTER TABLE public.transaction OWNER TO xnpio;

--
-- Name: transaction_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: xnpio
--

CREATE SEQUENCE public.transaction_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_transaction_id_seq OWNER TO xnpio;

--
-- Name: transaction_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: xnpio
--

ALTER SEQUENCE public.transaction_transaction_id_seq OWNED BY public.transaction.transaction_id;


--
-- Name: type; Type: TABLE; Schema: public; Owner: xnpio
--

CREATE TABLE public.type (
    type_id integer NOT NULL,
    name character varying(128)
);


ALTER TABLE public.type OWNER TO xnpio;

--
-- Name: binance_order order_id; Type: DEFAULT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.binance_order ALTER COLUMN order_id SET DEFAULT nextval('public.binance_order_order_id_seq'::regclass);


--
-- Name: dates date_id; Type: DEFAULT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.dates ALTER COLUMN date_id SET DEFAULT nextval('public.dates_date_id_seq'::regclass);


--
-- Name: transaction transaction_id; Type: DEFAULT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.transaction ALTER COLUMN transaction_id SET DEFAULT nextval('public.transaction_transaction_id_seq'::regclass);


--
-- Data for Name: binance_order; Type: TABLE DATA; Schema: public; Owner: xnpio
--

COPY public.binance_order (order_id, transaction_id, price, type, state) FROM stdin;
\.


--
-- Data for Name: dates; Type: TABLE DATA; Schema: public; Owner: xnpio
--

COPY public.dates (date_id, order_id, init_date, open_date, done_date) FROM stdin;
\.


--
-- Data for Name: state; Type: TABLE DATA; Schema: public; Owner: xnpio
--

COPY public.state (state_id, name) FROM stdin;
0	init
1	waiting
2	open
3	filled
4	canceled
5	disabled
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: xnpio
--

COPY public.transaction (transaction_id, symbol) FROM stdin;
\.


--
-- Data for Name: type; Type: TABLE DATA; Schema: public; Owner: xnpio
--

COPY public.type (type_id, name) FROM stdin;
0	entry
1	lose
2	profit
\.


--
-- Name: binance_order_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: xnpio
--

SELECT pg_catalog.setval('public.binance_order_order_id_seq', 1, true);


--
-- Name: dates_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: xnpio
--

SELECT pg_catalog.setval('public.dates_date_id_seq', 1, false);


--
-- Name: transaction_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: xnpio
--

SELECT pg_catalog.setval('public.transaction_transaction_id_seq', 3, true);


--
-- Name: binance_order binance_order_pkey; Type: CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.binance_order
    ADD CONSTRAINT binance_order_pkey PRIMARY KEY (order_id);


--
-- Name: dates dates_pkey; Type: CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.dates
    ADD CONSTRAINT dates_pkey PRIMARY KEY (date_id);


--
-- Name: state state_pkey; Type: CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.state
    ADD CONSTRAINT state_pkey PRIMARY KEY (state_id);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (transaction_id);


--
-- Name: type type_pkey; Type: CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.type
    ADD CONSTRAINT type_pkey PRIMARY KEY (type_id);


--
-- Name: binance_order binance_order_state_fkey; Type: FK CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.binance_order
    ADD CONSTRAINT binance_order_state_fkey FOREIGN KEY (state) REFERENCES public.state(state_id);


--
-- Name: binance_order binance_order_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.binance_order
    ADD CONSTRAINT binance_order_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES public.transaction(transaction_id);


--
-- Name: binance_order binance_order_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.binance_order
    ADD CONSTRAINT binance_order_type_fkey FOREIGN KEY (type) REFERENCES public.type(type_id);


--
-- Name: dates dates_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: xnpio
--

ALTER TABLE ONLY public.dates
    ADD CONSTRAINT dates_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.binance_order(order_id);


--
-- PostgreSQL database dump complete
--

