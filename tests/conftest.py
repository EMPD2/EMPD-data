# configuration module for pytest
from collections import OrderedDict, defaultdict

all_reports = OrderedDict()


report_path = ''


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
            d['message'] = report.longreprtext
        for attr in ['stderr', 'stdout', 'log']:
            if getattr(report, 'cap' + attr):
                d[attr] = getattr(report, 'cap' + attr)
        if d:
            md += '- [%s] %s..<b>%s</b>\n' % (
                'x' if not report.failed else ' ', report.nodeid,
                report.outcome.upper())
            for key, s in sorted(d.items()):
                details = (
                    '    <details>\n'
                    '<summary>%s</summary>\n\n'
                    '%s\n</details>') % (
                        key, '```\n%s\n```' % s if key == 'message' else s)
                md += '\n    '.join(details.splitlines()) + '\n'

    if report_path:
        with open(report_path, 'w') as f:
            f.write(md)


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--markdown-report",
        action="store",
        dest="mdreport",
        metavar="path",
        default=None,
        help="create markdown report file at given path.",
    )


def pytest_configure(config):
    global report_path
    report_path = config.getoption("mdreport")
