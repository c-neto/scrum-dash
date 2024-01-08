from extract.jira import IssuesCollectionDTO
from extract.processor import IssueRow
from pathlib import Path
import csv


def persist_reports_raw(issues_collections_dto: IssuesCollectionDTO, report_file_path: str) -> str:
    file_abspath = Path(report_file_path)
    file_abspath.parent.mkdir(parents=True, exist_ok=True)
    file_abspath.write_text(issues_collections_dto.model_dump_json())

    return str(file_abspath.absolute())


def persist_reports_in_csv(issue_rows: list[IssueRow], report_file_path: str) -> str:
    file_abspath = Path(report_file_path)
    file_abspath.parent.mkdir(parents=True, exist_ok=True)

    headers = list(IssueRow.model_fields.keys())

    with file_abspath.open("w") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(row.model_dump().values() for row in issue_rows)

    return str(file_abspath.absolute())
