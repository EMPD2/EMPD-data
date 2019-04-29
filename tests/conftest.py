# configuration module for pytest
from collections import OrderedDict
import pathlib
import os
import os.path as osp
import pytest
from functools import partial
from itertools import starmap
import textwrap

all_reports = OrderedDict()


report_path = ''

extract_failed = False

_meta_file = pathlib.Path(
    osp.join(osp.dirname(osp.abspath(__file__)), '..', 'meta.tsv')).resolve()

_base_meta_file = pathlib.Path(str(_meta_file.absolute()))

_commit_fixes = False


def _meta(fname=None):
    import pandas as pd
    import numpy as np
    fname = fname or _meta_file

    ret = pd.read_csv(str(fname), sep='\t', index_col='SampleName',
                      dtype=str)

    for col in ['Latitude', 'Longitude', 'Elevation', 'AreaOfSite', 'AgeBP']:
        if col in ret.columns:
            ret[col] = ret[col].replace('', np.nan).astype(float)
    if 'ispercent' in ret.columns:
        ret['ispercent'] = ret['ispercent'].replace('', False).astype(bool)

    if 'okexcept' not in ret.columns:
        ret['okexcept'] = ''

    return ret


def _data_files():
    df = _meta()
    base = osp.join(osp.dirname(_meta_file), 'samples')
    return [osp.join(base, sample + '.tsv') for sample in df.index.values]


@pytest.fixture
def skip_ci(request):
    return request.config.getoption("--skip-ci")


@pytest.fixture
def counts(data_files):
    import pandas as pd
    read_tsv = partial(pd.read_csv, sep='\t')
    if not len(data_files):
        pytest.skip("No sample data provided")
    return pd.concat(list(map(read_tsv, data_files)))


@pytest.fixture(scope='session')
def meta_file(request):
    """The meta data file as PosixPath"""
    return pathlib.Path(request.config.getoption(
        '--empd-meta')).expanduser().resolve()


@pytest.fixture(scope='session')
def full_meta(meta_file):
    """The meta data as pandas DataFrame"""
    return _meta(meta_file)


@pytest.fixture(scope='session')
def meta(full_meta, request):
    return full_meta.loc[full_meta.reset_index().SampleName.str.contains(
        request.config.getoption('--sample')).values, :].copy()


@pytest.fixture(scope='session')
def base_meta_file():
    return _base_meta_file


@pytest.fixture(scope='session')
def base_meta():
    return _meta(_base_meta_file)


@pytest.fixture(scope='session')
def base_counts():
    """A pd.DataFrame mapping from varname to acc_varname"""
    import pandas as pd
    import glob
    base = osp.join(osp.dirname(_meta_file), 'samples')
    data_files = _data_files()
    read_tsv = partial(pd.read_csv, sep='\t')
    files = filter(
        lambda f1: not any(osp.samefile(f1, f2) for f2 in data_files),
        glob.glob(osp.join(base, '*.tsv')))
    return pd.concat(list(map(read_tsv, files)), ignore_index=True)


@pytest.fixture(scope='session')
def countries(meta_file):
    """The countries in the database with the natural_earth column as index"""
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited', 'countries.tsv'),
        sep='\t').dropna(subset=['natural_earth']).set_index(
            'natural_earth').iloc[:, 0]


@pytest.fixture(scope='session')
def nat_earth_countries(meta, countries):
    import pandas as pd
    import numpy as np
    if not len(meta):
        return pytest.skip("No samples provided")
    lat = meta.Latitude.astype(float).values
    lon = meta.Longitude.astype(float).values
    mask = ~(np.isnan(lat) | np.isnan(lon))
    try:
        import geopandas as gpd  # Using geopandas is much faster!
    except ImportError:
        from latlon_utils import get_country
        countries = list(starmap(get_country, zip(lat[mask], lon[mask])))
    else:
        from latlon_utils import get_country_gpd
        countries = get_country_gpd(lat[mask], lon[mask])
    full_countries = np.zeros_like(mask, countries.dtype)
    full_countries[mask] = countries
    return pd.Series(full_countries, index=meta.index)


@pytest.fixture(scope='session')
def samplecontexts(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited',
                 'samplecontexts.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def sampletypes(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited', 'sampletypes.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def samplemethods(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited', 'samplemethods.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def workerroles(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited', 'workerroles.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def locationreliabilities(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited',
                 'locationreliabilities.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def groupids_table(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited', 'groupid.tsv'),
        sep='\t').replace('t', True).replace('f', False)


@pytest.fixture(scope='session')
def groupids(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited',
                 'groupid.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def ageuncertainties(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited',
                 'ageuncertainties.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def samples_dir(meta_file):
    return osp.join(osp.dirname(meta_file), 'samples')


@pytest.fixture(scope='session')
def data_files(meta_file, meta):
    base = osp.join(osp.dirname(meta_file), 'samples')
    return [osp.join(base, sample + '.tsv') for sample in meta.index.values]


@pytest.fixture
def data_file(request):
    """The path to a data file (set with metafunc.parameterize down below)"""
    return request.param


@pytest.fixture
def data_frame(data_file):
    import pandas as pd
    return pd.read_csv(data_file, sep='\t')


@pytest.fixture
def meta_row(request):
    """One row of the meta data"""
    return request.param


@pytest.fixture(scope='session')
def okexcept(meta):
    meta_okexcept = meta.okexcept.astype(str).fillna('')

    def okexcept(column):
        ret = meta_okexcept.str.contains(column)
        ret.name = f'okexcept({column})'
        return ret

    return okexcept


@pytest.fixture(scope='session')
def local_repo():
    try:
        from git import Repo
    except ImportError:
        return osp.dirname(str(_meta_file))
    else:
        return Repo(osp.dirname(str(_meta_file)))


@pytest.fixture(scope='session')
def commit_fixes():
    return _commit_fixes


def pytest_generate_tests(metafunc):
    if 'data_file' in metafunc.fixturenames:
        files = _data_files()
        metafunc.parametrize('data_file', files,
                             ids=list(map(osp.basename, files)), indirect=True)
    if 'meta_row' in metafunc.fixturenames:
        meta = _meta()
        metafunc.parametrize('meta_row', [row for key, row in meta.iterrows()],
                             ids=meta.index.tolist(), indirect=True)


def get_priority(report):
    if report.passed:
        return 0
    elif report.skipped:
        return 1
    elif report.failed:
        return 2


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        all_reports.setdefault(rep.nodeid, []).append(rep)


def pytest_sessionfinish(session):
    import pandas as pd
    md = ''
    meta = _meta()
    samples = meta.index.values
    failed_samples = set()

    for key, reports in all_reports.items():
        reports.sort(key=get_priority)

        d = OrderedDict()
        report = reports[-1]
        if report.longreprtext:
            d['error'] = report.longreprtext
        for attr in ['stderr', 'stdout', 'log']:
            if getattr(report, 'cap' + attr):
                d[attr] = getattr(report, 'cap' + attr)
        user_props = dict(report.user_properties)
        if d and not any(report.skipped for report in reports):
            md += '<details><summary>%s..<b>%s</b></summary>\n' % (
                report.nodeid, report.outcome.upper())
            if len(d) == 1 and (not 'failed_samples' in user_props and
                                not 'failed_data' in user_props):
                message, val = next(iter(d.items()))
                if message == 'error':
                    val = '\n\n```\n%s\n```' % val
                md += '%s: %s\n' % (message, val)
            else:
                for key, s in sorted(d.items()):
                    details = (
                        '<details>\n'
                        '<summary>%s</summary>\n\n'
                        '%s\n</details>') % (
                            key, '```\n%s\n```' % s if key == 'error' else s)
                    md += '\n' + details + '\n'
                if ('failed_samples' in user_props or
                    'failed_data' in user_props):
                    try:
                        df = user_props['failed_samples']
                        summary = '%i failed samples' % len(df)
                    except KeyError:
                        df = user_props['failed_data']
                        summary = '%i failed data rows' % len(df)
                    n = len(df)
                    df = df.head(session.config.getoption('--max-table-len'))
                    df = pd.concat([
                        pd.DataFrame([('---', ) * len(df.columns)],
                                     index=['---'], columns=df.columns),
                        df])
                    details = (
                        '<details>\n'
                        '<summary>%s</summary>\n\n'
                        '%s\n\nDisplaying %i of %i samples\n</details>') % (
                            summary,
                            textwrap.indent(
                                df.to_csv(sep='|', float_format='%1.8g'),
                                '| '), len(df) - 1, n)
                    md += '\n' + details + '\n'

            md += '</details>\n'
        if report.outcome == 'failed':
            failed_samples.update(set(report.keywords).intersection(samples))
            if 'failed_samples' in user_props:
                df = user_props['failed_samples']
                failed_samples.update(df.index)
                meta = meta.join(
                    df[[col for col in df.columns if col not in meta.columns]])
            elif 'failed_data' in user_props:
                df = user_props['failed_data']
                failed_samples.update(df.samplename)

    if report_path:
        report_path.write_text(md, encoding='utf-8')

    if extract_failed:
        target_dir = osp.join(osp.dirname(_meta_file), 'failures')
        target = osp.join(target_dir, extract_failed)
        os.makedirs(target_dir, exist_ok=True)
        meta.loc[list(failed_samples)].to_csv(
            target, sep='\t', float_format='%1.8g')

        if _commit_fixes:
            from git import Repo
            local_repo = Repo(osp.dirname(_meta_file))
            local_repo.index.add([target])
            local_repo.index.commit(
                f"Extracted failures to failures/{extract_failed} [skip ci]")


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--markdown-report", action="store", metavar="path",
        default=None, help="create markdown report file at given path.")
    group.addoption(
        '--max-table-len', metavar='NUM', type=int, default=100,
        help=("The maximal length of tables in the markdown-report. "
              "Default: %(default)s"))
    group = parser.getgroup('EMPD')
    group.addoption(
        "--fix-db", action='store_true', default=False,
        help="Run database fixes")
    group.addoption(
        "--commit", action='store_true', default=False,
        help="Commit the changes after having fixed the open issues.")
    group.addoption(
        "--skip-ci", action='store_true', default=False,
        help=("Do not build the commits with the continous integration. "
              "Has only an effect if the `--commit` argument is passed as "
              "well."))
    group.addoption('--empd-meta', default=str(_meta_file),
                    help="The path to the meta file")
    group.addoption(
        '--extract-failed', metavar='filename.tsv', nargs='?',
        const='failed.tsv', default=False,
        help=("Extract the meta data of failed samples into a separate file "
              "in the `failures` directory. Without argument, failed samples "
              "will be extracted to ``%(const)s``."))
    group.addoption(
        '--sample', metavar='SampleName', default='.*',
        help=("Name of samples to test. If provided, only samples that match "
              "the given pattern are tested."))


def pytest_configure(config):
    global report_path, _meta_file,  _base_meta_file, _commit_fixes
    global extract_failed
    if config.option.markdown_report:
        report_path = pathlib.Path(
            config.option.markdown_report).expanduser().resolve()
    if config.option.commit:
        _commit_fixes = True
    if config.option.extract_failed:
        extract_failed = config.option.extract_failed
    _meta_file = pathlib.Path(config.option.empd_meta).expanduser().resolve()
    _base_meta_file = pathlib.Path(
        osp.join(osp.dirname(_meta_file), 'meta.tsv'))
    fix_db = config.option.fix_db
    if getattr(config.option, 'markexpr', None):
        config.option.markexpr += ' and %sdbfix' % ('' if fix_db else 'not ')
    else:
        config.option.markexpr = '%sdbfix' % ('' if fix_db else 'not ')
