import csv
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
import base64


class GetListFromQuery():
    def get_no_private(some_list):
        return [d for d in some_list if not(d["Unit"].__contains__("private land only"))]
    
    def get_no_youth(some_list):
        return [d for d in some_list if not(d["Unit"].__contains__("youth only"))]
    
    def get_TotalAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["T"] <= d["Licenses"])]
    
    def get_1stAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["1st"] <= d["Licenses"])]
    
    def get_2ndAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["2nd"] <= d["Licenses"])]
    
    def get_3rdAppliedLicenses_LessThan_ActualLicenses(some_list):
        return [d for d in some_list if (d["3rd"] <= d["Licenses"])]
    
    def get_unit_by_number(some_list, unit_number):
        return [d for d in some_list if unit_number.find(d["Unit"]) != -1]
    
    def get_all_by_bag(some_list, bag):
        return [d for d in some_list if (d["Bag"].__contains__("{}".format(bag)))]

def drop_success(result_set):
    try:
        df_display = pd.DataFrame(result_set)
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
        df_display = df_display.drop(columns=["resident_percent_success"])
        df_display = df_display.drop(columns=["resident_1stDraw_percent_success"])
        df_display = df_display.drop(columns=["resident_2ndDraw_percent_success"])
        df_display = df_display.drop(columns=["resident_3rdDraw_percent_success"])
    except KeyError:
        pass
    return df_display


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
    filtered_list = GetListFromQuery.get_unit_by_number(odds_summary, unit_number)
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
                        "Unit": "",
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

# Function to create pie charts
def create_pie_chart(row, column, label):
    fig = px.pie(
        names=["Success", "Failure"],
        values=[row[column], 100 - row[column]],
        title=f"{label} - {row['Hunt Code']} <br> {row['Hunt Dates']} - {row['Hunt Type']}",
        hole=0.3
    )
    return fig

def get_df_for_pie_chart(df, new_column, total_column, factored_column):
    df[new_column] = df[total_column] / df[factored_column] * 100
    return df

