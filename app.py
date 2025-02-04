import proclamation_scraper as scraper
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
from query_odds import *
from residency import Residency
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
    dcc.Store(id="proclamation_results", storage_type='local', data={}),
    dcc.Store(id="query_results"),
    html.Tr([html.Td(html.Br())]),
    html.Tr([html.Td(html.Div(create_filtering_table()))]),
    html.Tr([html.Td(unit_dropdown())]),
    html.Tr([html.Td(bag_dropdown())]),
    html.Tr([html.Td(hunt_code_dropdown())]),
    html.Tr([html.Td(html.Br())]),
    html.Tr([html.Td(html.Div(id='result_info_table'))]),
    # Pie chart for resident success rate
    html.Div([
        html.H2("Resident Success Rates by Hunt Code"),
        html.Div(id='pie-chart-container')  # This will hold the dynamically generated pie charts
    ]),
        html.Td([html.Td("GMU Map"),
                    html.Td([html.Img(src=encoded_image, style={'width': '100%'})])
            ]),
    html.Div(id='output'),
]


# Callback that runs once after the page loads
@app.callback(
    Output("proclamation_results", "data"),
    Input('interval-component', 'n_intervals'),
    State('proclamation_results', 'data')  # Check if data is already in the store
)
def on_page_load(n, existing_data):

    if n == 1:  # The first interval (immediately after the page loads)
        if not existing_data:  # If no data is present in store
            deer_proclamation_df = scraper.scrape_for_deer()
            elk_proclamation_df = scraper.scrape_for_elk()
            return deer_proclamation_df.append(elk_proclamation_df, ignore_index=False, sort=False).to_dict("dict")
        return existing_data
    return existing_data  # Return existing data if n_intervals isn't 1


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
    
    if dataframe1 is not None and dataframe1 != {"": ""} and dataframe2 is not None and dataframe2 != {"": ""}:
        # Merge the two dataframes on 'Hunt Code' and 'Licenses' (inner join)
        df1 = pd.DataFrame.from_dict(dataframe1, orient='index')
        df2 = pd.DataFrame(dataframe2)
        try:
            filtered_df = pd.merge(df1, df2, on=['Hunt Code', 'Licenses', 'Bag'], how='inner')

            # Calculate the percentage values before generating pie charts
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')

            if selected_hunt_code is not None and selected_hunt_code != "":
                filtered_df = filtered_df[filtered_df['Hunt Code'] == selected_hunt_code]
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
            
            residency_choice = Residency(show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter)
            choice_result = Choice(show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals)
            success_total = SuccessTotals(show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total)
            success_percentage = SuccessPercentages(show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage)
            hunt_code_df = filter_on_boolean_switches(filtered_df, residency_choice, choice_result, success_total, success_percentage)
            hunt_code_df = drop_success(hunt_code_df)

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
    elif animal_choice_elk:
        csv_filename = '2024OddsSummary_Elk.csv'
    elif csv_filename == "":
        return "", {"": ""}

    odds_summary = parser_func("input/{}".format(csv_filename))
    if unit_number is None:
        return "you must choose a unit number", {"": ""}
    else:
        try:
            query_result = query_odds(odds_summary, unit_number, bag_choice, residency_choice, choice_result, success_total, success_percentage, add_private, add_youth,)
        except TypeError as error:
            return "", {"": ""}

    return "", {index: value for index, value in enumerate(query_result)}


# Run the app
if __name__ == '__main__':
    app.run(debug=True)