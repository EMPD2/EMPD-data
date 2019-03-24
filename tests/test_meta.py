# Test functions for the meta data
import os.path as osp
import glob
import pytest
from latlon_utils import get_country
from itertools import starmap
import numpy as np
import pandas as pd


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


def test_lat_lon(meta_row):
    assert okexcept(meta_row, 'Latitude') or (
        meta_row.Latitude >= -90 and meta_row.Latitude <= 90)
    assert okexcept(meta_row, 'Longitude') or (
        meta_row.Longitude >= -180 and meta_row.Longitude <= 360)


def test_country(meta_row):
    assert okexcept(meta_row, 'Country') or meta_row.Country == get_country(
        *meta_row[['Latitude', 'Longitude']])


def test_samplecontext(meta_row, samplecontexts):
    samplecontext = str(getattr(meta_row, 'SampleContext', ''))
    if isnull(samplecontext):
        return pytest.skip("No SampleContext specified.")
    assert (okexcept(meta_row, 'SampleContext') or
            samplecontext in samplecontexts)


def test_sampletype(meta_row, sampletypes):
    sampletype = str(getattr(meta_row, 'SampleType', ''))
    if isnull(sampletype):
        return pytest.skip("No SampleType specified.")
    assert (okexcept(meta_row, 'SampleType') or sampletype in sampletypes)


def test_samplemethod(meta_row, samplemethods):
    samplemethod = str(getattr(meta_row, 'SampleMethod', ''))
    if isnull(samplemethod):
        return pytest.skip("No samplemethod specified.")
    assert (okexcept(meta_row, 'SampleMethod') or
            samplemethod in samplemethods)


@pytest.mark.parametrize('worker', ['Worker1', 'Worker2', 'Worker3',
                                    'Worker4'])
def test_workerrole(meta_row, worker, workerroles):
    if (isnull(getattr(meta_row, worker + '_LastName', '')) or
            isnull(getattr(meta_row, worker + '_Role', ''))):
        return pytest.skip(worker + "_Role not specified.")
    assert meta_row[worker + '_Role'] in workerroles


def test_locationreliability(meta_row, locationreliabilities):
    locationreliability = str(getattr(meta_row, 'LocationReliability', ''))
    if isnull(locationreliability):
        return pytest.skip("No LocationReliability specified.")
    assert (okexcept(meta_row, 'LocationReliability') or
            locationreliability in locationreliabilities)


def test_ageuncertainty(meta_row, ageuncertainties):
    ageuncertainty = str(getattr(meta_row, 'AgeUncertainty', ''))
    if isnull(ageuncertainty):
        return pytest.skip("No AgeUncertainty specified.")
    assert (okexcept(meta_row, 'AgeUncertainty') or
            ageuncertainty in ageuncertainties)


def test_elevation(meta_row):
    assert okexcept(meta_row, 'Elevation') or ~np.isnan(meta_row.Elevation)


def test_temperature(meta_row):
    if okexcept(meta_row, 'Temperature'):
        return
    assert meta_row.Temperature
    temperature = np.array(meta_row.Temperature.split(',')).astype(float)
    assert len(temperature) == 17
    assert ((temperature > -100) & (temperature < 100)).all()


def test_precip(meta_row):
    if okexcept(meta_row, 'Precipitation'):
        return
    assert meta_row.Precipitation
    precip = np.array(meta_row.Precipitation.split(',')).astype(float)
    assert len(precip) == 17
    assert ((precip > 0) & (precip < 10000)).all()


# --- sample file tests


def test_orig_varnames(data_frame):
    assert data_frame.original_varname.all()
    duplicated = data_frame.duplicated('original_varname')
    assert not duplicated.any(), (
        'Duplicated acc_varnames: ' + str(
            data_frame[duplicated].original_varname))


def test_acc_varnames(data_frame):
    assert data_frame.acc_varname.all()
    duplicated = data_frame.duplicated('acc_varname', keep=False)
    if duplicated.any():
        names = data_frame[duplicated][['original_varname', 'acc_varname']]
        print('Found several duplicated acc_varnames:\n\n- ' +
              '\n - '.join(starmap('{}: {}'.format, names.values)))


def test_counts(data_frame):
    assert data_frame['count'].notnull().all()


def test_groupid(data_frame):
    assert data_frame.groupid.all()


def test_percentage(data_frame):
    assert data_frame[data_frame.make_percent].percentage.notnull().all()


def test_samplename(data_file):
    samplename = osp.splitext(osp.basename(data_file))[0]
    df = pd.read_csv(data_file, sep='\t')
    samplenames = df.samplename
    assert set(samplenames) == {samplename}


def test_data_exists(meta_row, samples_dir):
    fname = osp.join(samples_dir, meta_row.name) + '.tsv'
    assert osp.exists(fname), f"Missing {fname}"
