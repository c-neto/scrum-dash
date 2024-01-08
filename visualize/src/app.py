from dash import html
import dash

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import components


def serve_layout():
    return html.Div([components.navbar, dbc.Container(dash.page_container, class_name="my-2")])


def make_app() -> dash.Dash:
    app = dash.Dash(
        use_pages=True,
        external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME],
        title="Dash app structure",
    )
    app.layout = serve_layout
    return app


def main():
    app = make_app()
    load_figure_template("ZEPHYR")
    app.run_server(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    main()
