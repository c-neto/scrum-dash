import pandas as pd


def merge_by_assignee_column(
    df_assignee: pd.DataFrame, df_mapping_assignee_by_team: pd.DataFrame
) -> pd.DataFrame:
    df_assignee_with_team = pd.merge(
        df_assignee,
        df_mapping_assignee_by_team,
        left_on="assignee",
        right_on="assignee",
    )
    return df_assignee_with_team


def merge_by_area_column(
    df_area: pd.DataFrame, df_mapping_area_by_team: pd.DataFrame
) -> pd.DataFrame:
    df_area_with_team = pd.merge(df_area, df_mapping_area_by_team, left_on="area", right_on="area")
    return df_area_with_team


def get_unique_assignees(data_frame: pd.DataFrame) -> pd.Series:
    assignees = data_frame["assignee"].unique()
    return assignees


def get_unique_teams(data_frame: pd.DataFrame) -> pd.Series:
    assignees = data_frame["team"].unique()
    return assignees


def filter_issues_by_sprint(data_frame: pd.DataFrame, sprint: str | int) -> pd.DataFrame:
    filter_sprint = data_frame["sprint"] == sprint
    filtered_df = data_frame[filter_sprint]
    return filtered_df


def filter_issues_by_assignee(data_frame: pd.DataFrame, assignee: str) -> pd.DataFrame:
    filter_assignee = data_frame["assignee"] == assignee
    filtered_df = data_frame[filter_assignee]
    return filtered_df


def filter_issues_by_team(data_frame: pd.DataFrame, team: str) -> pd.DataFrame:
    filter_team = data_frame["team"] == team
    filtered_df = data_frame[filter_team]
    return filtered_df


def filter_issues_by_area(data_frame: pd.DataFrame, area: str) -> pd.DataFrame:
    filter_team = data_frame["area"] == area
    filtered_df = data_frame[filter_team]
    return filtered_df


def filter_issues_by_year(data_frame: pd.DataFrame, year: int) -> pd.DataFrame:
    sprint_filter = data_frame["year"] == year
    filtered_df = data_frame[sprint_filter]
    return filtered_df


def filter_issues_until_sprint(data_frame: pd.DataFrame, sprint: int) -> pd.DataFrame:
    sprint_filter = data_frame["sprint"] <= sprint
    filtered_df = data_frame[sprint_filter]
    return filtered_df


def agg_mean(data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = data_frame.groupby(columns).mean(numeric_only=True).round()
    df = df.sort_values(by="issue_done_percent")
    df = df.reset_index()
    return df


def agg_sum(data_frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = data_frame.groupby(columns).sum(numeric_only=True)
    df = df.reset_index()
    return df


def get_first_and_last_sprint(data_frame: pd.DataFrame) -> tuple[int, int]:
    sprints = data_frame["sprint"].unique()
    first, last = min(sprints), max(sprints)
    return first, last
