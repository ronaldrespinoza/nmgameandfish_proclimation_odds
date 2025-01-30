import csv
import sys
import enum
import time
import proclamation_scraper as scraper
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
import base64
import plotly.graph_objects as go


class Choice():
    def __init__(self, first_choice, second_choice, third_choice, fourth_choice, total_chosen):
        self._first_choice = first_choice
        self._second_choice = second_choice
        self._third_choice = third_choice
        self._fourth_choice = fourth_choice
        self._total_chosen = total_chosen

    @property
    def first_choice(self):
        return self._first_choice

    @first_choice.setter
    def first_choice(self, value):
        self._first_choice = value
    
    @property
    def second_choice(self):
        return self._second_choice

    @second_choice.setter
    def second_choice(self, value):
        self._second_choice = value
    
    @property
    def third_choice(self):
        return self._third_choice

    @third_choice.setter
    def third_choice(self, value):
        self._third_choice = value
    
    @property
    def fourth_choice(self):
        return self._fourth_choice

    @fourth_choice.setter
    def fourth_choice(self, value):
        self._fourth_choice = value
    
    @property
    def total_chosen(self):
        return self._total_chosen

    @total_chosen.setter
    def total_chosen(self, value):
        self._total_chosen = value


class SuccessTotals():
    def __init__(self, resident_total, non_resident_total, outfitter_total):
        self._resident_total = resident_total
        self._non_resident_total = non_resident_total
        self._outfitter_total = outfitter_total

    @property
    def resident_total(self):
        return self._resident_total

    @resident_total.setter
    def resident_total(self, value):
        self._resident_total = value
    
    @property
    def non_resident_total(self):
        return self._non_resident_total

    @non_resident_total.setter
    def non_resident_total(self, value):
        self._non_resident_total = value
    
    @property
    def outfitter_total(self):
        return self._outfitter_total

    @outfitter_total.setter
    def outfitter_total(self, value):
        self._outfitter_total = value


class SuccessPercentages():
    def __init__(self, resident_percentages, non_resident_percentages, outfitter_percentages):
        self._resident_percentages = resident_percentages
        self._non_resident_percentages = non_resident_percentages
        self._outfitter_percentages = outfitter_percentages

    @property
    def resident_percentages(self):
        return self._resident_percentages

    @resident_percentages.setter
    def resident_percentages(self, value):
        self._resident_percentages = value
    
    @property
    def non_resident_percentages(self):
        return self._non_resident_percentages

    @non_resident_percentages.setter
    def non_resident_percentages(self, value):
        self._non_resident_percentages = value
    
    @property
    def outfitter_percentages(self):
        return self._outfitter_percentages

    @outfitter_percentages.setter
    def outfitter_percentages(self, value):
        self._outfitter_percentages = value


class Residency():
    def __init__(self, resident, non_resident, outfitter):
        self._resident = resident
        self._non_resident = non_resident
        self._outfitter = outfitter

    @property
    def resident(self):
        return self._resident

    @resident.setter
    def resident(self, value):
        self._resident = value
    
    @property
    def non_resident(self):
        return self._non_resident

    @non_resident.setter
    def non_resident(self, value):
        self._non_resident = value
    
    @property
    def outfitter(self):
        return self._outfitter

    @outfitter.setter
    def outfitter(self, value):
        self._outfitter = value




class Bag(enum.Enum):
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"\'{self.value}\'"
    
    def get_deer_bags():
        return ['A', 'ES', 'ESWTD', 'FAD', 'FAMD', 'FAWTD']
    
    def get_deer_bag_drop_down(self):
        bag_options = []
        for item in self.get_deer_bags():
            bag_options.append({'label': '{}'.format(item), 'value': item})
        return bag_options

    def get_elk_bags():
        return ['A', 'APRE/6', 'APRE/6/A', 'ES', 'MB', 'MB/A']
    
    def get_elk_bag_drop_down(self):
        bag_options = []
        for item in self.get_elk_bags():
            bag_options.append({'label': '{}'.format(item), 'value': item})
        return bag_options

    FAMD = "FAMD"
    FAWD = "FAWD"
    ESWTD = "ESWTD"
    FAD = "FAD"
    A = "A"
    ES = "ES"
    MB = "MB"


class GetListFromQuery():
    def get_no_private(some_list):
        return [d for d in some_list if not(d["Unit/Description"].__contains__("private land only"))]
    
    def get_no_youth(some_list):
        return [d for d in some_list if not(d["Unit/Description"].__contains__("youth only"))]
    
    def get_TotalAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["T"] <= d["Licenses"])]
    
    def get_1stAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["1st"] <= d["Licenses"])]
    
    def get_2ndAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["2nd"] <= d["Licenses"])]
    
    def get_3rdAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["3rd"] <= d["Licenses"])]
    
    def get_unit_by_number(some_list, unit_number):
        return [d for d in some_list if (d["Unit/Description"].__contains__("{}".format(unit_number)))]
    
    def get_all_by_bag(some_list, bag):
        return [d for d in some_list if (d["Bag"].__contains__("{}".format(bag)))]
    
    
def filter_on_boolean_switches(filtered_list, residency_choice, choice_result, success_total, success_percentage):
    df = pd.DataFrame(filtered_list)
    
    try:
        if not(residency_choice.resident):
            df = df.drop(columns=["1st_resident", "2nd_resident", "3rd_resident", "Total_resident"])
        if not(residency_choice.non_resident):
            df = df.drop(columns=["1st_non_resident", "2nd_non_resident", "3rd_non_resident", "Total_non_resident"])
        if not(residency_choice.outfitter):
            df = df.drop(columns=["1st_outfitter", "2nd_outfitter", "3rd_outfitter", "Total_outfitter"])
    except KeyError:
        pass

    try:
        if not(choice_result.first_choice):
            df = df.drop(columns=["1st_choice_total_submissions"])
        if not(choice_result.second_choice):
            df = df.drop(columns=["2nd_choice_total_submissions"])
        if not(choice_result.third_choice):
            df = df.drop(columns=["3rd_choice_total_submissions"])
        if not(choice_result.total_chosen):
            df = df.drop(columns=["Total_all_submissions"])
    except KeyError:
        pass

    try:
        if not(success_total.resident_total):
            df = df.drop(columns=["Resident_successfull_draw_total"])
        if not(success_total.non_resident_total):
            df = df.drop(columns=["Nonresident_successfull_draw_total"])
        if not(success_total.outfitter_total):
            df = df.drop(columns=["Outiftter_successfull_draw_total"])
    except KeyError:
        pass

    try:
        if not(success_percentage.resident_percentages):
            df = df.drop(columns=["Resident_percentage_allocation"])
        if not(success_percentage.non_resident_percentages):
            df = df.drop(columns=["nonresident_percentage_allocation"])
        if not(success_percentage.outfitter_percentages):
            df = df.drop(columns=["outfitter_percentage_allocation"])
    except KeyError:
        pass

    return df.to_dict('records')

def query_odds(odds_summary, unit_number, bag_choice, residency_choice, choice_result, success_total, success_percentage, add_private, add_youth,):
    filtered_list = []
    for unit_num in unit_number:
        filtered_list = GetListFromQuery.get_unit_by_number(odds_summary, unit_num)
    for bag in bag_choice:
        filtered_list = GetListFromQuery.get_all_by_bag(filtered_list, bag)
    if not(add_private):
        filtered_list = GetListFromQuery.get_no_private(filtered_list)
    if not(add_youth):
        filtered_list = GetListFromQuery.get_no_youth(filtered_list)

    filtered_list = filter_on_boolean_switches(filtered_list, residency_choice, choice_result, success_total, success_percentage)
    return filtered_list

def new_odds_summary_dict():
    odds_summary_dict = {"Hunt Code": "",
                        "Unit/Description": "",
                        "Bag": "",
                        "Licenses": "",
                        "1st_choice_total_submissions": "",
                        "2nd_choice_total_submissions": "",
                        "3rd_choice_total_submissions": "",
                        "Total_all_submissions": "",
                        "1st_resident": "",
                        "2nd_resident": "",
                        "3rd_resident": "",
                        "Total_resident":"",
                        "1st_non_resident": "",
                        "2nd_non_resident": "",
                        "3rd_non_resident": "",
                        "Total_non_resident":"",
                        "1st_outfitter": "",
                        "2nd_outfitter": "",
                        "3rd_outfitter": "",
                        "Total_outfitter":"",
                        "Resident_successfull_draw_total": "",
                        "Nonresident_successfull_draw_total": "",
                        "Outiftter_successfull_draw_total": "",
                        "Total_drawn": "",
                        "Resident_percentage_allocation":"",
                        "nonresident_percentage_allocation": "",
                        "outfitter_percentage_allocation":"",
                        "total_allocation_of_available_tags": "",
                        "resident_1st_success": "",
                        "resident_2nd_success": "",
                        "resident_3rd_success": "",
                        "resident_4th_success": "",
                        "resident_total_success":"",
                        "nonresident_1st_success": "",
                        "nonresident_2nd_success": "",
                        "nonresident_3rd_success": "",
                        "nonresident_4th_success": "",
                        "nonresident_total_success":"",
                        "outfitter_1st_success": "",
                        "outfitter_2nd_success": "",
                        "outfitter_3rd_success": "",
                        "outfitter_4th_success": "",
                        "outfitter_total_success":""}
    return odds_summary_dict

def parser_func(csv_filename):
    with open(csv_filename, "r") as csv_reader:
        datareader = csv.reader(csv_reader)
        odds_summary = []
        for row in datareader:
            if row[0].__contains__("Hunt Code"):
                next(csv_reader)
            else:
                odds_summary_dict = new_odds_summary_dict()
                for idx, key in enumerate(odds_summary_dict):
                    if idx < 3:
                        odds_summary_dict[key] = row[idx]
                    elif 23 <= idx <= 27:
                        odds_summary_dict[key] = float(row[idx])
                    else:
                        odds_summary_dict[key] = int(row[idx])
                odds_summary.append(odds_summary_dict)
    return odds_summary

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded_string}"

encoded_image = encode_image("C://Users//admin//Documents//NMGF_Hunting//input//Map-New-Mexico-State-Game-Management-Unit-Boundaries.jpg")

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

def unit_dropdown():
    unit_options = []
    idx = 1

    while idx < 60:
        unit_options.append({'label': '{}'.format(idx), 'value': idx})
        idx += 1
    unit_options.append({'label': 'statewide', 'value': 'statewide'})
    return  dbc.Row([
                dbc.Label('Unit Choices:', className="my-label"),
                dbc.Col(
                    dcc.Dropdown(
                        id='unit_number',
                        className='dash-bootstrap',
                        options=unit_options,
                        value="lag_0",
                        multi=True,
                        clearable=True,
                        style={'float': 'left',"width":"200px"}
                    ),
                ),
            ], className="mt-2",)

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
                        id='hunt-dropdown',
                        options=[],
                        value="",
                        multi=False,
                        style={'float': 'left',"width":"200px"}
                    ),
                ),
            ], className="mt-2",)

# # Generate a pie chart for each hunt code
# def create_pie_chart(row, percent_success, draw_choice):
#     return px.pie(
#         names=['Resident {} Success'.format(draw_choice), 'Resident Failure'],
#         values=[row[percent_success], 100 - row['resident_percent_success']],
#         title=f"{row['Hunt Code']} - Resident {draw_choice} Success",
#         hole=0.3
#     )

# Function to create pie charts
def create_pie_chart(row, column, label):
    fig = px.pie(
        names=["Success", "Failure"],
        values=[row[column], 100 - row[column]],
        title=f"{label} - {row['Hunt Code']}",
        hole=0.3
    )
    return fig

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Tr([html.Td(html.Br())]),
    html.Tr([html.Td(html.Div(create_filtering_table()))]),
    html.Tr([html.Td(unit_dropdown())]),
    html.Tr([html.Td(bag_dropdown())]),
    html.Tr([html.Td(hunt_code_dropdown())]),
    html.Tr([html.Td(html.Br())]),
    html.Tr([html.Td(html.Div(id='filtered_result_table'))]),
    html.Div([
        html.Tr([html.Td(html.Div([dcc.Graph(id="percent_odds_graph")])), 
                html.Td(html.Div([dcc.Graph(id="percent_odds_graph_1stDraw")]))]),
        html.Tr([html.Td(html.Div([dcc.Graph(id="percent_odds_graph_2ndDraw")])),
                html.Td(html.Div([dcc.Graph(id="percent_odds_graph_3rdDraw")]))
                ])
    ]),
    # Pie chart for resident success rate
    html.Div([
        html.H2("Resident Success Rates by Hunt Code"),
        html.Div(id='pie-chart-container')  # This will hold the dynamically generated pie charts
    ]),
        html.Td([html.Td("GMU Map"),
                    html.Td([html.Img(src=encoded_image, style={'width': '100%'})])
            ]),
    html.Div(id='output'),
    dcc.Store(id="query_results")
]


@app.callback(
    Output("hunt-dropdown", "options"), 
    Input('query_results', 'data'))
def generate_hunt_dropdown(query_values):

    if query_values != "":
        # Convert the data to a DataFrame
        df = pd.DataFrame.from_dict(query_values, orient='index')

        #create the hunt_code_dropdown list of available selections
        return [{'label': row['Hunt Code'], 'value': row['Hunt Code']} for _, row in df.iterrows()]
    else:
        return []

def get_df_for_pie_chart(df, new_column, total_column, factored_column):
    df[new_column] = df[total_column] / df[factored_column] * 100
    return df

# Callback to update merged data and pie charts based on selected unit
@app.callback(
    [Output('merged-data', 'children'),
     Output('pie-chart-container', 'children')],
    [Input('unit-dropdown', 'value'),
     Input('query_results', 'data'),
     Input('proclamation_results', 'data'),]
)
def update_dashboard(selected_unit, dataframe1, dataframe2):
    # Merge the two dataframes on 'Hunt Code' and 'Licenses' (inner join)
    merged_df = pd.merge(dataframe1, dataframe2, on=['Hunt Code', 'Licenses'], how='inner')
    # Filter the merged DataFrame based on the selected unit
    filtered_df = merged_df[merged_df['Unit/Description'] == selected_unit]

    # Calculate the percentage values before generating pie charts
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')

    # Generate the table of merged Data
    merged_table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in filtered_df.columns])] +
        # Rows
        [html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns]) for i in range(len(filtered_df))]
    )

    # Create a list to store pie chart components (dcc.Graph)
    pie_chart_components = []

    # Loop through each unique Hunt Code to generate pie charts for each row
    for hunt_code in filtered_df['Hunt Code'].unique():
        # Filter rows with the current Hunt Code
        hunt_code_df = filtered_df[filtered_df['Hunt Code'] == hunt_code]

        # Create a row for the pie charts for each of the percentage columns
        pie_charts_for_this_hunt_code = []
        
        for _, row in hunt_code_df.iterrows():
            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_percent_success', 'Overall Success')))
            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_1stDraw_percent_success', '1st Draw Success')))
            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_2ndDraw_percent_success', '2nd Draw Success')))
            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_3rdDraw_percent_success', '3rd Draw Success')))
        
        # Add pie charts for the current hunt code to the list
        pie_chart_components.append(html.Div(
            children=pie_charts_for_this_hunt_code,
            style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-bottom': '20px'}
        ))

    return merged_table, pie_chart_components


@app.callback(
    Output("percent_odds_graph", "figure"),
    Output("percent_odds_graph_1stDraw", "figure"),
    Output("percent_odds_graph_2ndDraw", "figure"),
    Output("percent_odds_graph_3rdDraw", "figure"),
    Input('query_results', 'data'),
    Input('hunt-dropdown', 'value'))
def generate_charts(query_values, selected_hunt_code):

    if query_values != "":
        # Convert the data to a DataFrame
        df = pd.DataFrame.from_dict(query_values, orient='index')
        try:
            df_fig_1 = get_df_for_pie_chart(df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
            df_fig_2 = get_df_for_pie_chart(df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
            df_fig_3 = get_df_for_pie_chart(df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
            df_fig_4 = get_df_for_pie_chart(df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')
        except KeyError:
            return ({}, {}, {}, {})
        # Create individual pie charts for each hunt code
        # for idx, row in df.iterrows():
        try:
            row_fig_1 = df_fig_1[df_fig_1['Hunt Code'] == selected_hunt_code].iloc[0]
            row_fig_2 = df_fig_2[df_fig_2['Hunt Code'] == selected_hunt_code].iloc[0]
            row_fig_3 = df_fig_3[df_fig_3['Hunt Code'] == selected_hunt_code].iloc[0]
            row_fig_4 = df_fig_4[df_fig_4['Hunt Code'] == selected_hunt_code].iloc[0]
        except IndexError:
            return ({}, {}, {}, {})
        fig1 = create_pie_chart(row_fig_1, "resident_percent_success", "overall")
        fig2 = create_pie_chart(row_fig_2, "resident_1stDraw_percent_success", "1stDraw")
        fig3 = create_pie_chart(row_fig_3, "resident_2ndDraw_percent_success", "2ndDraw")
        fig4 = create_pie_chart(row_fig_4, "resident_3rdDraw_percent_success", "3rdDraw")
        return fig1, fig2, fig3, fig4
    else:
        return ({}, {}, {}, {})


@app.callback(
    [Output('bag_choice', component_property='options'),
     Output('deer_button', component_property='n_clicks'),
     Output('elk_button',  component_property='n_clicks'),
     Output(component_id='animal_choice_deer', component_property='on'),
     Output(component_id='animal_choice_elk', component_property='on')],
    [Input(component_id='animal_choice_deer', component_property='on'),
     Input(component_id='deer_button', component_property='n_clicks'),
    Input(component_id='animal_choice_elk', component_property='on'),
    Input(component_id='elk_button', component_property='n_clicks')]
)
def ensure_only_one_on(animal_choice_deer, n_clicks_deer, animal_choice_elk, n_clicks_elk):
    if animal_choice_deer and not(n_clicks_deer) and n_clicks_elk:
        return Bag.get_deer_bag_drop_down(Bag), 1,0, True, False #, 'deer_choice deer_btn_n:{}  elk_btn_n:{}'.format(n_clicks_deer, n_clicks_elk)
    elif animal_choice_elk and not(n_clicks_elk) and n_clicks_deer:
        return Bag.get_elk_bag_drop_down(Bag), 0,1,False, True#, 'elk_choice deer_btn_n:{}  elk_btn_n:{}'.format(n_clicks_deer, n_clicks_elk)
    elif animal_choice_deer and not(n_clicks_deer) and not(n_clicks_elk):
        return Bag.get_deer_bag_drop_down(Bag), 1,0, True, False#, 'deer_choice deer_btn_n:{}  elk_btn_n:{}'.format(n_clicks_deer, n_clicks_elk)
    elif animal_choice_elk and not(n_clicks_elk) and not(n_clicks_deer):
        return Bag.get_elk_bag_drop_down(Bag), 0,1, False, True#, 'elk_choice deer_btn_n:{}  elk_btn_n:{}'.format(n_clicks_deer, n_clicks_elk)
    else:
        return {},0,0,False,False#,""




@callback(
    Output(component_id='filtered_result_table', component_property='children'),
    Output('output', 'children'),
    Output("query_results", "data"),
    Output("proclamation_results", "data"),
    Input(component_id='animal_choice_deer', component_property='on'),
    Input(component_id='animal_choice_elk', component_property='on'),
    Input(component_id='add_private', component_property='on'),
    Input(component_id='add_youth', component_property='on'),
    Input(component_id='show_results_for_resident', component_property='on'),
    Input(component_id='show_results_for_nonresident', component_property='on'),
    Input(component_id='show_results_for_outfitter', component_property='on'),
    Input(component_id='show_results_for_1stchoice', component_property='on'),
    Input(component_id='show_results_for_2ndchoice', component_property='on'),
    Input(component_id='show_results_for_3rdchoice', component_property='on'),
    Input(component_id='show_results_for_4thchoice', component_property='on'),
    Input(component_id='show_results_for_totals', component_property='on'),
    Input(component_id='show_resident_successfull_draw_total', component_property='on'),
    Input(component_id='show_nonresident_successfull_draw_total', component_property='on'),
    Input(component_id='show_outfitter_successfull_draw_total', component_property='on'),
    Input(component_id='show_resident_successfull_draw_percentage', component_property='on'),
    Input(component_id='show_nonresident_successfull_draw_percentage', component_property='on'),
    Input(component_id='show_outfitter_successfull_draw_percentage', component_property='on'),
    Input(component_id='unit_number', component_property='value'),
    Input(component_id='bag_choice', component_property='value'),
)
def update_output_div(animal_choice_deer, animal_choice_elk,
                      add_private, add_youth,
                      show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter,
                      show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals,
                      show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total,
                      show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage,
                      unit_number, bag_choice):
    csv_filename = ""
    odds_summary = []
    query_result = None

    residency_choice = Residency(show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter)
    choice_result = Choice(show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals)
    success_total = SuccessTotals(show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total)
    success_percentage = SuccessPercentages(show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage)

    if animal_choice_deer:
        csv_filename = '2024OddsSummary_Deer.csv'
        proclamation_df = scraper.scrape_for_deer()
    elif animal_choice_elk:
        csv_filename = '2024OddsSummary_Elk.csv'
        proclamation_df = scraper.scrape_for_elk()
    elif csv_filename == "":
        return "", "", ""
        # return ""

    odds_summary = parser_func("input/{}".format(csv_filename))
    if unit_number is None:
        return "", "you must choose a unit number", ""
        # return "", query_result
    elif bag_choice is None:
        return "", "you must choose a bag", ""
        # return "", query_result
    else:
        try:
            query_result = query_odds(odds_summary, unit_number, bag_choice, residency_choice, choice_result, success_total, success_percentage, add_private, add_youth,)
            
        except TypeError as error:
            # return "", "{}".format(error)
            return "", query_result
        # return dash_table.DataTable(data=query_result, page_size=10), "", query_result#"{}".format(query_result)

    try:
        df_display = pd.DataFrame(query_result)
        df_display = df_display.drop(columns=["resident_1st_success"])
        df_display = df_display.drop(columns=["nonresident_1st_success"])
        df_display = df_display.drop(columns=["outfitter_1st_success"])
        df_display = df_display.drop(columns=["resident_2nd_success"])
        df_display = df_display.drop(columns=["nonresident_2nd_success"])
        df_display = df_display.drop(columns=["outfitter_2nd_success"])
        df_display = df_display.drop(columns=["resident_3rd_success"])
        df_display = df_display.drop(columns=["nonresident_3rd_success"])
        df_display = df_display.drop(columns=["outfitter_3rd_success"])
        df_display = df_display.drop(columns=["resident_4th_success"])
        df_display = df_display.drop(columns=["nonresident_4th_success"])
        df_display = df_display.drop(columns=["outfitter_4th_success"])
        df_display = df_display.drop(columns=["resident_total_success"])
        df_display = df_display.drop(columns=["nonresident_total_success"])
        df_display = df_display.drop(columns=["outfitter_total_success"])
    except KeyError:
        pass
    
    return dash_table.DataTable(data=df_display.to_dict('records'), page_size=10), "", {index: value for index, value in enumerate(query_result)}, {index: value for index, value in enumerate(proclamation_df)}



# Run the app
if __name__ == '__main__':
    app.run(debug=True)

