# https://pydash.readthedocs.io/en/latest/api.html#pydash.objects.get


from pydantic import BaseModel
import pydash as py_

from settings import settings
from extract.jira import IssuesCollectionDTO


class IssueRow(BaseModel):
    sprint: int
    assignee: str | None
    area: str | None
    team: str | None
    epic_link_summary: str | None
    issue_key: str
    issue_type: str
    original_estimate: int | None
    priority: str | None
    status: str | None
    summary: str | None
    time_spent: int | None
    is_planned: bool


def get_board(issue: dict, board_by_status_mapping: dict) -> str:
    issues_status = py_.get(issue, "fields.status.name")
    issue_type = py_.lower_case(issues_status)

    issue_board = ""

    for board, statuses in board_by_status_mapping.items():
        if issue_type in statuses:
            issue_board = board
            break

    return issue_board


def get_assignee(issue: dict):
    assignee = py_.get(issue, "fields.assignee.emailAddress")

    if not assignee:
        assignee = py_.get(issue, "fields.assignee.displayName")

    return assignee


def get_area(issue: dict, issue_custom_field_area: str):
    issue_area = py_.get(issue, issue_custom_field_area)

    return issue_area


def get_epic_link_summary(issue: dict):
    epic_name = None

    issue_type = py_.get(issue, "fields.parent.fields.issuetype.name")

    if py_.lower_case(issue_type):
        epic_name = py_.get(issue, "fields.parent.fields.summary")

    return epic_name


def get_team(issue: dict, issue_custom_field_team: str):
    issue_team = py_.get(issue, issue_custom_field_team)
    issue_team = py_.lower_case(issue_team)

    return issue_team


def get_issue_key(issue: dict):
    return issue["key"]


def get_issue_type(issue: dict):
    issue_type = py_.get(issue, "fields.issuetype.name")
    issue_type = py_.lower_case(issue_type)

    return issue_type


def get_original_estimate(issue: dict):
    originalestimate = py_.get(issue, "fields.timeoriginalestimate")

    return originalestimate


def get_priority(issue: dict):
    priority = py_.get(issue, "fields.priority.name")

    return priority


def get_status(issue: dict):
    issues_status = py_.get(issue, "fields.status.name")
    issue_type = py_.lower_case(issues_status)

    return issue_type


def get_summary(issue: dict):
    return py_.get(issue, "fields.summary")


def get_time_spent(issue: dict):
    return py_.get(issue, "fields.timespent")


def _make_issue_row(issue: dict, is_planned: bool, sprint: int):
    assignee = get_assignee(issue)
    area = get_area(issue, settings["issue_custom_field"]["area"]["api_path"])
    epic_link_summary = get_epic_link_summary(issue)
    team = get_team(issue, settings["issue_custom_field"]["team"]["api_path"])
    issue_key = get_issue_key(issue)
    issue_type = get_issue_type(issue)
    original_estimate = get_original_estimate(issue)
    priority = get_priority(issue)
    status = get_status(issue)
    summary = get_summary(issue)
    time_spent = get_time_spent(issue)

    issue_row = IssueRow(
        assignee=assignee,
        area=area,
        team=team,
        epic_link_summary=epic_link_summary,
        issue_key=issue_key,
        issue_type=issue_type,
        original_estimate=original_estimate,
        priority=priority,
        status=status,
        sprint=sprint,
        summary=summary,
        time_spent=time_spent,
        is_planned=is_planned,
    )

    return issue_row


def make_csv_report(issues_collection: IssuesCollectionDTO) -> list[IssueRow]:
    issues_rows = []

    for issue in issues_collection.issues_planned:
        issue = _make_issue_row(issue, True, issues_collection.sprint)
        issues_rows.append(issue)

    for issue in issues_collection.issues_unplanned:
        issue = _make_issue_row(issue, False, issues_collection.sprint)
        issues_rows.append(issue)

    return issues_rows
