import json
from pathlib import Path

from extract.settings import settings
from extract import persistence, processor, jira


def create_report_raw(issues_collection_dto: jira.IssuesCollectionDTO):
    report_file_path = "{base_path}/{sprint}-report-raw.json".format(
        base_path=settings["path_output_issue_report"], sprint=issues_collection_dto.sprint
    )
    persistence.persist_reports_raw(issues_collection_dto, report_file_path)


def create_report_csv(issues_collection_dto: jira.IssuesCollectionDTO):
    issues_report_rows = processor.make_csv_report(issues_collection_dto)
    report_file_path = "{base_path}/{sprint}-report.csv".format(
        base_path=settings["path_output_issue_report"], sprint=issues_collection_dto.sprint
    )

    persistence.persist_reports_in_csv(issues_report_rows, report_file_path)


def get_issues_collections_from_json_file(
    report_raw_json_path: str,
) -> jira.IssuesCollectionDTO:
    report_raw_path = Path(report_raw_json_path)
    report_content = report_raw_path.read_text()
    report = json.loads(report_content)
    issues_collection_dto = jira.IssuesCollectionDTO(**report)
    return issues_collection_dto


def get_issues_collections_from_api(sprint: int) -> jira.IssuesCollectionDTO:
    jira_api = jira.JiraAPI(**settings["jira"])
    jql_statements = jira.JQLStatements(**settings["jql"])

    print("getting issues in the Jira API... (15 seconds around to be completed)")
    issues_collection = jira.get_issues_collection(jira_api, jql_statements, sprint)

    return issues_collection
