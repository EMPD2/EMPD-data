--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: ageuncertainties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ageuncertainties (
    ageuncertainty character varying(1) NOT NULL,
    description character varying(21) NOT NULL,
    age character varying(14)
);


ALTER TABLE public.ageuncertainties OWNER TO postgres;

--
-- Name: climate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.climate (
    samplename character varying(25) NOT NULL,
    t_jan double precision,
    t_feb double precision,
    t_mar double precision,
    t_apr double precision,
    t_may double precision,
    t_jun double precision,
    t_jul double precision,
    t_aug double precision,
    t_sep double precision,
    t_oct double precision,
    t_nov double precision,
    t_dec double precision,
    t_djf double precision,
    t_mam double precision,
    t_jja double precision,
    t_son double precision,
    t_ann double precision,
    p_jan double precision,
    p_feb double precision,
    p_mar double precision,
    p_apr double precision,
    p_may double precision,
    p_jun double precision,
    p_jul double precision,
    p_aug double precision,
    p_sep double precision,
    p_oct double precision,
    p_nov double precision,
    p_dec double precision,
    p_djf double precision,
    p_mam double precision,
    p_jja double precision,
    p_son double precision,
    p_ann double precision
);


ALTER TABLE public.climate OWNER TO postgres;

--
-- Name: countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.countries (
    country character varying(42) NOT NULL,
    natural_earth character varying(42)
);


ALTER TABLE public.countries OWNER TO postgres;

--
-- Name: ecosystems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ecosystems (
    samplename character varying(25) NOT NULL,
    realm character(16),
    biome character(62),
    ecoregion character(65)
);


ALTER TABLE public.ecosystems OWNER TO postgres;

--
-- Name: groupid; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groupid (
    groupid character varying(9) NOT NULL,
    groupname character varying(60) NOT NULL,
    higher_groupid character varying(4) NOT NULL,
    used_in_sum boolean DEFAULT false,
    percent_values boolean DEFAULT false
);


ALTER TABLE public.groupid OWNER TO postgres;

--
-- Name: locationreliabilities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locationreliabilities (
    locationreliability character varying(1) NOT NULL,
    description character varying(55) NOT NULL,
    error character varying(5)
);


ALTER TABLE public.locationreliabilities OWNER TO postgres;

--
-- Name: metaViewer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."metaViewer" (
    "SampleName" text,
    "OriginalSampleName" text,
    "SiteName" text,
    "Country" text,
    "Longitude" double precision,
    "Latitude" double precision,
    "Elevation" double precision,
    "Temperature" text,
    "Precipitation" text,
    "LocationReliability" text,
    "LocationNotes" text,
    "AreaOfSite" double precision,
    "SampleContext" text,
    "SiteDescription" text,
    "VegDescription" text,
    "SampleType" text,
    "SampleMethod" text,
    "AgeBP" double precision,
    "AgeUncertainty" text,
    ispercent boolean,
    "Notes" text,
    "EMPD_version" text,
    "Publication1" text,
    "DOI1" text,
    "Publication2" text,
    "DOI2" text,
    "Publication3" text,
    "DOI3" text,
    "Publication4" text,
    "DOI4" text,
    "Publication5" text,
    "DOI5" text,
    "Worker1_Role" text,
    "Worker1_LastName" text,
    "Worker1_Initials" text,
    "Worker1_FirstName" text,
    "Worker1_Address1" text,
    "Worker1_Address2" text,
    "Worker1_Email1" text,
    "Worker1_Email2" text,
    "Worker1_Phone1" text,
    "Worker1_Phone2" text,
    "Worker2_Role" text,
    "Worker2_LastName" text,
    "Worker2_Initials" text,
    "Worker2_FirstName" text,
    "Worker2_Address1" text,
    "Worker2_Address2" text,
    "Worker2_Email1" text,
    "Worker2_Email2" text,
    "Worker2_Phone1" text,
    "Worker2_Phone2" text,
    "Worker3_Role" text,
    "Worker3_LastName" text,
    "Worker3_Initials" text,
    "Worker3_FirstName" text,
    "Worker3_Address1" text,
    "Worker3_Address2" text,
    "Worker3_Email1" text,
    "Worker3_Email2" text,
    "Worker3_Phone1" text,
    "Worker3_Phone2" text,
    "Worker4_Role" text,
    "Worker4_LastName" text,
    "Worker4_Initials" text,
    "Worker4_FirstName" text,
    "Worker4_Address1" text,
    "Worker4_Address2" text,
    "Worker4_Email1" text,
    "Worker4_Email2" text,
    "Worker4_Phone1" text,
    "Worker4_Phone2" text,
    okexcept text
);


ALTER TABLE public."metaViewer" OWNER TO postgres;

--
-- Name: metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metadata (
    samplename character varying(25) NOT NULL,
    originalsamplename character varying(70),
    sitename character varying(70),
    country character varying(42),
    longitude double precision,
    latitude double precision,
    elevation double precision,
    locationreliability character varying(1),
    locationnotes text,
    areaofsite double precision,
    samplecontext character varying(40),
    sitedescription text,
    vegdescription text,
    sampletype character varying(14),
    samplemethod character varying(31),
    agebp double precision,
    ageuncertainty character varying(1),
    ispercent boolean DEFAULT false,
    notes text,
    okexcept text,
    empd_version character varying(5)
);


ALTER TABLE public.metadata OWNER TO postgres;

--
-- Name: metapubli; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metapubli (
    samplename character varying(25) NOT NULL,
    publiid integer NOT NULL
);


ALTER TABLE public.metapubli OWNER TO postgres;

--
-- Name: metaworker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metaworker (
    samplename character varying(25) NOT NULL,
    workerid integer NOT NULL,
    workerrole character varying(3)
);


ALTER TABLE public.metaworker OWNER TO postgres;

--
-- Name: p_counts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.p_counts (
    samplename character varying(25) NOT NULL,
    var_ integer NOT NULL,
    count double precision NOT NULL,
    percentage double precision
);


ALTER TABLE public.p_counts OWNER TO postgres;

--
-- Name: p_vars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.p_vars (
    var_ integer NOT NULL,
    acc_var_ integer,
    original_varname character varying(100) NOT NULL,
    acc_varname character varying(100),
    groupid character varying(9),
    notes text
);


ALTER TABLE public.p_vars OWNER TO postgres;

--
-- Name: publications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.publications (
    publiid integer NOT NULL,
    doi character varying(50),
    reference text NOT NULL
);


ALTER TABLE public.publications OWNER TO postgres;

--
-- Name: samplecontexts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samplecontexts (
    samplecontext character varying(40) NOT NULL
);


ALTER TABLE public.samplecontexts OWNER TO postgres;

--
-- Name: samplemethods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samplemethods (
    samplemethod character varying(31) NOT NULL
);


ALTER TABLE public.samplemethods OWNER TO postgres;

--
-- Name: sampletypes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sampletypes (
    sampletype character varying(14) NOT NULL,
    notes character varying(13)
);


ALTER TABLE public.sampletypes OWNER TO postgres;

--
-- Name: workerroles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workerroles (
    workerrole character varying(3) NOT NULL,
    description character varying(35) NOT NULL
);


ALTER TABLE public.workerroles OWNER TO postgres;

--
-- Name: workers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workers (
    workerid integer NOT NULL,
    firstname character varying(25),
    lastname character varying(25),
    initials character varying(10),
    address1 text,
    email1 character varying(50),
    phone1 character varying(25),
    address2 text,
    email2 character varying(50),
    phone2 character varying(25)
);


ALTER TABLE public.workers OWNER TO postgres;

--
-- Data for Name: ageuncertainties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ageuncertainties (ageuncertainty, description, age) FROM stdin;
A	Modern sample	0BP to Present
B	Within last 100 years	0-50BP
C	Within last 250 years	50-200BP
\.


--
-- Data for Name: climate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.climate (samplename, t_jan, t_feb, t_mar, t_apr, t_may, t_jun, t_jul, t_aug, t_sep, t_oct, t_nov, t_dec, t_djf, t_mam, t_jja, t_son, t_ann, p_jan, p_feb, p_mar, p_apr, p_may, p_jun, p_jul, p_aug, p_sep, p_oct, p_nov, p_dec, p_djf, p_mam, p_jja, p_son, p_ann) FROM stdin;
test_a1	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5
test_a2	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5
test_a3	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5	5
\.


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countries (country, natural_earth) FROM stdin;
Albania	Albania
Algeria	Algeria
Andorra	Andorra
Armenia	Armenia
Austria	Austria
Azerbaijan	Azerbaijan
Bahrain	Bahrain
Belarus	Belarus
Belgium	Belgium
Bosnia And Herzegovina	Bosnia and Herzegovina
Bulgaria	Bulgaria
Cape Verde	Cabo Verde
China, People s Republic Of	China
Croatia	Croatia
Cyprus	Cyprus
Czech Republic	Czechia
Denmark	Denmark
Egypt	Egypt
Eritrea	Eritrea
Estonia	Estonia
Ethiopia	Ethiopia
Faroe Islands	Faroe Islands
Finland	Finland
France	France
Georgia	Georgia
Germany	Germany
Gibraltar	Gibraltar
Greece	Greece
Greenland	Greenland
Guernsey	Guernsey
Hungary	Hungary
Iceland	Iceland
India	India
Iran, Islamic Republic Of	Iran
Iraq	Iraq
Ireland	Ireland
Isle Of Man	Isle of Man
Israel	Israel
Italy	Italy
Japan	Japan
Jersey	Jersey
Jordan	Jordan
Kazakhstan	Kazakhstan
Kuwait	Kuwait
Kyrgyzstan	Kyrgyzstan
Latvia	Latvia
Lebanon	Lebanon
Libyan Arab Jamahiriya	Libya
Liechtenstein	Liechtenstein
Lithuania	Lithuania
Luxembourg	Luxembourg
Macedonia, The Former Yugoslav Republic Of	Macedonia
Malta	Malta
Moldova, Republic Of	Moldova
Monaco	Monaco
Serbia And Montenegro	Montenegro
Morocco	Morocco
Netherlands	Netherlands
Norway	Norway
Svalbard and Jan Mayen	Norway
Oman	Oman
Palestinian Territory, Occupied	Palestine
Poland	Poland
Portugal	Portugal
Qatar	Qatar
Romania	Romania
Russian Federation	Russia
San Marino	San Marino
Saudi Arabia	Saudi Arabia
Slovakia	Slovakia
Slovenia	Slovenia
Spain	Spain
Sweden	Sweden
Switzerland	Switzerland
Syrian Arab Republic	Syria
Tunisia	Tunisia
Turkey	Turkey
Turkmenistan, Republic Of	Turkmenistan
Ukraine	Ukraine
United Arab Emirates	United Arab Emirates
United Kingdom	United Kingdom
Yemen	Yemen
Black Sea	\N
Dead Sea	\N
Adriatic Sea	\N
\.


--
-- Data for Name: ecosystems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ecosystems (samplename, realm, biome, ecoregion) FROM stdin;
\.


--
-- Data for Name: groupid; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.groupid (groupid, groupname, higher_groupid, used_in_sum, percent_values) FROM stdin;
ACRI	Acritarchs	NOPO	f	f
ALGA	Algae	AQUA	f	t
AQBR	Aquatic Bryophytes	AQUA	f	t
AQPT	Aquatic Pteridophyta	AQUA	f	t
AQUA	Aquatics	AQUA	f	t
AQVP	Aquatic Vascular Plants	AQUA	f	t
BRYO	Bryophytes	VACR	t	t
CHAR	Charcoal	CHAR	f	f
CHLO	Chlorophytes	NOPO	f	f
CYAN	Cyanobacteria	NOPO	f	f
DINO	Dinoflagellates	NOPO	f	f
DWAR	Dwarf shrubs	TRSH	t	t
FUNG	Fungi	NOPO	f	f
HELO	Helophytes	AQUA	f	t
HEMI	Hemi-parasitic	NOPO	f	f
HERB	Herbs	HERB	t	t
INUN	Indeterminables and unknowns	INUN	f	f
INVE	Invertebrates	NOPO	f	f
LIAN	Liana	LIAN	t	t
MACR	Macrofossils	NOPO	f	f
MICR	Microcrustaceans	NOPO	f	f
NEMA	Nematoda (roundworms)	NOPO	f	f
NOPO	Nonpollen	NOPO	f	f
PLAT	Platyhelminthes (flatworms)	NOPO	f	f
PREQ	Pre-Quaternary type	NOPO	f	f
RHIZ	Rhizopods	NOPO	f	f
ROTI	Rotifera (Rotifers)	NOPO	f	f
SPOR	Taxonomically undifferentiated spores	INUN	f	f
TEAM	Testate amoebae	NOPO	f	f
TRSH	Trees & Shrubs	TRSH	t	t
UNPP	Undifferentiated NPP	INUN	f	f
UPBR	Upland Bryophytes	VACR	t	t
UPHE	Upland herbs	HERB	t	t
VACR	Vascular cryptogams (Pteridophytes)	VACR	t	t
VEMI	Vegetative microfossils	NOPO	f	f
MOSS	Moss	VACR	t	t
\.


--
-- Data for Name: locationreliabilities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locationreliabilities (locationreliability, description, error) FROM stdin;
A	Good for high resolution remote sensing (<100m)	<100m
B	Good for lower resolution remote sensing (<1km)	<1km
C	Ok for climate reconstruction or regional scale mapping	<5km
D	Ok for mapping at continental scale	<20km
X	Do not use!	\N
\.


--
-- Data for Name: metaViewer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."metaViewer" ("SampleName", "OriginalSampleName", "SiteName", "Country", "Longitude", "Latitude", "Elevation", "Temperature", "Precipitation", "LocationReliability", "LocationNotes", "AreaOfSite", "SampleContext", "SiteDescription", "VegDescription", "SampleType", "SampleMethod", "AgeBP", "AgeUncertainty", ispercent, "Notes", "EMPD_version", "Publication1", "DOI1", "Publication2", "DOI2", "Publication3", "DOI3", "Publication4", "DOI4", "Publication5", "DOI5", "Worker1_Role", "Worker1_LastName", "Worker1_Initials", "Worker1_FirstName", "Worker1_Address1", "Worker1_Address2", "Worker1_Email1", "Worker1_Email2", "Worker1_Phone1", "Worker1_Phone2", "Worker2_Role", "Worker2_LastName", "Worker2_Initials", "Worker2_FirstName", "Worker2_Address1", "Worker2_Address2", "Worker2_Email1", "Worker2_Email2", "Worker2_Phone1", "Worker2_Phone2", "Worker3_Role", "Worker3_LastName", "Worker3_Initials", "Worker3_FirstName", "Worker3_Address1", "Worker3_Address2", "Worker3_Email1", "Worker3_Email2", "Worker3_Phone1", "Worker3_Phone2", "Worker4_Role", "Worker4_LastName", "Worker4_Initials", "Worker4_FirstName", "Worker4_Address1", "Worker4_Address2", "Worker4_Email1", "Worker4_Email2", "Worker4_Phone1", "Worker4_Phone2", okexcept) FROM stdin;
test_a1	orig_test_a1	somewhere	France	10	50	340	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5	X	Actually in Germany	30	\N	\N	\N	\N	\N	\N	\N	t	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
test_a2	orig_test_a2	somewhere	Germany	10	52	340	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5	X	Actually in Germany	30	\N	\N	\N	\N	\N	\N	\N	t	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	Country
test_a3	orig_test_a2	somewhere	Germany	10	52	340	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5	5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5	X	Actually in Germany	30	i dont know	\N	\N	\N	\N	\N	\N	t	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	SampleContext
\.


--
-- Data for Name: metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metadata (samplename, originalsamplename, sitename, country, longitude, latitude, elevation, locationreliability, locationnotes, areaofsite, samplecontext, sitedescription, vegdescription, sampletype, samplemethod, agebp, ageuncertainty, ispercent, notes, okexcept, empd_version) FROM stdin;
test_a1	orig_test_a1	somewhere	France	10	50	340	X	Actually in Germany	30	\N	\N	\N	\N	\N	\N	\N	f	\N	\N	\N
test_a2	orig_test_a2	somewhere	Germany	10	52	340	X	Actually in Germany	30	\N	\N	\N	\N	\N	\N	\N	f	\N	Country	\N
test_a3	orig_test_a2	somewhere	Germany	10	52	340	X	Actually in Germany	30	i dont know	\N	\N	\N	\N	\N	\N	f	\N	\N	\N
\.


--
-- Data for Name: metapubli; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metapubli (samplename, publiid) FROM stdin;
\.


--
-- Data for Name: metaworker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metaworker (samplename, workerid, workerrole) FROM stdin;
\.


--
-- Data for Name: p_counts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.p_counts (samplename, var_, count, percentage) FROM stdin;
test_a2	1	45	\N
test_a2	2	6	\N
test_a2	3	55	\N
test_a3	1	45	\N
test_a3	2	6	\N
test_a3	3	55	\N
\.


--
-- Data for Name: p_vars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.p_vars (var_, acc_var_, original_varname, acc_varname, groupid, notes) FROM stdin;
1	\N	Pinus	Pinus	TRSH	NULL
2	\N	Exotic	Exotics (counted)	NOPO	NULL
3	\N	Umbelliferae	Apiaceae	HERB	NULL
\.


--
-- Data for Name: publications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.publications (publiid, doi, reference) FROM stdin;
\.


--
-- Data for Name: samplecontexts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.samplecontexts (samplecontext) FROM stdin;
arable
blanket bog
bog
cave
cirque lake
closed forest
coastal
coastal lake
coastal wetland
drained_lake
ephemeral lake
ephemeral lake/pond
estuarine
fallow
fallow - scattered trees/shrubs
fen
floodplain mire
fluvial
forest
forest undefined
heath
ice from glacier
kettle lake
lagoon
lake
maquis
marine
marsh
marshland
mire
mor humus
moss-shrubby tundra
natural grassland
natural grasslands
natural open water
open forest
open forest/orchard
open forest/scattered trees/shrubs
orchard
orchard/scattered trees/shrubs
pasture
peatbog
pond
riverine
salt lake
salt marsh
scattered trees
scattered trees/shrubs
shrubs
shrubs/scrubland
soil
soligenous (mineraltrophic) Mire
sparse/no vegetation
swamp
tectonic lake
terrestrial
treeless vegetation
treeless vegetation/natural grassland
treeless vegetation/sparse vegetation
urban
valley mire
wetland
wetland bog
wetland bog/scattered trees/shrubs
wetland bog/treeless vegetation
archaeological
moss
section
sediments
i dont know
\.


--
-- Data for Name: samplemethods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.samplemethods (samplemethod) FROM stdin;
hand picking
hand picking - multiple samples
unspecified
auger corer
freeze corer
gravity corer
piston corer
russian corer
box
spade
hiller corer
gouge auger
core
corer unspecified
eckman-grab
box corer
\.


--
-- Data for Name: sampletypes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sampletypes (sampletype, notes) FROM stdin;
dung	\N
litter	\N
moss	\N
pollen trap	To be removed
sediment	submerged
spider web	\N
soil	terrestrial
sphagnum peat	\N
peat	\N
lichen	\N
submerged	\N
core_top	\N
tussock	\N
epiphytic moss	\N
\.


--
-- Data for Name: workerroles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workerroles (workerrole, description) FROM stdin;
R	Responsible Person
R/A	Both Responsible Person and Analyst
A	Analyst
A/D	Analyst (Deceased)
A/I	Analysis (Inactive)
A/U	Analyst (Unknown)
\.


--
-- Data for Name: workers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workers (workerid, firstname, lastname, initials, address1, email1, phone1, address2, email2, phone2) FROM stdin;
\.


--
-- Name: ageuncertainties ageuncertainties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ageuncertainties
    ADD CONSTRAINT ageuncertainties_pkey PRIMARY KEY (ageuncertainty);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (country);


--
-- Name: ecosystems ecosystems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ecosystems
    ADD CONSTRAINT ecosystems_pkey PRIMARY KEY (samplename);


--
-- Name: groupid groupid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groupid
    ADD CONSTRAINT groupid_pkey PRIMARY KEY (groupid);


--
-- Name: locationreliabilities locationreliabilities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locationreliabilities
    ADD CONSTRAINT locationreliabilities_pkey PRIMARY KEY (locationreliability);


--
-- Name: metadata metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_pkey PRIMARY KEY (samplename);


--
-- Name: metapubli metapubli_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metapubli
    ADD CONSTRAINT metapubli_pkey PRIMARY KEY (samplename, publiid);


--
-- Name: metaworker metaworker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metaworker
    ADD CONSTRAINT metaworker_pkey PRIMARY KEY (samplename, workerid);


--
-- Name: climate metaworkerclimate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.climate
    ADD CONSTRAINT metaworkerclimate_pkey PRIMARY KEY (samplename);


--
-- Name: p_counts p_counts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p_counts
    ADD CONSTRAINT p_counts_pkey PRIMARY KEY (samplename, var_);


--
-- Name: p_vars p_vars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p_vars
    ADD CONSTRAINT p_vars_pkey PRIMARY KEY (var_);


--
-- Name: publications publications_doi_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_doi_key UNIQUE (doi);


--
-- Name: publications publications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_pkey PRIMARY KEY (publiid);


--
-- Name: samplecontexts samplecontexts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samplecontexts
    ADD CONSTRAINT samplecontexts_pkey PRIMARY KEY (samplecontext);


--
-- Name: samplemethods samplemethods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samplemethods
    ADD CONSTRAINT samplemethods_pkey PRIMARY KEY (samplemethod);


--
-- Name: sampletypes sampletypes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sampletypes
    ADD CONSTRAINT sampletypes_pkey PRIMARY KEY (sampletype);


--
-- Name: workerroles workerroles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workerroles
    ADD CONSTRAINT workerroles_pkey PRIMARY KEY (workerrole);


--
-- Name: workers workers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workers
    ADD CONSTRAINT workers_pkey PRIMARY KEY (workerid);


--
-- Name: ix_metaViewer_SampleName; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_metaViewer_SampleName" ON public."metaViewer" USING btree ("SampleName");


--
-- Name: climate climates_samplename_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.climate
    ADD CONSTRAINT climates_samplename_fk FOREIGN KEY (samplename) REFERENCES public.metadata(samplename);


--
-- Name: ecosystems ecosystems_samplename_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ecosystems
    ADD CONSTRAINT ecosystems_samplename_fk FOREIGN KEY (samplename) REFERENCES public.metadata(samplename);


--
-- Name: metadata metadata_ageuncertainty_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_ageuncertainty_fk FOREIGN KEY (ageuncertainty) REFERENCES public.ageuncertainties(ageuncertainty);


--
-- Name: metadata metadata_country_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_country_fk FOREIGN KEY (country) REFERENCES public.countries(country);


--
-- Name: metadata metadata_locationreliability_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_locationreliability_fk FOREIGN KEY (locationreliability) REFERENCES public.locationreliabilities(locationreliability);


--
-- Name: metadata metadata_samplecontext_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_samplecontext_fk FOREIGN KEY (samplecontext) REFERENCES public.samplecontexts(samplecontext);


--
-- Name: metadata metadata_samplemethod_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_samplemethod_fk FOREIGN KEY (samplemethod) REFERENCES public.samplemethods(samplemethod);


--
-- Name: metadata metadata_sampletype_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metadata
    ADD CONSTRAINT metadata_sampletype_fk FOREIGN KEY (sampletype) REFERENCES public.sampletypes(sampletype);


--
-- Name: metapubli metapubli_publiid_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metapubli
    ADD CONSTRAINT metapubli_publiid_fk FOREIGN KEY (publiid) REFERENCES public.publications(publiid);


--
-- Name: metapubli metapubli_samplename_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metapubli
    ADD CONSTRAINT metapubli_samplename_fk FOREIGN KEY (samplename) REFERENCES public.metadata(samplename);


--
-- Name: metaworker metaworker_samplename_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metaworker
    ADD CONSTRAINT metaworker_samplename_fk FOREIGN KEY (samplename) REFERENCES public.metadata(samplename);


--
-- Name: metaworker metaworker_workerid_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metaworker
    ADD CONSTRAINT metaworker_workerid_fk FOREIGN KEY (workerid) REFERENCES public.workers(workerid);


--
-- Name: metaworker metaworker_workerrole_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metaworker
    ADD CONSTRAINT metaworker_workerrole_fk FOREIGN KEY (workerrole) REFERENCES public.workerroles(workerrole);


--
-- Name: p_counts p_counts_samplename_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p_counts
    ADD CONSTRAINT p_counts_samplename_fk FOREIGN KEY (samplename) REFERENCES public.metadata(samplename);


--
-- Name: p_counts p_counts_var__fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p_counts
    ADD CONSTRAINT p_counts_var__fk FOREIGN KEY (var_) REFERENCES public.p_vars(var_);


--
-- Name: p_vars p_vars_groupid_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p_vars
    ADD CONSTRAINT p_vars_groupid_fk FOREIGN KEY (groupid) REFERENCES public.groupid(groupid);


--
-- PostgreSQL database dump complete
--

