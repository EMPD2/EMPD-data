--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
--SET client_min_messages = warning;


--
-- Name: metadata; Type: TABLE; Schema: public;
-- OK

CREATE TABLE metadata (
    sampleName character varying(25) NOT NULL, -- PK
    originalSampleName character varying(70),
    siteName character varying(70),
    country character varying(42), -------------- FK
    longitude double precision,
    latitude double precision,
    elevation double precision,
    locationReliability character varying(1), --- FK
    locationNotes text,
    areaOfSite double precision,
    sampleContext character varying(40), -------- FK
    siteDescription text,
    vegDescription text,
    sampleType character varying(14), ----------- FK
    sampleMethod character varying(31), --------- FK
    ageBP double precision,
    ageUncertainty character varying(1), -------- FK
    isPercent boolean DEFAULT FALSE,
    notes text,
    empd_version character varying(5)
);
ALTER TABLE metadata OWNER TO postgres;
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_pkey PRIMARY KEY (sampleName);


--
-- Name: publication; Type: TABLE; Schema: public;
-- OK

CREATE TABLE publications (
    publiID integer NOT NULL, ------------------- PK
    DOI character varying(50) UNIQUE,
    reference text NOT NULL
);
ALTER TABLE publications OWNER TO postgres;
ALTER TABLE ONLY publications ADD CONSTRAINT publications_pkey PRIMARY KEY (publiID);


--
-- Name: workers; Type: TABLE; Schema: public;
-- OK

CREATE TABLE workers (
    workerID integer NOT NULL, ------------------ PK
    firstName character varying(25),
    lastName character varying(25),
    initials character varying(10),
    address1 text,
    email1 character varying(50),
    phone1 character varying(25),
    address2 text,
    email2 character varying(50),
    phone2 character varying(25)
);
ALTER TABLE workers OWNER TO postgres;
ALTER TABLE ONLY workers ADD CONSTRAINT workers_pkey PRIMARY KEY (workerID);


--
-- Name: p_counts; Type: TABLE; Schema: public;
-- OK

CREATE TABLE p_counts (
    sampleName character varying(25) NOT NULL, -- PK, FK
    var_ integer NOT NULL, ---------------------- PK, FK
    count double precision NOT NULL
);
ALTER TABLE p_counts OWNER TO postgres;
ALTER TABLE ONLY p_counts ADD CONSTRAINT p_counts_pkey PRIMARY KEY (sampleName, var_);


--
-- Name: p_vars; Type: TABLE; Schema: public;
-- OK

CREATE TABLE p_vars (
    var_ integer NOT NULL, ---------------------- PK
    acc_var_ integer,
    original_varname character varying(100) NOT NULL,
    acc_varname character varying(100),
    groupid character varying(9), ---------------- FK
    notes text
);
ALTER TABLE p_vars OWNER TO postgres;
ALTER TABLE ONLY p_vars ADD CONSTRAINT p_vars_pkey PRIMARY KEY (var_);


--
-- Name: countries; Type: TABLE; Schema: public;
-- OK

CREATE TABLE countries (
    country character varying(42) NOT NULL ------- PK
    natural_earth character varying(42)
);
ALTER TABLE countries OWNER TO postgres;
ALTER TABLE ONLY countries ADD CONSTRAINT countries_pkey PRIMARY KEY (country);

--
-- Name: wwf_terr_ecos; Type: TABLE; Schema: public; Owner: epd; Tablespace:
-- OK

CREATE TABLE ecosystems (
    sampleName character varying(25) NOT NULL, -- PK
    realm char(16),
    biome char(62),
    ecoregion char(65)
);
ALTER TABLE ecosystems OWNER TO postgres;
ALTER TABLE ONLY ecosystems ADD CONSTRAINT ecosystems_pkey PRIMARY KEY (sampleName);



--
-- Name: locationReliabilities; Type: TABLE; Schema: public;
-- OK

CREATE TABLE locationReliabilities (
    locationReliability character varying(1), --- PK
    description character varying(55) NOT NULL,
    error character varying(5)
);
ALTER TABLE locationReliabilities OWNER TO postgres;
ALTER TABLE ONLY locationReliabilities ADD CONSTRAINT locationReliabilities_pkey PRIMARY KEY (locationReliability);


--
-- Name: sampleContexts; Type: TABLE; Schema: public;
-- OK

CREATE TABLE sampleContexts (
    sampleContext character varying(40) --------- PK
);
ALTER TABLE sampleContexts OWNER TO postgres;
ALTER TABLE ONLY sampleContexts ADD CONSTRAINT sampleContexts_pkey PRIMARY KEY (sampleContext);


--
-- Name: sampleTypes; Type: TABLE; Schema: public;
-- OK

CREATE TABLE sampleTypes (
    sampleType character varying(14), ----------- PK
    notes character varying(13)
);
ALTER TABLE sampleTypes OWNER TO postgres;
ALTER TABLE ONLY sampleTypes ADD CONSTRAINT sampleTypes_pkey PRIMARY KEY (sampleType);


--
-- Name: collectionMethods; Type: TABLE; Schema: public;
-- OK

CREATE TABLE sampleMethods (
    sampleMethod character varying(31) ---------- PK
);
ALTER TABLE sampleMethods OWNER TO postgres;
ALTER TABLE ONLY sampleMethods ADD CONSTRAINT sampleMethods_pkey PRIMARY KEY (sampleMethod);


--
-- Name: ageUncertainties; Type: TABLE; Schema: public;
-- OK

CREATE TABLE ageUncertainties (
    ageUncertainty character varying(1), -------- PK
    description character varying(21) NOT NULL,
    age character varying(14)
);
ALTER TABLE ageUncertainties OWNER TO postgres;
ALTER TABLE ONLY ageUncertainties ADD CONSTRAINT ageUncertainties_pkey PRIMARY KEY (ageUncertainty);


--
-- Name: workerRoles; Type: TABLE; Schema: public;
-- OK

CREATE TABLE workerRoles (
    workerRole character varying(3), ------------ PK
    description character varying(35) NOT NULL
);
ALTER TABLE workerRoles OWNER TO postgres;
ALTER TABLE ONLY workerRoles ADD CONSTRAINT workerRoles_pkey PRIMARY KEY (workerRole);


--
-- Name: groupID; Type: TABLE; Schema: public;
-- OK

CREATE TABLE groupID (
    groupid character varying(9) NOT NULL, ------ PK
    groupname character varying(60) NOT NULL,
    higher_groupid character varying(4) NOT NULL
);
ALTER TABLE groupID OWNER TO postgres;
ALTER TABLE ONLY groupID ADD CONSTRAINT groupID_pkey PRIMARY KEY (groupid);


--
-- Name: metadataPubli; Type: TABLE; Schema: public
-- OK

CREATE TABLE metaPubli (
    sampleName character varying(25) NOT NULL, -- PK, FK
    publiID integer NOT NULL -------------------- PK, FK
);
ALTER TABLE metaPubli OWNER TO postgres;
ALTER TABLE ONLY metaPubli ADD CONSTRAINT metaPubli_pkey PRIMARY KEY (sampleName, publiID);


--
-- Name: metaWorker; Type: TABLE; Schema: public
-- OK

CREATE TABLE metaWorker (
    sampleName character varying(25) NOT NULL, -- PK, FK
    workerID integer NOT NULL, ------------------ PK, FK
    workerRole character varying(3) ------------- FK
);
ALTER TABLE metaWorker OWNER TO postgres;
ALTER TABLE ONLY metaWorker ADD CONSTRAINT metaWorker_pkey PRIMARY KEY (sampleName, workerID);


--
-- Name: climate; Type: TABLE; Schema: public
-- OK

CREATE TABLE climate (
    sampleName character varying(25) NOT NULL, -- PK, FK
    T_jan double precision,
    T_feb double precision,
    T_mar double precision,
    T_apr double precision,
    T_may double precision,
    T_jun double precision,
    T_jul double precision,
    T_aug double precision,
    T_sep double precision,
    T_oct double precision,
    T_nov double precision,
    T_dec double precision,
    T_djf double precision,
    T_mam double precision,
    T_jja double precision,
    T_son double precision,
    T_ann double precision,
    P_jan double precision,
    P_feb double precision,
    P_mar double precision,
    P_apr double precision,
    P_may double precision,
    P_jun double precision,
    P_jul double precision,
    P_aug double precision,
    P_sep double precision,
    P_oct double precision,
    P_nov double precision,
    P_dec double precision,
    P_djf double precision,
    P_mam double precision,
    P_jja double precision,
    P_son double precision,
    P_ann double precision
);
ALTER TABLE climate OWNER TO postgres;
ALTER TABLE ONLY climate ADD CONSTRAINT metaWorkerclimate_pkey PRIMARY KEY (sampleName);



-- FOREIGN KEYS
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_country_fk FOREIGN KEY (country) REFERENCES countries(country);
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_locationReliability_fk FOREIGN KEY (locationReliability) REFERENCES locationReliabilities(locationReliability);
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_sampleContext_fk FOREIGN KEY (sampleContext) REFERENCES sampleContexts(sampleContext);
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_sampleType_fk FOREIGN KEY (sampleType) REFERENCES sampleTypes(sampleType);
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_sampleMethod_fk FOREIGN KEY (sampleMethod) REFERENCES sampleMethods(sampleMethod);
ALTER TABLE ONLY metadata ADD CONSTRAINT metadata_ageUncertainty_fk FOREIGN KEY (ageUncertainty) REFERENCES ageUncertainties(ageUncertainty);

ALTER TABLE ONLY p_counts ADD CONSTRAINT p_counts_sampleName_fk FOREIGN KEY (sampleName) REFERENCES metadata(sampleName);
ALTER TABLE ONLY p_counts ADD CONSTRAINT p_counts_var__fk FOREIGN KEY (var_) REFERENCES p_vars(var_);

ALTER TABLE ONLY p_vars ADD CONSTRAINT p_vars_groupid_fk FOREIGN KEY (groupid) REFERENCES groupid(groupid);

ALTER TABLE ONLY metaPubli ADD CONSTRAINT metaPubli_sampleName_fk FOREIGN KEY (sampleName) REFERENCES metadata(sampleName);
ALTER TABLE ONLY metaPubli ADD CONSTRAINT metaPubli_publiID_fk FOREIGN KEY (publiID) REFERENCES publications(publiID);

ALTER TABLE ONLY metaWorker ADD CONSTRAINT metaWorker_sampleName_fk FOREIGN KEY (sampleName) REFERENCES metadata(sampleName);
ALTER TABLE ONLY metaWorker ADD CONSTRAINT metaWorker_workerID_fk FOREIGN KEY (workerID) REFERENCES workers(workerID);
ALTER TABLE ONLY metaWorker ADD CONSTRAINT metaWorker_workerRole_fk FOREIGN KEY (workerRole) REFERENCES workerRoles(workerRole);

ALTER TABLE ONLY climate ADD CONSTRAINT climates_sampleName_fk FOREIGN KEY (sampleName) REFERENCES metadata(sampleName);
ALTER TABLE ONLY ecosystems ADD CONSTRAINT ecosystems_sampleName_fk FOREIGN KEY (sampleName) REFERENCES metadata(sampleName);
