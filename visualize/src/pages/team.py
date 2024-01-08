import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
from dash import html, callback, Input, Output
import plotly.express as px
import database as db
from settings import settings, COLOR_CONTINUOUS_SCALE


dash.register_page(__name__)


df_mapping_assignee_by_team = pd.read_csv(
    settings["reports_directory"]["mapping_assignee_by_team"]
)
df_team = pd.read_csv(settings["reports_directory"]["team"])


team_page_input_team = dcc.Dropdown(
    options=df_mapping_assignee_by_team["team"].sort_values().unique(), id="team_page_input_team"
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Label("Team"), team_page_input_team]),
            ]
        ),
        html.Hr(),
        dbc.Row([dbc.Col(dcc.Graph(figure={}, id="issues_closed_percent_by_team"))]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure={}, id="team_page_issues_closed_percentage_by_planning_category"
                    )
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={}, id="team_page_issues_closed_count_by_progress_category")
                )
            ]
        ),
        html.Hr(),
        dbc.Row([dbc.Col(dcc.Graph(figure={}, id="team_page_issues_count_by_progress_category"))]),
    ]
)


@callback(
    Output(component_id="issues_closed_percent_by_team", component_property="figure"),
    [
        Input(component_id="team_page_input_team", component_property="value"),
    ],
)
def issues_closed_percent_by_team(team: str):
    df = db.agg_mean(df_team, ["team"])

    if team:
        df = db.filter_issues_by_team(df, team)

    fig = px.bar(
        df,
        orientation="h",
        text_auto=True,
        color="issue_done_percent",
        x="issue_done_percent",
        y="team",
        range_color=[0, 100],
        range_x=[0, 100],
        color_continuous_scale=COLOR_CONTINUOUS_SCALE,
        title=f"Issues Closed Percent by Team",
    )

    fig.add_shape(
        y0=-1,
        y1=len(df),
        x0=70,
        x1=0,
        fillcolor="red",
        opacity=0.2,
        layer="below",
        line_width=1,
    )
    fig.add_shape(
        y0=-1,
        y1=len(df),
        x0=70,
        x1=100,
        fillcolor="green",
        opacity=0.2,
        layer="below",
        line_width=1,
    )

    fig.update_layout(
        xaxis={"dtick": 10},
        margin={"t": 100, "b": 100},
        height=700,
        barmode="stack",
        showlegend=False,
    )
    fig.update_traces(marker_line_color="gray", textposition="outside", opacity=1)

    return fig


@callback(
    Output(
        component_id="team_page_issues_closed_percentage_by_planning_category",
        component_property="figure",
    ),
    [
        Input(component_id="team_page_input_team", component_property="value"),
    ],
)
def team_page_issues_closed_percentage_by_planning_category(team: str):
    if not team:
        return {}

    df = db.filter_issues_by_team(df_team, team)

    fig = px.bar(
        df,
        orientation="v",
        text_auto=True,
        x="sprint",
        y=["issue_planned_done_percent", "issue_unplanned_done_percent"],
        color_discrete_map={
            "issue_planned_done_percent": "seagreen",
            "issue_unplanned_done_percent": "greenyellow",
        },
        range_y=[0, 105],
        title=f"Issues Closed Percentage by Planning Category",
    )

    sprint_first, sprint_last = db.get_first_and_last_sprint(df)
    fig.add_shape(
        x0=sprint_first - 1,
        x1=sprint_last + 1,
        y0=0,
        y1=70,
        fillcolor="red",
        opacity=0.2,
        layer="below",
        line_width=0,
    )
    fig.add_shape(
        x0=sprint_first - 1,
        x1=sprint_last + 1,
        y0=70,
        y1=100,
        fillcolor="green",
        opacity=0.2,
        layer="below",
        line_width=0,
    )

    fig.update_layout(
        xaxis={"dtick": 1},
        yaxis={"dtick": 10},
        margin={"t": 100, "b": 100},
        height=700,
        barmode="group",
        showlegend=True,
    )
    fig.update_traces(
        marker_line_color="gray",
        marker_line_width=1.5,
        textposition="outside",
        opacity=0.9,
    )

    return fig


@callback(
    Output(
        component_id="team_page_issues_closed_count_by_progress_category",
        component_property="figure",
    ),
    [Input(component_id="team_page_input_team", component_property="value")],
)
def team_page_issues_closed_count_by_progress_category(team: str):
    df = db.agg_sum(df_team, ["sprint"])

    if team:
        df = db.agg_sum(df_team, ["sprint", "team"])
        df = db.filter_issues_by_team(df, team)

    fig = px.bar(
        df,
        orientation="v",
        text_auto=True,
        x="sprint",
        y=[
            "issue_planned_done_count",
            "issue_unplanned_done_count",
            "issue_epic_done_count",
        ],
        color_discrete_map={
            "issue_planned_done_count": "seagreen",
            "issue_unplanned_done_count": "greenyellow",
            "issue_epic_done_count": "mediumpurple",
        },
        hover_data=[
            "issue_planned_total_count",
            "issue_unplanned_total_count",
            "issue_epic_total_count",
        ],
        title=f"Issues Closed Count by Progress Category",
    )

    fig.update_layout(
        xaxis={"dtick": 1},
        margin={"t": 100, "b": 100},
        height=700,
        barmode="stack",
        showlegend=True,
    )
    fig.update_traces(marker_line_color="gray", marker_line_width=1, opacity=0.9)

    return fig


@callback(
    Output(
        component_id="team_page_issues_count_by_progress_category", component_property="figure"
    ),
    [Input(component_id="team_page_input_team", component_property="value")],
)
def team_page_issues_count_by_progress_category(team: str):
    df = db.agg_sum(df_team, ["sprint"])

    if team:
        df = db.agg_sum(df_team, ["sprint", "team"])
        df = db.filter_issues_by_team(df, team)

    fig = px.bar(
        df,
        orientation="v",
        text_auto=True,
        x="sprint",
        y=["issue_done_count", "issue_doing_count", "issue_todo_count"],
        color_discrete_map={
            "issue_done_count": "green",
            "issue_doing_count": "gold",
            "issue_todo_count": "indianred",
        },
        title=f"Issues Count by Progress Category",
    )

    fig.update_layout(
        xaxis={"dtick": 1},
        margin={"t": 100, "b": 100},
        height=700,
        barmode="stack",
        showlegend=True,
    )
    fig.update_traces(marker_line_color="gray", marker_line_width=1.5, opacity=0.9)

    return fig
