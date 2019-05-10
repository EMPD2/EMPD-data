# Module for fixing errors in the meta data
import requests
import os.path as osp
from itertools import starmap
import pandas as pd
import numpy as np
import pytest
from latlon_utils import get_climate


def get_elevation(points):
    query = ('https://api.open-elevation.com/api/v1/lookup?locations=' +
             '|'.join(starmap('{},{}'.format, points)))
    r = requests.get(query).json()
    # json object, various ways you can extract value
    # one approach is to use pandas json functionality:
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values
    return elevation


group_order = ['TRSH', 'PALM', 'MANG', 'LIAN', 'SUCC', 'HERB', 'VACR', 'AQUA']


@pytest.mark.formatfix
@pytest.mark.dbfix
def fix_trailing_spaces(full_meta, meta, meta_file, commit_fixes,
                        local_repo, skip_ci):
    for col in meta.columns:
        try:
            meta[col].str
        except AttributeError:
            pass
        else:
            meta[col] = meta[col].str.strip()
    changed = (meta.fillna('') !=
               full_meta.loc[meta.index.values].fillna('')).any(axis=1)
    if changed.any():
        message = "Removed trailing spaces for %i samples" % (
            changed.sum())
        print(message)
        full_meta.loc[meta.index.values, :] = meta
        full_meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]' if skip_ci else ''))
    else:
        print("No cells contained leading or trailing spaces")


@pytest.mark.formatfix
@pytest.mark.dbfix
def fix_newline_chars(full_meta, meta, meta_file, commit_fixes,
                      local_repo, skip_ci):
    for col in meta.columns:
        try:
            meta[col].str
        except AttributeError:
            pass
        else:
            meta[col] = meta[col].str.replace(
                '\n', ' ').str.replace('\r', ' ')
    changed = (meta.fillna('') !=
               full_meta.loc[meta.index.values].fillna('')).any(axis=1)
    if changed.any():
        message = "Removed newline characters for %i samples" % (
            changed.sum())
        print(message)
        full_meta.loc[meta.index.values, :] = meta
        full_meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]' if skip_ci else ''))
    else:
        print("No cells contained newline characters")


@pytest.mark.formatfix
@pytest.mark.dbfix
def fix_sample_data_formatting(data_files, groupids_table, commit_fixes,
                               meta, local_repo, skip_ci):

    ordered_groups = group_order + groupids_table.groupid.tolist() + \
        groupids_table.higher_groupid.tolist()
    if 'ispercent' not in meta.columns:
        meta = meta.copy()
        meta['ispercent'] = False
    for fname in data_files:
        counts = pd.read_csv(fname, '\t')
        samplename = osp.splitext(osp.basename(fname))[0]
        counts['samplename'] = samplename
        counts = counts[[c for c in counts.columns
                         if c == 'groupid' or c not in groupids_table]]
        counts = counts.merge(groupids_table, on='groupid', how='left')
        if not meta.loc[samplename, 'ispercent']:
            summed = counts[counts.used_in_sum]['count'].sum()
            counts['percentage'] = np.nan
            mask = counts.percent_values.values
            counts.loc[mask, 'percentage'] = (
                100. * counts.loc[mask, 'count'] / summed)

        # order the samples
        counts['order'] = counts.higher_groupid.apply(ordered_groups.index)
        counts.sort_values(['order', 'acc_varname'], inplace=True)

        notes = ['notes'] if 'notes' in counts.columns else []
        counts = counts[['samplename', 'original_varname', 'acc_varname',
                         'groupid', 'count', 'percentage'] + notes]
        counts.to_csv(fname, sep='\t', index=False, float_format='%1.8g')
    if commit_fixes:
        local_repo.index.add(['samples'])
        local_repo.index.commit(
            "Fixed formatting of samples data" + (
                '\n\n[skip ci]' if skip_ci else ''))


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_country(full_meta, meta, nat_earth_countries, meta_file,
                commit_fixes, local_repo, skip_ci, countries):

    def get_country(vals, default):
        return default if default in vals else vals[0]

    meta['Country'] = [
        (get_country(countries.loc[[new]].values, current) if new else current)
        for new, current in zip(nat_earth_countries.fillna('').values,
                                meta['Country'].values)]
    changed = (meta.fillna('') !=
               full_meta.loc[meta.index.values].fillna('')).any(axis=1)
    if changed.any():
        message = "Changed countries for %i samples" % (
            changed.sum())
        print(message)
        full_meta.loc[meta.index.values, :] = meta
        full_meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]' if skip_ci else ''))
    else:
        print("No wrong countries could be found")


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_elevation(full_meta, meta, meta_file, commit_fixes, local_repo,
                  skip_ci):
    try:
        samples = meta[meta.Elevation.isnull()].index.values
    except AttributeError:
        samples = meta.index.values
    if len(samples):
        message = "Set elevation for %s" % samples
        print(message)
        points = full_meta.loc[samples, ['Latitude', 'Longitude']].values
        elev = get_elevation(points)
        full_meta.loc[samples, 'Elevation'] = elev
        full_meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]' if skip_ci else ''))
    else:
        pytest.skip("All elevations already specified")


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_temperature(full_meta, meta, meta_file, commit_fixes, local_repo,
                    skip_ci):
    try:
        mask = meta.Temperature.isnull()
        mask |= meta.Temperature.astype(str).str.contains('nan')
    except AttributeError:
        mask = meta.index.astype(bool)
    mask &= (meta.Longitude.notnull() &
             meta.Latitude.notnull())
    samples = meta[mask].index.values
    if len(samples):
        message = "Set temperature from WorldClim v2 for %i" % len(samples)
        print(message)
        temperature = get_climate(
            *full_meta.loc[samples, ['Latitude', 'Longitude']].values.T,
            variables=['tavg'])
        full_meta.loc[samples, 'Temperature'] = temperature.to_csv(
            header=False, index=False, float_format='%1.8g').splitlines()
        full_meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]\n' if skip_ci else '\n\n') +
                ', '.join(samples))


@pytest.mark.metafix
@pytest.mark.dbfix
def fix_precipitation(full_meta, meta, meta_file, commit_fixes, local_repo,
                      skip_ci):
    try:
        mask = meta.Precipitation.isnull()
        mask |= meta.Precipitation.astype(str).str.contains('nan')
    except AttributeError:
        mask = meta.index.astype(bool)
    mask &= (meta.Longitude.notnull() &
             meta.Latitude.notnull())
    samples = meta[mask].index.values
    if len(samples):

        message = "Set precipitation from WorldClim v2 for %i" % len(samples)
        print(message)
        precip = get_climate(
            *full_meta.loc[samples, ['Latitude', 'Longitude']].values.T,
            variables=['prec'])
        # correct the data to make sure we have mm and not mm/month
        precip[-1] *= 12
        precip[-5:-1] *= 3
        full_meta.loc[samples, 'Precipitation'] = precip.to_csv(
            header=False, index=False, float_format='%1.8g').splitlines()
        full_meta.to_csv(str(meta_file), sep='\t', float_format='%1.8g')
        if commit_fixes:
            local_repo.index.add([meta_file.name])
            local_repo.index.commit(
                message + ('\n\n[skip ci]\n' if skip_ci else '\n\n') +
                ', '.join(samples))
