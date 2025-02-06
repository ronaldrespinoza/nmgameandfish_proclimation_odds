import dash_bootstrap_components as dbc
from dash import dcc

def unit_dropdown(width):
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
                style={'float': 'left', "width": width}
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



def available_weapon_dropdown():
    return  dbc.Row([
                dbc.Label('Available weapon:', className="my-label"),
                dbc.Col(
                    dcc.Dropdown(
                        id='weapon_dropdown',
                        options=[],
                        value="",
                        multi=False,
                        style={'float': 'left',"width":"100%"}
                    ),
                ),
            ], className="mt-2",)