import proclamation_scraper as scraper
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import query_odds as query_odds
from residency import Residency
import pandas as pd
from success_percentages import SuccessPercentages
from success_totals import SuccessTotals
from choice import Choice
from bag import Bag

# Initialize the app
app = Dash()

# App layout
app.layout = [
    dcc.Interval(
        id='interval-component', 
        interval=5 * 1000,  # in milliseconds (1ms means it runs right after load)
        n_intervals=0,  # Runs once when the page loads
        disabled=False  # Makes sure the interval is active right after page load
    ),
    dcc.Store(id="proclamation_results", storage_type='session', data={}),
    dcc.Store(id="odds_summary", storage_type='session', data={}),
    # dcc.Store(id="proclamation_results"),
    # dcc.Store(id="odds_summary"),
    dcc.Store(id="query_results"),
    html.Tr([html.Td(html.Br())]),
    html.Tr([html.Td(html.Div(query_odds.create_filtering_table()))]),
    html.Tr([html.Td(query_odds.unit_dropdown())]),
    html.Tr([html.Td(query_odds.bag_dropdown())]),
    html.Tr([html.Td(query_odds.hunt_code_dropdown())]),
    html.Tr([html.Td(html.Br())]),
    html.Tr([html.Td(html.Div(id='result_info_table'))]),
    # Pie chart for resident success rate
    html.Div([
        html.H2("Resident Success Rates by Hunt Code"),
        html.Div(id='pie-chart-container')  # This will hold the dynamically generated pie charts
    ]),
        html.Td([html.Td("GMU Map"),
                    html.Td([html.Img(src=query_odds.encoded_image, style={'width': '100%'})])
            ]),
    html.Div(id='output'),
]


# Callback that runs once after the page loads
@app.callback(
    Output("proclamation_results", "data"),
    Input('interval-component', 'n_intervals'),
    State('proclamation_results', 'data')  # Check if data is already in the store
)
def on_page_load_proclamation_results(n, proclamation_results):
    # Debugging log
    # # print(f"on_page_load triggered, n_intervals: {n}, proclamation_results: {proclamation_results}")

    if n == 1:  # The first interval (immediately after the page loads)
        if not proclamation_results:  # If no data is present in store Scrape data
            deer_proclamation_df = scraper.scrape_for_deer()
            elk_proclamation_df = scraper.scrape_for_elk()
            # return deer_proclamation_df.append(elk_proclamation_df, ignore_index=False, sort=False).to_dict("dict") # Return data to store
            return pd.concat([deer_proclamation_df, elk_proclamation_df], ignore_index=True).to_dict("dict")
        return proclamation_results # If data exists, just return it (no scraping necessary)
    return proclamation_results  # Return existing data if n_intervals isn't 1# Callback that runs once after the page loads


@app.callback(
    Output("odds_summary", "data"),
    Input('interval-component', 'n_intervals'),
    State('odds_summary', 'data')
)
def on_page_load_odds_summary(n, odds_summary):
    """
    Callback to load odds summary data when page loads or on interval triggers.
    """
    # Debugging log to check what's in odds_summary
    # if odds_summary:
        # print(f"Existing data in store, count: {len(odds_summary)}")
        # for item in odds_summary:
        #     print(item.get('Hunt Code', 'No Hunt Code Found'))
    
    if n == 1:  # On the first interval (just after the page loads)
        if not odds_summary:  # If no data in store, load it
            print("No data in store, loading from CSV...")
            
            # Parsing the CSV data and combining it
            data1 = query_odds.parser_func("input//2024OddsSummary_Deer.csv")
            data2 = query_odds.parser_func("input//2024OddsSummary_Elk.csv")
            
            # print(f"Data from first CSV (Deer) count: {len(data1)}")
            # print(f"Data from second CSV (Elk) count: {len(data2)}")
            
            # Combine data from both CSVs
            odds_summary = data1 + data2
            
            # Debug: Check combined data before returning
            print(f"Combined data count: {len(odds_summary)}")
            return odds_summary  # Return combined data to store
        else:
            print("Data already in store, returning existing data.")
            return odds_summary  # Return existing data

    return odds_summary  # Return existing data if no new interval trigger



# @app.callback(
#     Output("odds_summary", "data"),
#     Input('interval-component', 'n_intervals'),
#     State('odds_summary', 'data')  # Check if data is already in the store
# )
# def on_page_load_odds_summary(n, odds_summary):
#     # Debugging log
#     # # print(f"on_page_load triggered, n_intervals: {n}, odds_summary: {odds_summary}")
#     for item in odds_summary:
#         print(item['Hunt Code'])

#     if n == 1:  # The first interval (immediately after the page loads)
#         if not odds_summary:  # If no data is present in store Scrape data
#             data1 = query_odds.parser_func("input//2024OddsSummary_Deer.csv")
#             data2 = query_odds.parser_func("input//2024OddsSummary_Elk.csv")
#             odds_summary = data1 + data2
#             return odds_summary
#         return odds_summary # If data exists, just return it (no scraping necessary)
#     return odds_summary  # Return existing data if n_intervals isn't 1


@app.callback(
    Output("hunt_dropdown", "options"), 
    Input('query_results', 'data'))
def generate_hunt_dropdown(query_values):

    if query_values != None and query_values !=  {"": ""}:
        # Convert the data to a DataFrame
        df = pd.DataFrame.from_dict(query_values, orient='index')

        #create the hunt_code_dropdown list of available selections
        return [{'label': row['Hunt Code'], 'value': row['Hunt Code']} for _, row in df.iterrows()]
    else:
        return []


# Callback to update merged data and pie charts based on selected unit
@app.callback(
    [Output('pie-chart-container', 'children'),
    Output('result_info_table', 'children'),],
    Input('query_results', 'data'),
    Input('proclamation_results', 'data'),
    Input('hunt_dropdown', 'value'),
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
)
def update_dashboard(dataframe1, dataframe2, selected_hunt_code,
                      show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter,
                      show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals,
                      show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total,
                      show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage,
                     ):
    # # print(f"dataframe1: {dataframe1}")
    # # print(f"dataframe2: {dataframe2}")
    if dataframe1 is not None and dataframe1 != {"": ""} and dataframe2 is not None and dataframe2 != {"": ""}:
        # Merge the two dataframes on 'Hunt Code' and 'Licenses' (inner join)
        df1 = pd.DataFrame.from_dict(dataframe1, orient='index')
        df2 = pd.DataFrame(dataframe2)
        # print(f"df1: {df1.columns}")
        # print(f"df2: {df2.columns}")
        try:

            filtered_df = pd.merge(df1, df2, on=['Hunt Code', 'Licenses', 'Bag', ], how='inner')
            # filtered_df = pd.merge(df1, df2, on=["Unit/Description", "Hunt Type", "Hunt Dates", "Hunt Code", "Fee Type", "Licenses", "Bag"], how='inner')

            # print(f'filtered_df: {filtered_df}')

            # Calculate the percentage values before generating pie charts
            # print("here1")
            filtered_df = query_odds.get_df_for_pie_chart(filtered_df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
            filtered_df = query_odds.get_df_for_pie_chart(filtered_df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
            filtered_df = query_odds.get_df_for_pie_chart(filtered_df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
            filtered_df = query_odds.get_df_for_pie_chart(filtered_df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')
            # print("here2")
            if selected_hunt_code is not None and selected_hunt_code != "":
                filtered_df = filtered_df[filtered_df['Hunt Code'] == selected_hunt_code]
            # Create a list to store pie chart components (dcc.Graph)
            pie_chart_components = []
            # print("here3")
            # Loop through each unique Hunt Code to generate pie charts for each row
            for hunt_code in filtered_df['Hunt Code'].unique():
                # Filter rows with the current Hunt Code
                hunt_code_df = filtered_df[filtered_df['Hunt Code'] == hunt_code]

                # Create a row for the pie charts for each of the percentage columns
                pie_charts_for_this_hunt_code = []
                
                for _, row in hunt_code_df.iterrows():
                    pie_charts_for_this_hunt_code.append(dcc.Graph(figure=query_odds.create_pie_chart(row, 'resident_percent_success', 'Overall Success')))
                    pie_charts_for_this_hunt_code.append(dcc.Graph(figure=query_odds.create_pie_chart(row, 'resident_1stDraw_percent_success', '1st Draw Success')))
                    pie_charts_for_this_hunt_code.append(dcc.Graph(figure=query_odds.create_pie_chart(row, 'resident_2ndDraw_percent_success', '2nd Draw Success')))
                    pie_charts_for_this_hunt_code.append(dcc.Graph(figure=query_odds.create_pie_chart(row, 'resident_3rdDraw_percent_success', '3rd Draw Success')))
                
                # Add pie charts for the current hunt code to the list
                pie_chart_components.append(html.Div(
                    children=pie_charts_for_this_hunt_code,
                    style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-bottom': '20px'}
                ))    
            # print("here4")
            residency_choice = Residency(show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter)
            choice_result = Choice(show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals)
            success_total = SuccessTotals(show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total)
            success_percentage = SuccessPercentages(show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage)
            # print("here5")
            hunt_code_df = query_odds.filter_on_boolean_switches(filtered_df, residency_choice, choice_result, success_total, success_percentage)
            # print("here6")
            hunt_code_df = query_odds.drop_success(hunt_code_df)
            # print(f"hunt_code_df: {hunt_code_df}")
            return pie_chart_components, dash_table.DataTable(data=hunt_code_df.to_dict('records'), page_size=10)
        except KeyError:
            return [None, None]
    else:
        return [None, None]

@app.callback(
    [Output('bag_choice', component_property='options'),
     Output('unit_number', component_property='options'),
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
        return Bag.get_deer_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'deer'), 1,0, True, False
    elif animal_choice_elk and not(n_clicks_elk) and n_clicks_deer:
        return Bag.get_elk_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'elk'), 0,1,False, True
    elif animal_choice_deer and not(n_clicks_deer) and not(n_clicks_elk):
        return Bag.get_deer_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'deer'), 1,0, True, False
    elif animal_choice_elk and not(n_clicks_elk) and not(n_clicks_deer):
        return Bag.get_elk_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'elk'), 0,1, False, True
    else:
        return {},{},0,0,False,False




@callback(
    Output('output', 'children'),
    Output("query_results", "data"),
    Input('odds_summary', 'data'),
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
def update_output_div(odds_summary,
                      add_private, add_youth,
                      show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter,
                      show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals,
                      show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total,
                      show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage,
                      unit_number, bag_choice):
    query_result = None

    residency_choice = Residency(show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter)
    choice_result = Choice(show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals)
    success_total = SuccessTotals(show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total)
    success_percentage = SuccessPercentages(show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage)

    # # print(f"unit_number: {unit_number}")
    if unit_number is None or unit_number == "":
        return "you must choose a unit number", {"": ""}
    else:
        try:
            query_result = query_odds.get_filtered_list(odds_summary, unit_number, bag_choice, residency_choice, choice_result, success_total, success_percentage, add_private, add_youth)
        except TypeError as error:
            return "", {"": ""}

    # # print(query_result)
    return "", {index: value for index, value in enumerate(query_result)}


# Run the app
if __name__ == '__main__':
    app.run(debug=True)