from dash import html
import dash_daq as daq
import dash_bootstrap_components as dbc

def create_choice_table():
    row1 = html.Tr([
        html.Td("Get top 10 odds for Deer", style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),
        html.Td([
            dbc.Button('Search', id='search_top_10_deer', n_clicks=0, color="primary", size="sm", className="shadow-btn")
        ], style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),

        html.Td("Get top 10 odds for Elk", style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),
        html.Td([
            dbc.Button('Search', id='search_top_10_elk', n_clicks=0, color="success", size="sm", className="shadow-btn")
        ], style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),

        html.Td("Get top 10 odds based on Unit", style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),
        html.Td([
            dbc.Button('Search', id='search_top_10_unit', n_clicks=0, color="info", size="sm", className="shadow-btn")
        ], style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),

        html.Td("Get top 10 odds based on Weapon Choice", style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"}),
        html.Td([
            dbc.Button('Search', id='search_top_10_hunt_type', n_clicks=0, color="warning", size="sm", className="shadow-btn")
        ], style={"padding-right": "15px", "padding-left": "15px", "padding-top": "10px", "padding-bottom": "10px"})
    ])

    # Define table body
    table_body = html.Tbody([row1])

    # Wrap the table in a div with the responsive class for mobile-friendliness
    table = html.Div(
                    children=[
                        html.Div(
                                children=html.Table(table_body, className="table table-bordered table-striped"), 
                                className="table-responsive"
                                )
                            ]
                        )

    return table


def create_filtering_table():
    row1 = html.Tr([html.Td("Deer"),
                    html.Td([
                        daq.BooleanSwitch(
                            id='animal_choice_deer',
                            on=False,
                        ),
                        html.Button(id='deer_button',n_clicks=0,style={'display': 'none'})
                        ]),
                    html.Td("Elk"),
                    html.Td([
                        daq.BooleanSwitch(
                            id='animal_choice_elk',
                            on=False,
                        ),
                        html.Button(id='elk_button',n_clicks=0,style={'display': 'none'})
                        ]),
                    ])
    row2 = html.Tr([html.Td("Private"),
                    html.Td([
                        daq.BooleanSwitch(
                            id='add_private',
                            on=False,
                        ),
                        ]),
                    html.Td("Youth"),
                    html.Td([
                        daq.BooleanSwitch(
                            id='add_youth',
                            on=False,
                        ),
                        ])
                    ])
    row3 = html.Tr([html.Td("Resident"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_resident',
                            on=False,
                        )),
                    html.Td("Non Resident"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_nonresident',
                            on=False,
                        )),
                    html.Td("Outfitter"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_outfitter',
                            on=False,
                        ))
                    ])
    row4 = html.Tr([html.Td("1st Choice"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_1stchoice',
                            on=False,
                        )),
                    html.Td("2nd Choice"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_2ndchoice',
                            on=False,
                        )),
                    html.Td("3rd Choice"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_3rdchoice',
                            on=False,
                        )),
                    html.Td("4th Choice"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_4thchoice',
                            on=False,
                        )),
                    html.Td("Totals for all Choices"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_results_for_totals',
                            on=False,
                        ))
                    ])
    row5 = html.Tr([html.Td("Success totals Resident"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_resident_successfull_draw_total',
                            on=False,
                        )),
                    html.Td("Success totals Non Resident"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_nonresident_successfull_draw_total',
                            on=False,
                        )),
                    html.Td("Success totals Outfitter"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_outfitter_successfull_draw_total',
                            on=False,
                        )),
                    ])
    row6 = html.Tr([html.Td("Success Percentage Resident"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_resident_successfull_draw_percentage',
                            on=False,
                        )),
                    html.Td("Success Percentage Non Resident"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_nonresident_successfull_draw_percentage',
                            on=False,
                        )),
                    html.Td("Success Percentage Outfitter"),
                    html.Td(
                        daq.BooleanSwitch(
                            id='show_outfitter_successfull_draw_percentage',
                            on=False,
                        )),
                    ])

    table_body = [html.Tbody([row1, row2]), html.Tbody([row3, row5, row6]), html.Tbody([row4])]
    table = html.Table(table_body, style={'vertical-align': 'left', 'text-align':'end'})

    return table