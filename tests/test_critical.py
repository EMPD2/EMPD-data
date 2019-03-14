# Critical tests for the EMPD data. If they do not run, you can abort the tests
import pytest


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
def test_data_columns(data_frame):
    ref_cols = {'var_', 'samplename', 'count', 'acc_var_',
                'original_varname', 'acc_varname', 'groupid', 'groupname',
                'higher_groupid', 'included_in_percent_sum', 'make_percent',
                'higher_groupname', 'percentage'}
    assert ref_cols <= set(data_frame.columns)
    assert data_frame.columns.all()  # make sure every column has a title
