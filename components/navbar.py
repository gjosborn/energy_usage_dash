from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc

# Navbar component
def create_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
            dbc.NavItem(dbc.NavLink("Forecasting", href="/forecasting")),
        ],
    
        brand="Energy Consumption Analytics",
        brand_href="/",
        color="slategray",
        dark=True,
)