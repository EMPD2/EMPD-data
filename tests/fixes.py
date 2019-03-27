# Module for fixing errors in the meta data
from latlon_utils import get_country, get_climate
import requests
from itertools import starmap
import pandas as pd
import pytest


def get_elevation(points):
    query = ('https://api.open-elevation.com/api/v1/lookup?locations=' +
             '|'.join(starmap('{},{}'.format, points)))
    r = requests.get(query).json()
    # json object, various ways you can extract value
    # one approach is to use pandas json functionality:
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values
    return elevation


@pytest.mark.formatfix
@pytest.mark.dbfix
def fix_trailing_spaces(meta, meta_row, meta_file, commit_fixes, local_repo,
                        skip_ci):
    meta_row = meta_row.astype(str)
    stripped = meta_row.str.strip()
    cols = meta_row[stripped != meta_row].index
    if len(cols):
        message = "Removed trailing spaces for %s" % (cols, )
        print(message)
        meta.loc[meta_row.name, cols] = stripped[cols]
        meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                ("[%s]: %s" % (meta_row.name, message)) +
                ('\n\n[skip ci]' if skip_ci else ''))


@pytest.mark.formatfix
@pytest.mark.dbfix
def fix_newline_chars(meta, meta_row, meta_file, commit_fixes, local_repo,
                      skip_ci):
    meta_row = meta_row.astype(str)
    stripped = meta_row.str.replace('\n', ' ').str.replace('\r', ' ')
    cols = meta_row[stripped != meta_row].index
    if len(cols):
        message = "Removed newline characters for %s" % (cols, )
        print(message)
        meta.loc[meta_row.name, cols] = stripped[cols]
        meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                ("[%s]: %s" % (meta_row.name, message)) +
                ('\n\n[skip ci]' if skip_ci else ''))


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_country(meta, meta_row, meta_file, commit_fixes, local_repo,
                skip_ci, countries):
    country = get_country(meta_row.Latitude, meta_row.Longitude)
    try:
        country = countries.loc[country]
    except KeyError:
        pass
    current = getattr(meta_row, 'Country', '')
    if country != current:
        message = "Changed country from %s to %s" % (current, country)
        print(message)
        meta.loc[meta_row.name, 'Country'] = country
        meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                ("[%s]: %s" % (meta_row.name, message)) +
                ('\n\n[skip ci]' if skip_ci else ''))


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_elevation(meta, meta_file, commit_fixes, local_repo, skip_ci):
    try:
        samples = meta[meta.Elevation.isnull()].index.values
    except AttributeError:
        samples = meta.index.values
    if len(samples):
        message = "Set elevation for %s" % samples
        print(message)
        points = meta.loc[samples, ['Latitude', 'Longitude']].values
        elev = get_elevation(points)
        meta.loc[samples, 'Elevation'] = elev
        meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]' if skip_ci else ''))
    else:
        pytest.skip("All elevations already specified")


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_temperature(meta, meta_file, commit_fixes, local_repo, skip_ci):
    try:
        mask = meta.Temperature.isnull()
        mask |= meta.Temperature.astype(str).str.contains('nan')
    except AttributeError:
        mask = meta.index.astype(bool)
    mask &= meta.Longitude.notnull() & meta.Latitude.notnull()
    samples = meta[mask].index.values
    if len(samples):
        message = "Set temperature from WorldClim v2 for %i" % len(samples)
        print(message)
        temperature = get_climate(
            *meta.loc[samples, ['Latitude', 'Longitude']].values.T,
            variables=['tavg'])
        meta.loc[samples, 'Temperature'] = temperature.to_csv(
            header=False, index=False, float_format='%1.8g').splitlines()
        meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]\n' if skip_ci else '\n\n') +
                ', '.join(samples))


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_precipitation(meta, meta_file, commit_fixes, local_repo, skip_ci):
    try:
        mask = meta.Precipitation.isnull()
        mask |= meta.Precipitation.astype(str).str.contains('nan')
    except AttributeError:
        mask = meta.index.astype(bool)
    mask &= meta.Longitude.notnull() & meta.Latitude.notnull()
    samples = meta[mask].index.values
    if len(samples):

        message = "Set precipitation from WorldClim v2 for %i" % len(samples)
        print(message)
        precip = get_climate(
            *meta.loc[samples, ['Latitude', 'Longitude']].values.T,
            variables=['prec'])
        meta.loc[samples, 'Precipitation'] = precip.to_csv(
            header=False, index=False, float_format='%1.8g').splitlines()
        meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]\n' if skip_ci else '\n\n') +
                ', '.join(samples))
