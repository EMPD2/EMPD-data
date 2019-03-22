"""Import new data into the EMPD2"""
import psycopg2 as psql
import pandas as pd
import numpy as np
import os
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'meta', help="The path to the meta file. Default: %(default)s", nargs='?',
    default=os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'meta.tsv')))
parser.add_argument(
    '-db', '--database-url', default=os.getenv('DATABASE_URL'),
    help="The url to connect to the database. Default: %(default)s")

args = parser.parse_args()

meta = args.meta
db_url = args.database_url

samples_dir = os.path.join(os.path.dirname(meta), 'samples')
base_meta = os.path.join(os.path.dirname(meta), 'meta.tsv')

conn = psql.connect(db_url)
cursor = conn.cursor()


def is_null_str(x):
    return 'NULL' if x == "" else "'" + x.strip().replace("'", " ").replace(
        '\n', ' ').replace('\r', ' ')+"'"


def is_null_nb(x, nodata=np.nan):
    return 'NULL' if x == nodata else str(round(x, 2))


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


# script for returning elevation from lat, long, based on open elevation data
# which in turn is based on SRTM
def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    # json object, various ways you can extract value
    r = requests.get(query).json()
    # one approach is to use pandas json functionality:
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
    return elevation


def clean_doi(doi):
    DOI = doi.replace('https://doi.org/', '')
    DOI = DOI.replace('http://dx.doi.org/', '')
    DOI = DOI.replace('doi: ', '')
    DOI = DOI.replace('doi.org/', '')
    DOI = DOI.replace('DOI: ', '')
    DOI = DOI.replace('DOI ', '')
    DOI = DOI.replace('doi:', '')
    DOI = DOI.replace(' ', '')
    DOI = DOI.replace('https://link.springer.com/article/', '')
    return DOI


PUBLI_ID = 1   # TODO: Has to be set from EMPD2
WORKER_ID = 1  # TODO: Has to be set from EMPD2

err = 0
list_of_errors = []
missing_elevation = {}


METADATA = pd.read_csv(meta, sep='\t')
base_meta = METADATA
for col in set(base_meta.columns) - set(METADATA.columns):
    METADATA[col] = ''

METADATA.replace(np.nan, '', inplace=True)
PUBLI = METADATA[['Publication1', 'DOI1']]
tmp = METADATA[['Publication2', 'DOI2']]
tmp.columns = list(PUBLI.columns)
PUBLI = PUBLI.append(tmp, ignore_index=True)
tmp = METADATA[['Publication3', 'DOI3']]
tmp.columns = list(PUBLI.columns)
PUBLI = PUBLI.append(tmp, ignore_index=True)
tmp = METADATA[['Publication4', 'DOI4']]
tmp.columns = list(PUBLI.columns)
PUBLI = PUBLI.append(tmp, ignore_index=True)
tmp = METADATA[['Publication5', 'DOI5']]
tmp.columns = list(PUBLI.columns)
PUBLI = PUBLI.append(tmp, ignore_index=True)
PUBLI = PUBLI.drop_duplicates()

# -----
for x in range(PUBLI.shape[0]):
    duplicate_doi = 0
    if PUBLI.iloc[x][1] != '':
        duplicate_doi = PUBLI.query('DOI1 == %s' % is_null_str(
            PUBLI.iloc[x][1])).shape[0]
        if duplicate_doi > 1:
            print(PUBLI.query('DOI1 == %s' % is_null_str(PUBLI.iloc[x][1])))
            print('DOI %s duplicated %d times.' % (PUBLI.iloc[x][1],
                                                   duplicate_doi))
    if PUBLI.iloc[x][0] != '' and duplicate_doi <= 1:
        DOI = clean_doi(PUBLI.iloc[x][1])
        cursor.execute(
            "SELECT * FROM publications WHERE (DOI IS NULL OR DOI=%s) AND "
            "(reference =%s)" % (is_null_str(DOI),
                                 is_null_str(PUBLI.iloc[x][0])))
        res = cursor.fetchall()
        if len(res) == 0:
            try:
                cursor.execute(
                    "INSERT INTO publications (publiID, DOI, reference) "
                    "VALUES (%d, %s, %s)" % (PUBLI_ID, is_null_str(DOI),
                                             is_null_str(PUBLI.iloc[x][0])))
                conn.commit()
            except Exception:
                print(
                    "ERROR: "
                    "INSERT INTO publications (publiID, DOI, reference) "
                    "VALUES (%d, %s, %s)" % (PUBLI_ID, is_null_str(DOI),
                                             is_null_str(PUBLI.iloc[x][0])))
                conn = psql.connect(db_url)
                cursor = conn.cursor()
            PUBLI_ID += 1
        else:
            pass
    elif PUBLI.iloc[x][1] != '' and duplicate_doi <= 1:
        print('Empty paper description for DOI %s' % PUBLI.iloc[x][1])
# ---
# ---
# ---
_worker_attrs = ['FirstName', 'Initials', 'LastName', 'Address1', 'Email1',
                 'Phone1', 'Address2', 'Email2', 'Phone2']
WORKERS = METADATA[list('Worker1_' + a for a in _worker_attrs)]

tmp = METADATA[list('Worker2_' + a for a in _worker_attrs)]
tmp.columns = list(WORKERS.columns)
WORKERS = WORKERS.append(tmp, ignore_index=True)

tmp = METADATA[list('Worker3_' + a for a in _worker_attrs)]
tmp.columns = list(WORKERS.columns)
WORKERS = WORKERS.append(tmp, ignore_index=True)

tmp = METADATA[list('Worker4_' + a for a in _worker_attrs)]
tmp.columns = list(WORKERS.columns)

WORKERS = WORKERS.append(tmp, ignore_index=True)
WORKERS = WORKERS.drop_duplicates()
WORKERS.replace('', np.nan, inplace=True)
WORKERS = WORKERS.dropna(axis='index', how='all')
WORKERS.replace(np.nan, '', inplace=True)

# ---
# ---
# ---
for x in range(WORKERS.shape[0]):
    cursor.execute(
        "SELECT * FROM Workers WHERE "
        "(firstname IS NULL OR firstName=%s) AND "
        "(initials ISNULL OR initials=%s) AND "
        "(lastname ISNULL OR lastName=%s) AND "
        "(address1 ISNULL OR address1=%s) AND "
        "(email1 ISNULL OR email1=%s) AND "
        "(phone1 ISNULL OR phone1=%s) AND "
        "(address2 ISNULL OR address2=%s) AND "
        "(email2 ISNULL OR email2=%s) AND "
        "(phone2 ISNULL OR phone2=%s)" % (
            is_null_str(WORKERS.iloc[x][0]), is_null_str(WORKERS.iloc[x][1]),
            is_null_str(WORKERS.iloc[x][2]), is_null_str(WORKERS.iloc[x][3]),
            is_null_str(WORKERS.iloc[x][4]),
            is_null_str(str(WORKERS.iloc[x][5])),
            is_null_str(WORKERS.iloc[x][6]), is_null_str(WORKERS.iloc[x][7]),
            is_null_str(str(WORKERS.iloc[x][8]))))
    res = cursor.fetchall()
    if len(res) == 0:
        cursor.execute(
            "INSERT INTO Workers "
            "(workerID, firstName, initials, lastName, "
            " address1, email1, phone1, address2, email2, phone2) VALUES "
            "(%d, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
                WORKER_ID, is_null_str(WORKERS.iloc[x][0]),
                is_null_str(WORKERS.iloc[x][1]),
                is_null_str(WORKERS.iloc[x][2]),
                is_null_str(WORKERS.iloc[x][3]),
                is_null_str(WORKERS.iloc[x][4]),
                is_null_str(str(WORKERS.iloc[x][5])),
                is_null_str(WORKERS.iloc[x][6]),
                is_null_str(WORKERS.iloc[x][7]),
                is_null_str(str(WORKERS.iloc[x][8]))))
        conn.commit()
        WORKER_ID += 1
    else:
        pass
# ---
# ---
# ---
for x in range(METADATA.shape[0]):
    elevation = METADATA.iloc[x][6]
    elev_notes = str(METADATA.iloc[x][8])
    if elevation == '':
        if elev_notes == '':
            elev_notes = ('Elevation estimated from Google Earth from the '
                          'coordinates.')
        else:
            elev_notes += ('; Elevation estimated from Google Earth from the '
                           'coordinates')
        if METADATA.iloc[x][0] in missing_elevation.keys():
            elevation = missing_elevation[METADATA.iloc[x][0]]
        else:
            try:
                print(METADATA.iloc[x]['SampleName'])
                elevation = get_elevation(METADATA.iloc[x]['Latitude'],
                                          METADATA.iloc[x]['Longitude'])
                f_missing_elev = open("missing_elevation.csv", "a")
                f_missing_elev.write(
                    METADATA.iloc[x][0] + "," + str(elevation) + "\n")
                f_missing_elev.close()
            except Exception:
                elevation = -9999
    try:
        cursor.execute(
            "INSERT INTO metadata "
            "(sampleName, originalSampleName, siteName, country, longitude, "
            " latitude, elevation, locationReliability, locationNotes, "
            " areaOfSite, sampleContext, siteDescription, vegDescription, "
            " sampleType, sampleMethod, ageBP, ageUncertainty, notes, "
            " empd_version) VALUES "
            "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            " %s, %s, 'EMPD2')" % (
                is_null_str(METADATA.iloc[x]['SampleName']),
                is_null_str(str(METADATA.iloc[x]['OriginalSampleName'])),
                is_null_str(str(METADATA.iloc[x]['SiteName'])),
                is_null_str(METADATA.iloc[x]['Country']),
                is_null_str(str(METADATA.iloc[x]['Longitude'])),
                is_null_str(str(METADATA.iloc[x]['Latitude'])),
                is_null_str(str(elevation)),
                is_null_str(METADATA.iloc[x]['LocationReliability']),
                is_null_str(elev_notes),
                is_null_str(str(METADATA.iloc[x]['AreaOfSite'])),
                is_null_str(METADATA.iloc[x]['SampleContext'].lower()),
                is_null_str(METADATA.iloc[x]['SiteDescription']),
                is_null_str(METADATA.iloc[x]['VegDescription']),
                is_null_str(METADATA.iloc[x][
                    'SampleType'].split(' (to be ')[0].lower()),
                is_null_str(METADATA.iloc[x]['SampleMethod'].lower()),
                is_null_str(str(METADATA.iloc[x]['AgeBP'])),
                is_null_str(METADATA.iloc[x]['AgeUncertainty']),
                is_null_str(METADATA.iloc[x]['Notes'])))
        conn.commit()
    except psql.IntegrityError as e:
        conn = psql.connect(db_url)
        cursor = conn.cursor()
        if str(e) not in list_of_errors:
            list_of_errors.append(str(e))
        print('IntegrityError ', x, e)
        err += 1
    except psql.DataError as e:
        if str(e) not in list_of_errors:
            list_of_errors.append(str(e))
        print('DataError ', x, e)
        conn = psql.connect(db_url)
        cursor = conn.cursor()
        err += 1
    except AttributeError as e:
        if str(e) not in list_of_errors:
            list_of_errors.append(str(e))
        print('AttributeError ', x, e)
        conn = psql.connect(db_url)
        cursor = conn.cursor()
        err += 1
    except Exception as e:
        if str(e) not in list_of_errors:
            list_of_errors.append(str(e))
        print('Error ', x, e)
        conn = psql.connect(db_url)
        cursor = conn.cursor()
        err += 1

    temperature = METADATA.iloc[x]['Temperature']
    precip = METADATA.iloc[x]['Precipitation']
#    try:
    temperature = temperature or ','.join(['NULL'] * 17)
    precip = precip or ','.join(['NULL'] * 17)

    cursor.execute(
        "INSERT INTO climate VALUES (%s,%s,%s)" % (
            is_null_str(METADATA.iloc[x]['SampleName']), temperature, precip))
    conn.commit()

    for _worker in map('Worker{}_'.format, '1234'):
        if METADATA.iloc[x][_worker + 'LastName'] != '':
            cursor.execute(
                "SELECT workerID from workers WHERE lastname= '%s' AND "
                "(firstname ISNULL or firstname='%s')" % (
                    METADATA.iloc[x][_worker + 'LastName'].strip(),
                    METADATA.iloc[x][_worker + 'FirstName'].strip()))
            workerID = cursor.fetchall()[0][0]
            cursor.execute(
                "INSERT INTO metaworker (sampleName, workerID, workerRole) "
                "VALUES (%s, %d, %s)" % (
                    is_null_str(METADATA.iloc[x]['SampleName']), workerID,
                    is_null_str(METADATA.iloc[x][_worker + 'Role'])))
            conn.commit()
    for i in '1234':
        _pub = 'Publication' + i
        _doi = 'DOI' + i
        if METADATA.iloc[x][_pub] != '':
            cursor.execute(
                "SELECT publiID from publications WHERE reference= %s AND "
                "(DOI ISNULL or DOI='%s')" % (
                    is_null_str(METADATA.iloc[x][_pub]),
                    clean_doi(METADATA.iloc[x][_doi])))
            publiID = cursor.fetchall()[0][0]
            cursor.execute(
                "INSERT INTO metapubli (sampleName, publiID) VALUES "
                "(%s, %d)" % (is_null_str(METADATA.iloc[x]['SampleName']),
                              publiID))
            conn.commit()

cursor.execute("SELECT MAX(var_) FROM p_vars")
res = cursor.fetchall()
TAXON_ID = (res[0][0] or 0) + 1

for samplename in METADATA.SampleName:
    COUNTS = pd.read_csv(os.path.join(samples_dir, samplename + '.tsv'),
                         sep='\t')
    for x, row in COUNTS.iterrows():
        ACCVARNAME = row.acc_varname
        ORIVARNAME = row.original_varname
        GROUPID = row.groupid  # should take EPD or Neotoma groupids here!
        NOTES = ''
        cursor.execute(
            "SELECT var_ FROM p_vars WHERE original_varname='%s' AND "
            "acc_varname='%s' AND (groupID ISNULL OR groupID='%s')" % (
                ORIVARNAME, ACCVARNAME, GROUPID))
        res = cursor.fetchall()
        if len(res) == 0:
            cursor.execute(
                "INSERT INTO p_vars "
                "(var_, acc_var_, acc_varname, original_varname, groupID, "
                " notes) VALUES (%d, NULL, '%s', '%s', '%s', '%s')" % (
                    TAXON_ID, ACCVARNAME, ORIVARNAME, GROUPID,
                    is_null_str(NOTES)))
            VAR_ = TAXON_ID
            TAXON_ID += 1
            conn.commit()
        else:
            VAR_ = res[0][0]
            samplename = row.samplename
            try:
                if row['count'] > 0:
                    val = round(row['count'])
                    try:
                        cursor.execute(
                            "INSERT INTO p_counts (sampleName, var_, count) "
                            "VALUES ('%s', %d, %d)" % (
                                samplename, VAR_, val))
                        conn.commit()
                    except psql.IntegrityError as e:
                        conn = psql.connect(db_url)
                        cursor = conn.cursor()
                        if 'duplicate key value violates unique constraint "p_counts_pkey"' in str(e):
                            cursor.execute(
                                "SELECT count FROM p_counts WHERE "
                                "sampleName = '%s' AND var_ = %d" % (
                                    samplename, VAR_))
                            new_val = cursor.fetchall()[0][0] + val
                            cursor.execute(
                                "UPDATE p_counts SET count=%d WHERE "
                                "sampleName = '%s' AND var_ = %d" % (
                                    new_val, samplename, VAR_))
                            conn.commit()
            except Exception:
                print(samplename, VAR_, "!" + str(row['count']) + "!")