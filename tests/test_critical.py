# Critical tests for the EMPD data. If they do not run, you can abort the tests
import pytest
import os.path as osp
import pandas as pd
import textwrap


@pytest.mark.critical
def test_columns(meta, base_meta):
    required_cols = {
       'OriginalSampleName', 'Longitude', 'Latitude',
       'Worker1_Role', 'Worker1_LastName', 'Worker1_Initials',
       'Worker1_FirstName', 'Worker1_Address1',
       'Worker1_Email1', 'Worker1_Phone1'}
    assert required_cols <= set(meta.columns)
    assert meta.columns.all()  # make sure every column has a title


@pytest.mark.critical
def test_samplename_duplicates(meta):
    assert not meta.index.has_duplicates, "Duplicated samples: " + str(
        meta.index[meta.index.duplicated(keep=False)])


@pytest.mark.critical
def test_data_columns(meta, data_files, record_property):

    def test_data(fname):
        if osp.exists(fname):
            data_frame = pd.read_csv(fname, sep='\t')
            return (ref_cols <= set(data_frame.columns) and
                    data_frame.columns.fillna('').astype(bool).all())

    ref_cols = {'count', 'original_varname', 'acc_varname', 'groupid'}
    meta = meta.copy()
    meta['files'] = data_files
    meta['valid'] = meta['files'].apply(test_data)

    failed = meta[~meta['valid']]

    record_property('failed_samples', failed[['files', 'valid']])

    msg = "Found %i invalid data columns: %s" % (
        len(failed), textwrap.shorten(
            ', '.join(failed.index), 80, placeholder='...'))
    assert not len(failed), msg
