import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
from dash import html, callback, Input, Output
import plotly.express as px
import database as db
from settings import settings, COLOR_CONTINUOUS_SCALE


dash.register_page(__name__)


df_sprints = pd.read_csv(settings["reports_directory"]["sprint"])


sprint_page_input_sprint = dcc.Dropdown(
    options=df_sprints["sprint"].sort_values().unique(), id="sprint_page_input_sprint"
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Label("Team"), sprint_page_input_sprint]),
            ]
        ),
        html.Hr(),
        dbc.Row([dbc.Col(dcc.Graph(figure={}, id="sprint_page_issues_closed_percent_by_sprint"))]),
        html.Hr(),
        dbc.Row([dbc.Col(dcc.Graph(figure={}, id="sprint_page_issues_unplanned_volume"))]),
        html.Hr(),
        dbc.Row([dbc.Col(dcc.Graph(figure={}, id="sprint_issues_count_by_progress_category"))]),
    ]
)


@callback(
    Output(
        component_id="sprint_page_issues_closed_percent_by_sprint",
        component_property="figure",
    ),
    [
        Input(component_id="sprint_page_input_sprint", component_property="value"),
    ],
)
def sprint_page_issues_closed_percent_by_sprint(sprint: int):
    df = db.agg_mean(df_sprints, ["sprint"])

    if sprint:
        df = db.filter_issues_by_sprint(df, sprint)

    fig = px.bar(
        df,
        orientation="v",
        text_auto=True,
        color="issue_done_percent",
        x="sprint",
        y="issue_done_percent",
        range_color=[0, 100],
        range_y=[0, 100],
        color_continuous_scale=COLOR_CONTINUOUS_SCALE,
        title=f"Issues Closed Percent by Team",
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
        showlegend=False,
    )
    fig.update_traces(marker_line_color="gray", textposition="outside", opacity=1)

    return fig


@callback(
    Output(component_id="sprint_page_issues_unplanned_volume", component_property="figure"),
    [Input(component_id="sprint_page_input_sprint", component_property="value")],
)
def sprint_page_issues_unplanned_volume(sprint: str):
    df = db.agg_sum(df_sprints, ["sprint"])

    if sprint:
        df = db.filter_issues_by_sprint(df, sprint)

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
        component_id="sprint_issues_count_by_progress_category",
        component_property="figure",
    ),
    [Input(component_id="sprint_page_input_sprint", component_property="value")],
)
def sprint_issues_count_by_progress_category(sprint: str):
    df = db.agg_sum(df_sprints, ["sprint"])

    if sprint:
        df = db.filter_issues_by_sprint(df, sprint)

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
