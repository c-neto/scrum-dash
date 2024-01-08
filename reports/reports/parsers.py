import pandas as pd
from pydantic import BaseModel


class MappingAssigneeTeam(BaseModel):
    assignee: str
    team: str


class MappingAreaTeam(BaseModel):
    area: str
    team: str


class IssueOverall(BaseModel):
    issue_total_count: int | None

    issue_todo_count: int | None
    issue_doing_count: int | None
    issue_done_count: int | None

    issue_todo_percent: int | None
    issue_doing_percent: int | None
    issue_done_percent: int | None


class IssuePlanned(BaseModel):
    issue_planned_total_count: int | None

    issue_planned_todo_count: int | None
    issue_planned_doing_count: int | None
    issue_planned_done_count: int | None

    issue_planned_todo_percent: int | None
    issue_planned_doing_percent: int | None
    issue_planned_done_percent: int | None


class IssueUnplanned(BaseModel):
    issue_unplanned_total_count: int | None

    issue_unplanned_todo_count: int | None
    issue_unplanned_doing_count: int | None
    issue_unplanned_done_count: int | None

    issue_unplanned_todo_percent: int | None
    issue_unplanned_doing_percent: int | None
    issue_unplanned_done_percent: int | None


class IssueEpic(BaseModel):
    issue_epic_total_count: int | None

    issue_epic_todo_count: int | None
    issue_epic_doing_count: int | None
    issue_epic_done_count: int | None

    issue_epic_todo_percent: int | None
    issue_epic_doing_percent: int | None
    issue_epic_done_percent: int | None


class SprintReport(IssueOverall, IssuePlanned, IssueUnplanned, IssueEpic):
    sprint: int


class AssigneeReport(SprintReport):
    assignee: str


class AreaReport(SprintReport):
    area: str


class TeamReport(SprintReport):
    team: str


class EpicReport(SprintReport):
    epic_link_summary: str


def get_percent(sub_value: int, total_value: int):
    if sub_value == 0 and total_value == 0:
        return None

    value = (sub_value / total_value) * 100
    return int(value)


def get_issue_overall(data_frame: pd.DataFrame) -> IssueOverall:
    filter_todo = data_frame["board"] == "todo"
    filter_doing = data_frame["board"] == "doing"
    filter_done = data_frame["board"] == "done"

    issue_total_count = len(data_frame)

    issue_todo_count = len(data_frame[filter_todo])
    issue_doing_count = len(data_frame[filter_doing])
    issue_done_count = len(data_frame[filter_done])

    issue_todo_percent = get_percent(issue_todo_count, issue_total_count)
    issue_doing_percent = get_percent(issue_doing_count, issue_total_count)
    issue_done_percent = get_percent(issue_done_count, issue_total_count)

    issue_overall = IssueOverall(
        issue_total_count=issue_total_count,
        issue_todo_count=issue_todo_count,
        issue_doing_count=issue_doing_count,
        issue_done_count=issue_done_count,
        issue_todo_percent=issue_todo_percent,
        issue_doing_percent=issue_doing_percent,
        issue_done_percent=issue_done_percent,
    )

    return issue_overall


def get_issue_planned(df: pd.DataFrame):
    filter_planned = df["is_planned"] == True
    filter_todo = df["board"] == "todo"
    filter_doing = df["board"] == "doing"
    filter_done = df["board"] == "done"

    issue_planned_total_count = len(df[filter_planned])
    issue_planned_todo_count = len(df[filter_planned & filter_todo])
    issue_planned_doing_count = len(df[filter_planned & filter_doing])
    issue_planned_done_count = len(df[filter_planned & filter_done])

    issue_planned_todo_percent = get_percent(issue_planned_todo_count, issue_planned_total_count)
    issue_planned_doing_percent = get_percent(issue_planned_doing_count, issue_planned_total_count)
    issue_planned_done_percent = get_percent(issue_planned_done_count, issue_planned_total_count)

    issue_planned = IssuePlanned(
        issue_planned_total_count=issue_planned_total_count,
        issue_planned_todo_count=issue_planned_todo_count,
        issue_planned_doing_count=issue_planned_doing_count,
        issue_planned_done_count=issue_planned_done_count,
        issue_planned_todo_percent=issue_planned_todo_percent,
        issue_planned_doing_percent=issue_planned_doing_percent,
        issue_planned_done_percent=issue_planned_done_percent,
    )

    return issue_planned


def get_issue_unplanned(df: pd.DataFrame):
    filter_unplanned = df["is_planned"] == False
    filter_todo = df["board"] == "todo"
    filter_doing = df["board"] == "doing"
    filter_done = df["board"] == "done"

    issue_unplanned_total_count = len(df[filter_unplanned])
    issue_unplanned_todo_count = len(df[filter_unplanned & filter_todo])
    issue_unplanned_doing_count = len(df[filter_unplanned & filter_doing])
    issue_unplanned_done_count = len(df[filter_unplanned & filter_done])

    issue_unplanned_todo_percent = get_percent(
        issue_unplanned_todo_count, issue_unplanned_total_count
    )
    issue_unplanned_doing_percent = get_percent(
        issue_unplanned_doing_count, issue_unplanned_total_count
    )
    issue_unplanned_done_percent = get_percent(
        issue_unplanned_done_count, issue_unplanned_total_count
    )

    issue_unplanned = IssueUnplanned(
        issue_unplanned_total_count=issue_unplanned_total_count,
        issue_unplanned_todo_count=issue_unplanned_todo_count,
        issue_unplanned_doing_count=issue_unplanned_doing_count,
        issue_unplanned_done_count=issue_unplanned_done_count,
        issue_unplanned_todo_percent=issue_unplanned_todo_percent,
        issue_unplanned_doing_percent=issue_unplanned_doing_percent,
        issue_unplanned_done_percent=issue_unplanned_done_percent,
    )

    return issue_unplanned


def get_issue_epic(data_frame: pd.DataFrame):
    df = data_frame.dropna(subset="epic_link_summary")

    filter_todo = df["board"] == "todo"
    filter_doing = df["board"] == "doing"
    filter_done = df["board"] == "done"

    issue_epic_total_count = len(df)
    issue_epic_todo_count = len(df[filter_todo])
    issue_epic_doing_count = len(df[filter_doing])
    issue_epic_done_count = len(df[filter_done])

    issue_epic_todo_percent = get_percent(issue_epic_todo_count, issue_epic_total_count)
    issue_epic_doing_percent = get_percent(issue_epic_doing_count, issue_epic_total_count)
    issue_epic_done_percent = get_percent(issue_epic_done_count, issue_epic_total_count)

    issue_epic = IssueEpic(
        issue_epic_total_count=issue_epic_total_count,
        issue_epic_todo_count=issue_epic_todo_count,
        issue_epic_doing_count=issue_epic_doing_count,
        issue_epic_done_count=issue_epic_done_count,
        issue_epic_todo_percent=issue_epic_todo_percent,
        issue_epic_doing_percent=issue_epic_doing_percent,
        issue_epic_done_percent=issue_epic_done_percent,
    )

    return issue_epic


def get_values(data_frame: pd.DataFrame, column: str, sprint: int):
    rows = []

    for cell_value in data_frame[column].dropna().unique():
        filter_by_arg_column = data_frame[column] == cell_value
        df_by_arg_column = data_frame[filter_by_arg_column]

        issue_total_count = len(df_by_arg_column)

        issue_overall = get_issue_overall(df_by_arg_column)
        issue_planned = get_issue_planned(df_by_arg_column)
        issue_unplanned = get_issue_unplanned(df_by_arg_column)
        issue_epic = get_issue_epic(df_by_arg_column)

        result = {
            **issue_overall.model_dump(),
            **issue_planned.model_dump(),
            **issue_unplanned.model_dump(),
            **issue_epic.model_dump(),
            "issue_total_count": issue_total_count,
            "sprint": sprint,
            column: str(cell_value).lower(),
        }

        rows.append(result)

    return rows


def make_report_rows(data_frame: pd.DataFrame, report_schema, column: str):
    rows = []
    for sprint in data_frame["sprint"].unique():
        filter_by_sprint = data_frame["sprint"] == sprint

        df_by_sprint = data_frame[filter_by_sprint]
        report_rows = get_values(df_by_sprint, column, sprint)

        for report_row in report_rows:
            assignee_report = report_schema(**report_row)
            rows.append(assignee_report)

    return rows


def create_report_area(data_frame: pd.DataFrame):
    result = make_report_rows(data_frame, AreaReport, "area")
    return result


def create_report_assignee(data_frame: pd.DataFrame):
    result = make_report_rows(data_frame, AssigneeReport, "assignee")
    return result


def create_report_team(data_frame: pd.DataFrame):
    result = make_report_rows(data_frame, TeamReport, "team")
    return result


def create_report_sprints(data_frame: pd.DataFrame):
    result = make_report_rows(data_frame, SprintReport, "sprint")
    return result


def create_report_epic_link_summary(data_frame: pd.DataFrame):
    result = make_report_rows(data_frame, EpicReport, "epic_link_summary")
    return result


def create_report_assignee_team_mapping(assignee_mapping: dict):
    rows = []
    for team, assignees in assignee_mapping.items():
        area_rows = [MappingAssigneeTeam(assignee=assignee, team=team) for assignee in assignees]
        rows.extend(area_rows)
    return rows


def create_report_area_team_mapping(area_mapping: dict):
    rows = []
    for team, areas in area_mapping.items():
        area_rows = [MappingAreaTeam(area=area, team=team) for area in areas]
        rows.extend(area_rows)
    return rows
