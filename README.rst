EMPD data
=========

This repository contains the data of the Eurasian Modern Pollen Database
(EMPD), published under the `Creative Commons Attribution 4.0 International license (CC-BY 4.0) <LICENSE>`_.

The data in this repository may be subject to changes. The last stable release can be found in the `Releases tab`_.

.. contents::
    **Contents**

Citing the EMPD
---------------

When using this data, please consider citing the corresponding publication:

	Davis, B.A.S., Zanon, M., Collins, P. et al., The European Modern Pollen Database (EMPD) project, Veget Hist Archaeobot (2013) 22: 521. https://doi.org/10.1007/s00334-012-0388-5
  
New publications for version 2 are in progress and will be listed here upon acceptance.


Contributing to the EMPD
------------------------
If you want to contribute to the EMPD – That's great!! Please refer to our `contributing guide <CONTRIBUTING.md>`_ for more information.


Accessing the data
------------------
The latest version of this data can be downloaded and accessed through the interactive viewer at EMPD2.github.io_ (see `EMPD2.github.io/data`_ for more information on this). The data is then the same as in the raw format mentioned below.

Otherwise you can access the EMPD data through this repository.

.. contents:: We provide the following formats
    :local:

Raw tab-delimited format: meta.tsv_
***********************************
- The meta data is stored as tab-delimited format in the `meta.tsv`_ file. See the `Column names <column-names>`_ below for further information
- The sample data is stored in the `samples`_ directory, one tab-delimited
  file per row in `meta.tsv`_. The filename is determined by the corresponding
  *SampleName* in the meta data.
  
  
Postgres dump: EMPD2.sql_
*************************
We provide a relational postgres dump for the EMPD2 in the `postgres/EMPD2.sql`__ file. If you are familiar with Postgres and have a postgres server running on your machine, you can import this data via::

  createdb EMPD2
  psql EMPD2 -f EMPD2.sql
  
Note that you can directly pipe from the raw github file into the database via curl::

  createdb EMPD2
  curl -fsSL https://raw.githubusercontent.com/EMPD2/EMPD-data/master/postgres/EMPD2.sql | psql EMPD2
  
or, if you want to use a specific version, e.g. ``v1.0``, use::

  curl -fsSL https://raw.githubusercontent.com/EMPD2/EMPD-data/v1.0/postgres/EMPD2.sql | psql EMPD2
  

Tab-delimited database: tab-delimited_
**************************************
A tab-delimited version of the postgres dump is also available in the tab-delimited_ folder.


.. _Releases tab: https://github.com/EMPD2/EMPD-data/releases/latest
.. _EMPD2.github.io: https://EMPD2.github.io?branch=master
.. _EMPD2.github.io/data: https://empd2.github.io/data.html
.. _meta.tsv: meta.tsv
.. _samples: samples
.. _EMPD2.sql: postgres/EMPD2.sql
.. _tab-delimited: tab-delimited

__ EMPD2.sql_

.. _column-names:

Column names in meta.tsv_
*************************

SampleName
    Unique identifier of the sample in the EMPD.
OriginalSampleName
    Original sample name as given by the author
SiteName
    Site or area name (given by author or else assigned) from where the sample/samples were taken.
Country
    EMPD country name (see worksheet 'Country' for list of countries)
Longitude
    Longitude (Decimal)
Latitude
    Latitude (Decimal)
Elevation
    Elevation (metres)
LocationReliability
    EMPD code assigned for location relaibility A, B, C , D, X

    A
    	Good for high resolution remote sensing (<100m), <100m
    B
        Good for lower resolution remote sensing (<1km), <1km
    C
        Ok for climate reconstruction or regional scale mapping, <5km
    D
        Ok for mapping at continental scale, <20km
    X
        Do not use!
LocationNotes
    Free text information about location
AreaOfSite
    Area of site (Hectares)
SampleContext
    EMPD code assigigned to describe environment from where the sample was taken
SiteDescription
    Free text description of the sample site
VegDescription
    Free text description of local or regional vegetation
SampleType
    EMPD code for the type of sample
SampleMethod
    EMPD code for the method used to collect the sample
AgeBP
    Age BP (before present) in years before (+) or after (-) AD 1950
AgeUncertainty
    EMPD code assigned for dating reliability A, B, C

    A
        Modern sample, 0BP to Present
    B
        Within last 100 years, 0-50BP
    C
        Within last 250 years, 50-200BP
Notes
    Free text for any further information
Publication1
    Publication relevant to the site/sample
Publication2
    Publication relevant to the site/sample
Publication3
    Publication relevant to the site/sample
Publication4
    Publication relevant to the site/sample
Publication5
    Publication relevant to the site/sample
Worker1_Role
    EMPD code that describes the workers role

    R
	    Responsible Person
    R/A
        Both Responsible Person and Analyst
    A
	    Analyst
    A/D
        Analyst (Deceased)
    A/I
        Analysis (Inactive)
    A/U
        Analyst (Unknown)
Worker1_LastName
    Last name or surname
Worker1_Initials
    Initials
Worker1_FirstName
    First name
Worker1_Address1
    Main postal address
Worker1_Address2
    Secondary postal address
Worker1_Email1
    Main email
Worker1_Email2
    Secondary email
Worker1_Phone1
    Main phone number
Worker1_Phone2
    Secondary phone number
Worker2_Role
    As above
Worker2_LastName
    As above
Worker2_Initials
    As above
Worker2_FirstName
    As above
Worker2_Address1
    As above
Worker2_Address2
    As above
Worker2_Email1
    As above
Worker2_Email2
    As above
Worker2_Phone1
    As above
Worker2_Phone2
    As above
Worker3_Role
	As above
Worker3_LastName
    As above
Worker3_Initials
    As above
Worker3_FirstName
    As above
Worker3_Address1
    As above
Worker3_Address2
    As above
Worker3_Email1
    As above
Worker3_Email2
    As above
Worker3_Phone1
    As above
Worker3_Phone2
    As above
Worker4_Role
    As above
Worker4_LastName
    As above
Worker4_Initials
	As above
Worker4_FirstName
    As above
Worker4_Address1
    As above
Worker4_Address2
    As above
Worker4_Email1
    As above
Worker4_Email2
    As above
Worker4_Phone1
    As above
Worker4_Phone2
    As above
okexcept
    Comma-delimited combination of the above fields. The EMPD tests failed on these columns for the given sample. Possible values in here are

    Country
        The Country of the *Latitude* and *Longitude* does not match with the NaturalEarth data (probably because it is close to a border)
    Latitude
        The latitudinal information is invalid
    Longitude
        The longitudinal information is invalid
    Temperature
        No temperature has been extracted for the given sample
    Precipitation
        No precipitation has been extracted for the given sample
    Elevation
        The sample has no elevation data
