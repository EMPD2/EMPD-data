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


@pytest.mark.dbfix
def fix_country(meta, meta_row, meta_file):
    country = get_country(meta_row.Latitude, meta_row.Longitude)
    current = getattr(meta_row, 'Country', '')
    if country != current:
        print("Changing country from %s to %s" % (current, country))
        meta.loc[meta_row.name, 'Country'] = country
        meta.to_csv(str(meta_file), sep='\t')


@pytest.mark.dbfix
def fix_elevation(meta, meta_file):
    try:
        samples = meta[meta.Elevation.isnull()].index.values
    except AttributeError:
        samples = meta.index.values
    if len(samples):
        print("Getting elevation for %s" % samples)
        points = meta.loc[samples, ['Latitude', 'Longitude']].values
        elev = get_elevation(points)
        meta.loc[samples, 'Elevation'] = elev
        meta.to_csv(str(meta_file), sep='\t')
    else:
        pytest.skip("All elevations already specified")


@pytest.mark.dbfix
def fix_temperature(meta, meta_file):
    try:
        samples = meta[meta.Temperature.isnull()].index.values
    except AttributeError:
        samples = meta.index.values
    if len(samples):
        print("Getting temperature from WorldClim v2 for %s" % samples)
        temperature = get_climate(
            *meta.loc[samples, ['Latitude', 'Longitude']].values.T,
            variables=['tavg'])
        meta.loc[samples, 'Temperature'] = list(map(
            ','.join, temperature.values.astype(str)))
        meta.to_csv(str(meta_file), sep='\t')


@pytest.mark.dbfix
def fix_precipitation(meta, meta_file):
    try:
        samples = meta[meta.Precipitation.isnull()].index.values
    except AttributeError:
        samples = meta.index.values
    if len(samples):
        print("Getting temperature from WorldClim v2 for %s" % samples)
        precip = get_climate(
            *meta.loc[samples, ['Latitude', 'Longitude']].values.T,
            variables=['prec'])
        meta.loc[samples, 'Precipitation'] = list(map(
            ','.join, precip.values.astype(str)))
        meta.to_csv(str(meta_file), sep='\t')
