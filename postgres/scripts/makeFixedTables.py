import sys
import os.path as osp
import psycopg2 as psql
import pandas as pd
import numpy as np

db_url = sys.argv[-1]

conn = psql.connect(db_url)
cursor = conn.cursor()


def is_null_str(x):
    return 'NULL' if x == "" else "'" + x.strip().replace("'", " ") + "'"


tables = osp.join(osp.dirname(__file__), "FixedTables.xlsx")


# ---
countries = pd.read_excel(tables, sheet_name="Country")
countries.replace(np.nan, '', inplace=True)

for x in range(countries.shape[0]):
    cursor.execute(
        "INSERT INTO countries (country) VALUES ('%s')" % countries.iloc[x][0])

conn.commit()


# ---
LocationReliability = pd.read_excel(tables, sheet_name="LocationReliability")
LocationReliability.replace(np.nan, '', inplace=True)

for x in range(LocationReliability.shape[0]):
    cursor.execute(
        "INSERT INTO LocationReliabilities "
        "(locationReliability, description, error) "
        "VALUES ('%s', '%s', %s)" % (
            LocationReliability.iloc[x][0], LocationReliability.iloc[x][1],
            is_null_str(LocationReliability.iloc[x][2])))

conn.commit()


# ---
sampleContext = pd.read_excel(tables, sheet_name="SampleContext")
sampleContext.replace(np.nan, '', inplace=True)

for x in range(sampleContext.shape[0]):
    cursor.execute(
        "INSERT INTO sampleContexts (sampleContext) VALUES ('%s')" % (
            sampleContext.iloc[x][0]))

conn.commit()


# ---
sampleType = pd.read_excel(tables, sheet_name="SampleType")
sampleType.replace(np.nan, '', inplace=True)

for x in range(sampleType.shape[0]):
    cursor.execute(
        "INSERT INTO sampleTypes (sampleType, notes) "
        "VALUES ('%s', %s)" % (sampleType.iloc[x][0],
                               is_null_str(sampleType.iloc[x][1])))

conn.commit()


# ---
SampleMethod = pd.read_excel(tables, sheet_name="SampleMethod")
SampleMethod.replace(np.nan, '', inplace=True)

for x in range(SampleMethod.shape[0]):
    cursor.execute(
        "INSERT INTO sampleMethods (sampleMethod) VALUES ('%s')" % (
            SampleMethod.iloc[x][0]))

conn.commit()


# ---
ageUncertainties = pd.read_excel(tables, sheet_name="AgeUncertainty")
ageUncertainties.replace(np.nan, '', inplace=True)

for x in range(ageUncertainties.shape[0]):
    cursor.execute(
        "INSERT INTO ageUncertainties (ageUncertainty, description, age) "
        "VALUES ('%s', '%s', '%s')" % (
            ageUncertainties.iloc[x][0], ageUncertainties.iloc[x][1],
            ageUncertainties.iloc[x][2]))

conn.commit()


# ---
workerRoles = pd.read_excel(tables, sheet_name="WorkerRole")
workerRoles.replace(np.nan, '', inplace=True)

for x in range(workerRoles.shape[0]):
    cursor.execute(
        "INSERT INTO workerRoles (workerRole, description) VALUES "
        "('%s', '%s')" % (workerRoles.iloc[x][0], workerRoles.iloc[x][1]))

conn.commit()


# ---
groupIDs = pd.read_excel(tables, sheet_name="GroupID")
groupIDs.replace(np.nan, '', inplace=True)

for x in range(groupIDs.shape[0]):
    cursor.execute(
        "INSERT INTO groupID (groupID, groupname, higher_groupid) VALUES "
        "(%s, %s, %s)" % (
            is_null_str(groupIDs.iloc[x][0]), is_null_str(groupIDs.iloc[x][1]),
            is_null_str(groupIDs.iloc[x][2])))

conn.commit()


conn.close()