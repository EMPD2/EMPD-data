---
title: 'Open Data Web Management Tools for the Eurasian Modern Pollen Database (EMPD) version 2'
tags:
    - palynology
    - pollen
    - earth science
    - climate
    - paleao
    - webapp
    - github
    - open data
    - open science
    - python
authors:
    - name: Philipp S. Sommer
      orcid: 0000-0001-6171-7716
      affiliation: 1
    - name: Manuel Chevalier
      orcid: 0000-0002-8183-9881
      affiliation: 1
    - name: Basil A. S. Davis
      orcid: 0000-0002-7148-1863
      affiliation: 1
affiliations:
    - name: Institute of Earth Surface Dynamics, University of Lausanne, Géopolis, 1015 Lausanne, Switzerland
      index: 1
date: 13 May 2019
bibliography: paper.bib
---

# Summary

The European Modern Pollen Database (EMPD), version 1, established in 2013 by
@DavisEtAl2013, is a fully documented and quality-controlled dataset of modern
pollen samples. Recent efforts by more than 60 data contributors almost doubled
the number of samples in the database and increased it's spatial domain, such
that it is now released as the Eurasian Modern Pollen Database, version 2
(Davis et. al, in prep.) with around 8000 samples.

The EMPD is the only public and openly accessible database of modern pollen
data in the Eurasian continent and is entirely driven by the community of it's
data contributors. This effort of creating an open and accessible database led
to the development of new open source data management tools to simplify and
reveal the management of multiple contributions from different sources and
people. The EMPD2 is now hosted on the version control platform Github at
[github.com/EMPD2](https://github.com/EMPD2) with a
dedicated web viewer at [EMPD2.github.io](https://EMPD2.github.io) and a
automated administration app, the EMPD-admin.

# The EMPD web framework
In favor of open science, the hosting on Github allows a fully transparent and
comprehensible development of the database, without the need of additional
funding for  dedicated web services. The implementation on Github additionally
provides the advantage of continuous integration services, such as Travis CI
([travis-ci.org](https://travis-ci.org/)) and DockerHub
([hub.docker.com](https://hub.docker.com/)) to further process and distribute
the database. The following sections describe the different tools and
integrations in more detail.

## The EMPD viewer
The main interface into the EMPD is an interactive web viewer accessible via
[EMPD2.github.io](https://EMPD2.github.io). This JavaScript-based application
provides an interface into the database in an informative way without
requiring any particular computer expertise. It enables the user to view the
data on a map and select and download subsets of the database. The webpage
involves no server-side processing and such it can be hosted for free using on
Github allowing stability, independent on the availability of funding. This
also allows a local use the viewer with data in a local repository, without the
need for further installations of dependencies.

Being inspired by the open source climate proxies finder (@BollietEtAl2016,
@ClimateProxiesFinder), it is mainly based on the dc (@ZhuEtAl2019),
crossfilter (@SqareIncEtAl2019) and leaflet (@AgafonkinEtAl2019) open source
JavaScript libraries. This allows a quick and efficient filtering of the
database. The viewer is fully integrated into the Github framework of the EMPD
and loads the displayed data from the online repository. As such, it also
provides a further quality control check and allows the data contributors to
review and edit their contributions before they are merged into the database,
and to raise issues without the need to have an own Github account.

## The EMPD2 data repository
The raw data of the EMPD2 is accessible as plain text files in a Github
repository. This allows a transparent traceback of changes made to the EMPD via
version control and it allows the EMPD viewer to interface into the database
(see previous section). In an automated post-processing, and as an
additional check of the database, we also provide a relational postgres dump
that is automatically generated based on the plain text files. Meta data tests
and a combination with the continuous integration service of Travis CI,
standard tools for open source software development, allow a continuous check
of the community-based database and facilitates the implementation of new
contributions. The management and testing of new contributions through pull
requests on Github contributions additionally enables the integration with the
automated administration web app EMPD-admin (see next section).

## The EMPD-admin
To facilitate the check of new contributions to the EMPD, we developed the
EMPD-admin webapp. Inspired by the web management tools of the conda-forge
community (@conda-forge2019), this tool provides an automated handling of data
contributions from within Github Pull Requests, including testing, fixing
and querying the submission. An additional integration with the EMPD viewer
(see previous section) allows the interactive editing of data contributions and
the reporting of issues through the web interface.

The EMPD-admin webapp is hosted for free at Heroku (https://www.heroku.com)
at [empd-admin.herokuapp.com](https://empd-admin.herokuapp.com/).
This, again, allows stability independent on the availability of funding. It's
core functionality can, however, also be installed locally and used from the
command-line, independent of Github and Heroku.

The Python library is based on  the tornado web framework
[www.tornadoweb.org](https://www.tornadoweb.org/en/stable/), as well as pandas
(@McKinneyEtAl2010), a tabular data analysis library for Python, and
sqlalchemy (@Bayer2012), a Python SQL toolkit. Additional to the installation


# Accessibility
The EMPD is hosted within the EMPD2 Github organization
(https://github.com/EMPD2) at https://github.com/EMPD2/EMPD-data. The source
files of the viewer are accessible at https://github.com/EMPD2/EMPD2.github.io
and for the EMPD-admin at https://github.com/EMPD2/EMPD-admin.

The EMPD data and the EMPD-admin are additionally both available as Docker
images at https://hub.docker.com/u/empd2 and can be accessed via

```bash
docker pull empd2/empd-data
docker pull empd2/empd-admin
```

The EMPD-admin can also be installed through the python package manager `pip`
via

```bash
pip install EMPD-admin
```


# Acknowledgements

We gratefully acknowledge funding by the Swiss National Science Foundation
(SNF) through the HORNET project (200021_169598).

# References
