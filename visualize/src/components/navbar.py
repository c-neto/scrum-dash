import dash_bootstrap_components as dbc


# component
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Team", href="/team")),
                        dbc.NavItem(dbc.NavLink("Individual", href="/individual")),
                        dbc.NavItem(dbc.NavLink("Area", href="/area")),
                        dbc.NavItem(dbc.NavLink("Sprint Overall", href="/sprint")),
                    ]
                ),
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)
