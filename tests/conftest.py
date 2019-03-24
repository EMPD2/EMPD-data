# configuration module for pytest
from collections import OrderedDict
import pathlib
import os.path as osp
import pytest
from functools import partial

all_reports = OrderedDict()


report_path = ''

_meta_file = pathlib.Path(
    osp.join(osp.dirname(osp.abspath(__file__)), '..', 'meta.tsv')).resolve()

_base_meta_file = pathlib.Path(str(_meta_file.absolute()))

_commit_fixes = False


def _meta(fname=None):
    import pandas as pd
    fname = fname or _meta_file
    return pd.read_csv(str(fname), sep='\t', index_col='SampleName')


def _data_files():
    import pandas as pd
    df = pd.read_csv(str(_meta_file), sep='\t', index_col='SampleName')
    base = osp.join(osp.dirname(_meta_file), 'samples')
    return [osp.join(base, sample + '.tsv') for sample in df.index.values]


@pytest.fixture
def skip_ci(request):
    return request.config.getoption("--skip-ci")


@pytest.fixture
def counts():
    import pandas as pd
    read_tsv = partial(pd.read_csv, sep='\t')
    return pd.concat(list(map(read_tsv, _data_files())))


@pytest.fixture(scope='session')
def meta_file(request):
    """The meta data file as PosixPath"""
    return pathlib.Path(request.config.getoption(
        '--empd-meta')).expanduser().resolve()


@pytest.fixture(scope='session')
def meta(meta_file):
    """The meta data as pandas DataFrame"""
    return _meta(meta_file)


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
def ageuncertainties(meta_file):
    import pandas as pd
    return pd.read_csv(
        osp.join(osp.dirname(meta_file), 'tab-delimited',
                 'ageuncertainties.tsv'),
        sep='\t').iloc[:, 0].values


@pytest.fixture(scope='session')
def samples_dir(meta_file):
    return osp.join(osp.dirname(meta_file), 'samples')


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


def pytest_runtest_logreport(report):
    if report_path:
        all_reports.setdefault(report.nodeid, []).append(report)


def pytest_sessionfinish(session):
    md = ''
    for key, reports in all_reports.items():
        reports.sort(key=get_priority)

        d = OrderedDict()
        report = reports[-1]
        if report.longreprtext:
            d['error'] = report.longreprtext
        for attr in ['stderr', 'stdout', 'log']:
            if getattr(report, 'cap' + attr):
                d[attr] = getattr(report, 'cap' + attr)
        if d and not any(report.skipped for report in reports):
            md += '<details><summary>%s..<b>%s</b></summary>\n' % (
                report.nodeid, report.outcome.upper())
            if len(d) == 1:
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
            md += '</details>\n'

    if report_path:
        report_path.write_text(md, encoding='utf-8')


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--markdown-report", action="store", metavar="path",
        default=None, help="create markdown report file at given path.")
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


def pytest_configure(config):
    global report_path, _meta_file,  _base_meta_file, _commit_fixes
    if config.option.markdown_report:
        report_path = pathlib.Path(
            config.option.markdown_report).expanduser().resolve()
    if config.option.commit:
        _commit_fixes = True
    _meta_file = pathlib.Path(config.option.empd_meta).expanduser().resolve()
    _base_meta_file = pathlib.Path(
        osp.join(osp.dirname(_meta_file), 'meta.tsv'))
    if not config.option.fix_db:
        if getattr(config.option, 'markexpr', None):
            config.option.markexpr += ' and not dbfix'
        else:
            config.option.markexpr = 'not dbfix'
