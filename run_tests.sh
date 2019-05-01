#!/bin/bash
cd /opt/empd-data

$PYTEST -v

start_pg_server
createdb -U postgres EMPD2
cd /opt/empd-data
psql EMPD2 -U postgres -f postgres/EMPD2.sql
python postgres/scripts/import_into_empd2.py meta.tsv -d ${DATABASE_URL}/EMPD2
