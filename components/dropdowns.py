import dash_bootstrap_components as dbc
from dash import dcc

def unit_dropdown():
    return dbc.Row([
        dbc.Label('Unit Choices:', className="my-label"),
        dbc.Col(
            dcc.Dropdown(
                id='unit_number',
                className='dash-bootstrap',
                options={},
                value="",
                multi=False,
                clearable=True,
                style={'float': 'left', "width": "50%"}
            ),
        ),
    ], className="mt-2")


def bag_dropdown():
    return  dbc.Row([
                dbc.Label('Bag Choices:', className="my-label"),
                dbc.Col(
                    dcc.Dropdown(
                        id='bag_choice',
                        className='dash-bootstrap',
                        options={},
                        value="lag_0",
                        multi=True,
                        clearable=True,
                        style={'float': 'left',"width":"200px"}
                    ),
                ),
            ], className="mt-2",)


def hunt_code_dropdown():
    return  dbc.Row([
                dbc.Label('Resident Success Pie Chart by hunt code:', className="my-label"),
                dbc.Col(
                    dcc.Dropdown(
                        id='hunt_dropdown',
                        options=[],
                        value="",
                        multi=False,
                        style={'float': 'left',"width":"200px"}
                    ),
                ),
            ], className="mt-2",)