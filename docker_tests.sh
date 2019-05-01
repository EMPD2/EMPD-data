#!/bin/bash
# Syntax:
#
#     test-empd-data [meta.tsv]

set -ex

cd /opt/empd-data

if [[ $1 ]]; then METAFILE=$1; else METAFILE=meta.tsv; fi

# activate conda
. "/opt/conda/etc/profile.d/conda.sh"
conda activate empd-admin

pytest -v --empd-meta=$METAFILE

start_pg_server
createdb -U postgres EMPD2
cd /opt/empd-data
psql EMPD2 -U postgres -f postgres/EMPD2.sql
python postgres/scripts/import_into_empd2.py $METAFILE -d ${DATABASE_URL}/EMPD2
