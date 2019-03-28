# Test the formatting of the data
import pytest
import numpy as np


def test_trailing_spaces(meta, record_property):
    has_failed = np.zeros_like(meta, dtype=bool)
    for i, (col, s) in enumerate(meta.astype(str).fillna('').items()):
        has_failed[:, i] = s.str.strip() != s
    failed = meta.where(has_failed).dropna(how='all').dropna(axis=1, how='all')
    record_property('failed_samples',
                    failed.astype(str).fillna('').applymap(repr))

    msg = "Found %i cells with trailing spaces" % has_failed.sum()
    assert not len(failed), msg


def test_newline_chars(meta, record_property):
    has_failed = np.zeros_like(meta, dtype=bool)
    for i, (col, s) in enumerate(meta.astype(str).fillna('').items()):
        has_failed[:, i] = s.str.replace('\n', ' ').str.replace(
            '\r', ' ') != s
    failed = meta.where(has_failed).dropna(how='all').dropna(axis=1, how='all')
    record_property('failed_samples',
                    failed.astype(str).fillna('').applymap(repr))

    msg = "Found %i cells with newline characters" % has_failed.sum()
    assert not len(failed), msg


@pytest.mark.parametrize('doi_field', ['DOI1', 'DOI2', 'DOI3', 'DOI4', 'DOI5'])
def test_doi(meta, doi_field, record_property):
    if doi_field in meta.columns and meta[doi_field].fillna('').any():
        col = meta[doi_field].astype(str).fillna('')
        orig = col
        for patt in ['https://doi.org/', 'http://dx.doi.org/', 'doi: ',
                     'doi.org/', 'DOI: ', 'DOI ', 'doi:', ' ',
                     'https://link.springer.com/article/']:
            col = col.replace(patt, '')
        failed = meta[col != orig]
        record_property('failed_samples', failed[[doi_field]])

        msg = "Found %i cells with invalid DOI" % len(failed)
        assert not len(failed[doi_field]), msg
    else:
        pytest.skip("%s field empty specified" % doi_field)
