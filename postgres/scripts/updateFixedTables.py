import sys
import os.path as osp
import psycopg2 as psql
import pandas as pd
import numpy as np
from functools import partial

db_url = sys.argv[1]
to_update = sys.argv[2:]

conn = psql.connect(db_url)
cursor = conn.cursor()


def is_null_str(x):
    return 'NULL' if x == "" else "'" + x.strip().replace("'", " ") + "'"


tables = osp.join(osp.dirname(__file__), "tables", '')

read_tsv = partial(pd.read_csv, sep='\t')

# ---
if 'Country' in to_update or 'all' in to_update:
    countries = read_tsv(tables + "Country.tsv")
    countries.replace(np.nan, '', inplace=True)

    for x in range(countries.shape[0]):
        cursor.execute(
            "UPDATE countries SET natural_earth = %s WHERE country = '%s'" % (
                is_null_str(countries.iloc[x][1]), countries.iloc[x][0]))

    conn.commit()


# ---
if 'SampleType' in to_update or 'all' in to_update:
    sampleType = read_tsv(tables + "SampleType.tsv")
    sampleType.replace(np.nan, '', inplace=True)

    for x in range(sampleType.shape[0]):
        cursor.execute(
            "UPDATE sampleTypes SET notes = %s WHERE sampleType = '%s'" % (
                is_null_str(sampleType.iloc[x][1]), sampleType.iloc[x][0]))

    conn.commit()


conn.close()
