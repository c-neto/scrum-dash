import parsers
import pandas as pd
from pydantic import BaseModel


def enrich_board(data_frame: pd.DataFrame, status_mapping: dict):
    filter_todo = data_frame["status"].isin(status_mapping["todo"])
    filter_doing = data_frame["status"].isin(status_mapping["doing"])
    filter_done = data_frame["status"].isin(status_mapping["done"])

    data_frame.loc[filter_todo, "board"] = "todo"
    data_frame.loc[filter_doing, "board"] = "doing"
    data_frame.loc[filter_done, "board"] = "done"


def read_issue_report_csv(path_input_issue_report: str) -> pd.DataFrame:
    df_input_issue_report = pd.read_csv(path_input_issue_report)
    return df_input_issue_report


def persist_reports_in_csv(rows: list[BaseModel], report_file_path: str):
    df = pd.DataFrame([row.model_dump() for row in rows])
    df.to_csv(report_file_path, index=False)


def persist_reports(df_input_issue_report: pd.DataFrame, reports_directory: str):
    sprints = parsers.create_report_sprints(df_input_issue_report)
    team = parsers.create_report_team(df_input_issue_report)
    assignee = parsers.create_report_assignee(df_input_issue_report)
    area = parsers.create_report_area(df_input_issue_report)
    epic_link_summary = parsers.create_report_epic_link_summary(df_input_issue_report)

    persist_reports_in_csv(sprints, f"{reports_directory}/sprints.csv")
    persist_reports_in_csv(team, f"{reports_directory}/team.csv")
    persist_reports_in_csv(assignee, f"{reports_directory}/assignee.csv")
    persist_reports_in_csv(area, f"{reports_directory}/area.csv")
    persist_reports_in_csv(epic_link_summary, f"{reports_directory}/epic_link_summary.csv")


def persist_enum_csv(enum_mappings: dict, reports_directory: str):
    mapping_assignee_by_team = parsers.create_report_assignee_team_mapping(
        enum_mappings["mapping_assignee_by_team"]
    )
    mapping_area_by_team = parsers.create_report_area_team_mapping(
        enum_mappings["mapping_area_by_team"]
    )

    persist_reports_in_csv(
        mapping_assignee_by_team,
        f"{reports_directory}/mapping-assignee-by-team.csv",
    )
    persist_reports_in_csv(
        mapping_area_by_team,
        f"{reports_directory}/mapping-area-by-team.csv",
    )
