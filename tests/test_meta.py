# Test functions for the meta data
import os.path as osp
import glob
import pytest
from itertools import starmap
import numpy as np
from difflib import get_close_matches
import textwrap


def okexcept(meta_row, col):
    okexcept = getattr(meta_row, 'okexcept', [])
    try:
        return col in okexcept
    except TypeError:
        return False


def notnull(val):
    return not isnull(val)


def isnull(val):
    val = str(val)
    return val == '' or val == 'nan' or val == 'None'


# ---- meta.tsv tests


def test_meta_exists(samples_dir, meta, base_meta):
    files = glob.glob(osp.join(samples_dir, '*.tsv'))
    samples = map(lambda f: osp.splitext(osp.basename(f))[0], files)
    missing = set(samples).difference(base_meta.index).difference(meta.index)
    assert not missing, f"Missing meta information for samples {missing}"


def test_lat_lon(meta, okexcept, record_property):
    meta = meta.copy()
    meta = meta.join(okexcept('Latitude'))
    meta['Latitude_ok'] = (meta.Latitude >= -90) & (meta.Latitude <= 90)
    meta = meta.join(okexcept('Longitude'))
    meta['Longitude_ok'] = (meta.Longitude >= -180) & (meta.Longitude <= 360)
    failed = meta[~(meta.iloc[:, -4] | meta.iloc[:, -3]) |
                  ~(meta.iloc[:, -2] | meta.iloc[:, -1])]
    record_property('failed_samples',
                    failed[['Latitude', 'Longitude'] + list(meta.columns[-4:])]
                    )
    msg = "Found %i invalid Latitude-Longitude pairs: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_country(meta, countries, nat_earth_countries, okexcept,
                 record_property):
    ref = countries
    meta = meta.copy()
    s = meta['Country'].fillna('')

    s_ok = okexcept(s.name)
    s_ok |= (okexcept("Latitude") & okexcept("Longitude")).values
    meta = meta.join(s_ok)
    meta['nat_earth'] = nat_earth_countries
    meta['empd_countries'] = [
        '; '.join(ref.loc[[n]]) if n in ref.index else c
        for c, n in meta[[s.name, 'nat_earth']].values]
    meta[s.name + '_ok'] = [n in ref.index and c in ref.loc[[n]].values
                            for c, n in meta[[s.name, 'nat_earth']].values]
    failed = meta[~(s_ok | meta.Country_ok)]
    if len(failed):
        record_property('failed_samples',
                        failed[[s.name, 'nat_earth', 'empd_countries', s_ok.name,
                                s.name + '_ok']]
                        )
    msg = "Found %i invalid %s: %s" % (
        len(failed), s.name if len(failed) == 1 else 'Countries',
        textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_samplecontext(meta, samplecontexts, okexcept, record_property):
    if 'SampleContext' not in meta.columns:
        return pytest.skip("No SampleContext specified.")
    ref = samplecontexts
    meta = meta.copy()
    s = meta['SampleContext'].fillna('')

    s_ok = okexcept(s.name)
    meta = meta.join(s_ok)
    meta[s.name + '_ok'] = (~s.astype(bool)) | np.isin(s, ref)
    meta[s.name + '_lower'] = s.str.lower() == s

    failed = meta[
        ~(s_ok | (meta[s.name + '_lower'] & meta[s.name + '_ok']))]
    failed[s.name + '_suggestions'] = failed[s.name].apply(
        lambda s: '; '.join(get_close_matches(s, ref)))
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s_ok.name, s.name + '_lower',
                    s.name + '_ok', s.name + '_suggestions']])
    msg = "Found %i invalid %ss: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_sampletype(meta, sampletypes, okexcept, record_property):
    if 'SampleType' not in meta.columns:
        return pytest.skip("No SampleType specified.")
    ref = sampletypes
    meta = meta.copy()
    s = meta['SampleType'].fillna('')

    s_ok = okexcept(s.name)
    meta = meta.join(s_ok)
    meta[s.name + '_ok'] = (~s.astype(bool)) | np.isin(s, ref)

    failed = meta[~(s_ok | meta[s.name + '_ok'])]
    failed[s.name + '_suggestions'] = failed[s.name].apply(
        lambda s: '; '.join(get_close_matches(s, ref)))
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s_ok.name, s.name + '_ok',
                    s.name + '_suggestions']])

    msg = "Found %i invalid SampleTypes: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_samplemethod(meta, samplemethods, okexcept, record_property):
    if 'SampleMethod' not in meta.columns:
        return pytest.skip("No SampleMethod specified.")
    ref = samplemethods
    meta = meta.copy()
    s = meta['SampleMethod'].fillna('')

    s_ok = okexcept(s.name)
    meta = meta.join(s_ok)
    meta[s.name + '_ok'] = (~s.astype(bool)) | np.isin(s, ref)

    failed = meta[~(s_ok | meta[s.name + '_ok'])]
    failed[s.name + '_suggestions'] = failed[s.name].apply(
        lambda s: '; '.join(get_close_matches(s, ref)))
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s_ok.name, s.name + '_ok',
                    s.name + '_suggestions']])

    msg = "Found %i invalid %ss: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


@pytest.mark.parametrize('worker', ['Worker1', 'Worker2', 'Worker3',
                                    'Worker4'])
def test_workerrole(meta, worker, workerroles, record_property):
    if worker + '_Role' not in meta.columns:
        return pytest.skip(f"No {worker}_Role specified.")
    ref = workerroles
    meta = meta.copy()
    s = meta[worker + '_Role'].fillna('')

    meta[s.name + '_ok'] = (~s.astype(bool)) | np.isin(s, ref)

    failed = meta[~meta[s.name + '_ok']]
    failed[s.name + '_suggestions'] = failed[s.name].apply(
        lambda s: '; '.join(get_close_matches(s, ref)))
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s.name + '_ok',  s.name + '_suggestions']])

    msg = "Found %i invalid values for %s: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_locationreliability(meta, locationreliabilities, record_property):
    if 'LocationReliability' not in meta.columns:
        return pytest.skip(f"No LocationReliability specified.")
    ref = locationreliabilities
    meta = meta.copy()
    s = meta['LocationReliability'].fillna('')

    meta[s.name + '_ok'] = ((~s.astype(bool)) | np.isin(s, ref))

    failed = meta[~(meta[s.name + '_ok'].values)]
    failed[s.name + '_suggestions'] = failed[s.name].apply(
        lambda s: '; '.join(get_close_matches(s, ref)))
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s.name + '_ok', s.name + '_suggestions']])

    msg = "Found %i invalid values for %s: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_ageuncertainty(meta, ageuncertainties, record_property):
    ref = ageuncertainties
    if 'AgeUncertainty' not in meta.columns:
        return pytest.skip(f"No AgeUncertainty specified.")
    meta = meta.copy()
    s = meta['AgeUncertainty'].replace(np.nan, '')
    meta[s.name + '_ok'] = ((~s.astype(bool)) | np.isin(s, ref))

    failed = meta[~meta[s.name + '_ok']]
    failed[s.name + '_suggestions'] = failed[s.name].apply(
        lambda s: '; '.join(get_close_matches(s, ref)))
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s.name + '_ok', s.name + '_suggestions']])
    msg = "Found %i invalid values for %s: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_elevation(meta, okexcept, record_property):
    meta = meta.copy()
    s = meta.Elevation.astype(float)
    s_ok = okexcept(s.name)
    meta = meta.join(s_ok)
    meta[s.name + '_ok'] = notnull = s.notnull()

    failed = meta[~(s_ok | notnull)]
    if len(failed):
        record_property(
            'failed_samples', failed[[s.name, s_ok.name, s.name + '_ok']])
    msg = "Found %i invalid values for %s: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_temperature(meta, okexcept, record_property):

    def test_range(l):
        try:
            temperature = np.array(l, dtype=float)
        except Exception:
            return False
        else:
            return ((temperature > -100) & (temperature < 100)).all()

    meta = meta.copy()
    s = meta.Temperature.astype(str).fillna('')
    s_ok = okexcept(s.name)
    meta = meta.join(s_ok)
    meta[s.name + '_nvals'] = nvals_ok = s.str.split(',').apply(len) == 17
    meta[s.name + '_ok'] = range_ok = s.str.split(',').apply(test_range)

    failed = meta[~(s_ok | (nvals_ok & range_ok))]
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s_ok.name, s.name + '_nvals', s.name + '_ok']])
    msg = "Found %i invalid values for %s: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


def test_precip(meta, okexcept, record_property):

    def test_range(l):
        try:
            precip = np.array(l, dtype=float)
        except Exception:
            return False
        else:
            return ((precip >= 0) & (precip < 10000)).all()

    meta = meta.copy()
    s = meta.Precipitation.astype(str).fillna('')
    s_ok = okexcept(s.name)
    meta = meta.join(s_ok)
    meta[s.name + '_nvals'] = nvals_ok = s.str.split(',').apply(len) == 17
    meta[s.name + '_ok'] = range_ok = s.str.split(',').apply(test_range)

    failed = meta[~(s_ok | (nvals_ok & range_ok))]
    if len(failed):
        record_property(
            'failed_samples',
            failed[[s.name, s_ok.name, s.name + '_nvals', s.name + '_ok']])
    msg = "Found %i invalid values for %s: %s" % (
        len(failed), s.name, textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg


# --- sample file tests


def test_orig_varnames(counts, record_property):
    counts = counts.copy()
    counts.original_varname.fillna('')
    counts = counts[counts.groupid != 'NOPO']
    counts['original_varname_valid'] = names = counts.original_varname.astype(
        bool)
    counts['duplicated'] = duplicated = counts.duplicated(
        ['samplename', 'original_varname'], keep=False)

    failed = counts[(~names) | duplicated]
    if len(failed):
        record_property('failed_data', failed)
    msg = "Found %i invalid original varnames: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.samplename.unique()), 80, placeholder='...'))
    assert not len(failed), msg


def test_acc_varnames(counts, record_property):
    counts = counts.copy()
    counts.acc_varname.fillna('')
    counts['acc_varname_valid'] = names = counts.acc_varname.astype(bool)
    duplicated = counts.duplicated(
        ['samplename', 'acc_varname'], keep=False)
    if duplicated.any():
        rows = counts[duplicated][
            ['samplename', 'original_varname', 'acc_varname']].sort_values(
                ['samplename', 'acc_varname'])
        print('Found several duplicated acc_varnames:\n\n- ' +
              '\n - '.join(starmap('{}: {} --> {}'.format, rows.values)))

    failed = counts[~names]
    if len(failed):
        record_property('failed_data', failed)
    msg = "Found %i invalid accepted varnames: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.samplename.unique()), 80, placeholder='...'))
    assert not len(failed), msg


def test_counts(counts, record_property, meta):
    counts = counts.merge(meta[['ispercent']], left_on='samplename',
                          right_index=True, how='left')
    failed = counts[~counts['ispercent'] &
                    (counts['count'].isnull() | (counts['count'] < 0))]
    if len(failed):
        record_property('failed_data', failed)
    msg = "Found %i rows with invalid count data: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.samplename.unique()), 80, placeholder='...'))
    assert not len(failed), msg


def test_percentages(counts, record_property, meta):
    failed = counts[counts['percentage'].isnull() | (counts['percentage'] < 0)]
    if len(failed):
        record_property('failed_data', failed)
    msg = "Found %i rows with invalid percentage data: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.samplename.unique()), 80, placeholder='...'))
    assert not len(failed), msg


def test_groupid(counts, record_property, groupids):
    counts = counts.copy()
    counts['groupid'] = counts['groupid'].astype(str).fillna('')

    counts['valid_groupid'] = valid = counts.groupid.str.strip().astype(bool)
    counts['existing_groupid'] = exists = np.isin(counts.groupid, groupids)

    failed = counts[~(valid & exists)]
    if len(failed):
        record_property('failed_data', failed)
    msg = "Found %i invalid groupids: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.samplename.unique()), 80, placeholder='...'))
    assert not len(failed), msg


def test_data_exists(meta, data_files, record_property):
    meta['data_file'] = data_files
    meta['data_exists'] = meta.data_file.apply(osp.exists)

    failed = meta[~meta.data_exists]
    if len(failed):
        record_property('failed_samples', failed[['data_file', 'data_exists']])
    msg = "Missing %i datafiles: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg
