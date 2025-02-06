from dash import html
import dash_daq as daq

def create_choice_table():
    row1 = html.Tr([html.Td("Get top 10 odds for Deer"),
                    html.Td([
                        html.Button('Top 10 Deer', id='my-button', n_clicks=0)
                        ])
                    ])
    row2 = html.Tr([html.Td("Get top 10 odds for Elk"),
                    html.Td([
                        html.Button('Top 10 Elk', id='my-button', n_clicks=0)
                        ])
                    ])
    row3 = html.Tr([html.Td("Get top 10 odds based on Unit"),
                    html.Td([
                        html.Button('Top 10 in Unit', id='my-button', n_clicks=0)
                        ])
                    ])
    table_body = [html.Tbody([row1]),
                  html.Tbody([row2]),
                  html.Tbody([row3])]
    table = html.Table(table_body, style={'vertical-align': 'left', 'text-align':'end'})

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