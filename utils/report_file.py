import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_make_report(item):
    outcome = yield
    report = outcome.get_result()

    # Add custom markers to the report
    if report.when == 'call':
        case_id = item.get_closest_marker('case_id')
        title = item.get_closest_marker('title')

        if case_id:
            report.case_id = case_id.args[0] if case_id.args else 'N/A'
        if title:
            report.title = title.args[0] if title.args else 'N/A'

def pytest_html_results_table_header(cells):
    cells.insert(1, '<th>Test Case ID</th>')
    cells.insert(2, '<th>Title</th>')


def pytest_html_results_table_row(report, cells):
    case_id = getattr(report, 'case_id', 'N/A')
    title = getattr(report, 'title', 'N/A')

    cells.insert(1, f'<td>{case_id}</td>')
    cells.insert(2, f'<td>{title}</td>')