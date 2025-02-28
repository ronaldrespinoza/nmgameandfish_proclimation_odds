import dash
from dash import dcc, html, Input, Output, State, callback, dash_table, callback_context
import pandas as pd
import re
from components import create_pie_chart_with_raw_value, create_choice_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func
from models import Residency, SuccessPercentages, PercentSuccess, SuccessTotals, Choice, Bag

# Specify the exact order of columns as required, including 'percent_success'
columns_to_retain_in_order = ['Unit', 'top_10_result_type', 'Hunt Code', 'Hunt Dates', 'Bag', 'Hunt Type',
        'Total_all_submissions', 'Total_drawn',
        'total_allocation_of_available_tags', 'percent_success'  # Add the 'percent_success' column explicitly
]

# Define your order
desired_order = [
    'resident_percent_success', 'resident_1stDraw_percent_success', 'resident_2ndDraw_percent_success', 'resident_3rdDraw_percent_success',
    'nonresident_percent_success', 'nonresident_1stDraw_percent_success', 'nonresident_2ndDraw_percent_success', 'nonresident_3rdDraw_percent_success',
    'outfitter_percent_success', 'outfitter_1stDraw_percent_success', 'outfitter_2ndDraw_percent_success', 'outfitter_3rdDraw_percent_success'
]

find_top_10_layout = html.Div([
    dcc.Store(id="top_10_results"),
    html.Div([
        html.H2("Find the top 10 draw odd results by clicking the search buttons below"),
        html.Tr([html.Td(html.Div(create_choice_table()))], style={"width": "100%"}),
        html.Tr([html.Td(html.Div([
            dash_table.DataTable(
                id='top10_result_info_table',
                columns=[],  # Columns will be populated dynamically
                data=[],  # Initially empty data
                row_selectable='multi',  # Allow row selection
                selected_rows=[],  # Default no rows selected
                sort_action='native',  # Enable native sorting on columns
                sort_by=[],  # Default no sorting
            )
        ]) )]),
        html.Div([  # Pie chart for resident success rate
            html.H2("Top 10 Success Rates as pie charts"),
            html.Div(id='top10-pie-chart-container')
        ]),
    ], style={"width": "100%"}),
])



def get_odds_summary(animal_choice_deer=True, animal_choice_elk=False):
    if animal_choice_deer:
        csv_filename = '2024OddsSummary_Deer.csv'
        odds_summary = parser_func("input//odds_reports//{}".format(csv_filename))
    elif animal_choice_elk:
        csv_filename = '2024OddsSummary_Elk.csv'
        odds_summary = parser_func("input//odds_reports//{}".format(csv_filename))
    return pd.DataFrame(odds_summary)


def update_filtered_df_with_percent_success(filtered_df, new_column, total_success, total_submission):
    return get_df_for_pie_chart(filtered_df, new_column, total_success, total_submission)


def create_all_percent_success():
    # Define the column mappings
    column_mappings = [
        ('resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident'),
        ('resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident'),
        ('resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident'),
        ('resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident'),
        ('nonresident_percent_success', 'Nonresident_successfull_draw_total', 'Total_nonresident'),
        ('nonresident_1stDraw_percent_success', 'nonresident_1st_success', '1st_nonresident'),
        ('nonresident_2ndDraw_percent_success', 'nonresident_2nd_success', '2nd_nonresident'),
        ('nonresident_3rdDraw_percent_success', 'nonresident_3rd_success', '3rd_nonresident'),
        ('outfitter_percent_success', 'Outfitter_successfull_draw_total', 'Total_outfitter'),
        ('outfitter_1stDraw_percent_success', 'outfitter_1st_success', '1st_outfitter'),
        ('outfitter_2ndDraw_percent_success', 'outfitter_2nd_success', '2nd_outfitter'),
        ('outfitter_3rdDraw_percent_success', 'outfitter_3rd_success', '3rd_outfitter')
    ]

    # Create the success_dict as a list of dictionaries
    success_dict_list = []

    for new_column, total_success, total_submission in column_mappings:
        # For each mapping, create a dictionary with the required structure
        success_dict = {
            "percent_success": new_column,
            "total_success": total_success,
            "total_submission": total_submission
        }
        
        # Append the dictionary to the list
        success_dict_list.append(success_dict)
    
    return success_dict_list

def apply_all_percent_success_to_df(filtered_df):
    # Get the success_dict_list from the create_all_percent_success function
    success_dict_list = create_all_percent_success()
    # Iterate through each dictionary in success_dict_list and update the filtered_df
    for success_dict in success_dict_list:
        new_column = success_dict["percent_success"]
        total_success = success_dict["total_success"]
        total_submission = success_dict["total_submission"]
        # Update the DataFrame with the calculated percentage for this mapping
        filtered_df = update_filtered_df_with_percent_success(filtered_df, new_column, total_success, total_submission)

    return filtered_df

def get_top_10_percent_success(filtered_df, new_column):
    """
    Get top 10 rows from filtered_df based on the percentage success for a specific new_column.
    """
    top_10_df = filtered_df.nlargest(10, new_column)
    top_10_df = top_10_df.drop_duplicates(subset=['Hunt Code', 'Licenses', 'Bag'])  # Remove duplicates
    return top_10_df

def create_top_10_percent_success_dfs(filtered_df):
    """
    Create a dictionary of DataFrames, each containing the top 10 largest percent values for each new_column.
    """
    success_dict_list = create_all_percent_success()  # Get the list of dictionaries
    # Dictionary to store the top 10 DataFrames for each new_column
    top_10_dfs = {}

    # Iterate over each dictionary in success_dict_list
    for success_dict in success_dict_list:
        new_column = success_dict["percent_success"]

        # Get the top 10 DataFrame for this new_column
        top_10_df = get_top_10_percent_success(filtered_df, new_column)

        # Store the top 10 DataFrame in the dictionary with the column name as the key
        top_10_dfs[new_column] = top_10_df

    return top_10_dfs  # Return the dictionary of DataFrames


def get_data(animal_choice_deer, animal_choice_elk, proclamation_results):
    query_result_df = get_odds_summary(animal_choice_deer, animal_choice_elk)
    proclamation_results_df = pd.DataFrame(proclamation_results)
    return query_result_df, proclamation_results_df


def merge_and_process_data(query_result_df, proclamation_results_df):
    # Merge the dataframes based on Hunt Code, Licenses, and Bag
    filtered_df = pd.merge(query_result_df, proclamation_results_df, on=['Hunt Code', 'Licenses', 'Bag'], how='inner')
    filtered_df = filtered_df.drop_duplicates(subset=['Hunt Code', 'Licenses', 'Bag'])
    filtered_df = apply_all_percent_success_to_df(filtered_df)  # Assuming this is a function that adds success rates
    return filtered_df


def filter_by_selected_units(filtered_df, unit_number_group):
    if unit_number_group:
        selected_units = [unit.split(' ')[1] for unit in unit_number_group]
        filtered_df = filtered_df[filtered_df['Unit'].apply(lambda x: any(unit in x for unit in selected_units))]
    return filtered_df


def process_top_10_dfs(top_10_dfs):
    top_10_list = []

    # Iterate through the top_10_dfs dictionary and process each DataFrame
    for new_column, top_10_df in top_10_dfs.items():
        # Add the 'percent_success' column to the DataFrame
        top_10_df['percent_success'] = top_10_df[new_column]
        
        # Add the 'top_10_result_type' column with the name of the current column
        top_10_df['top_10_result_type'] = new_column

        # Ensure we select the columns in the specified order, including 'percent_success'
        top_10_df = top_10_df[columns_to_retain_in_order]

        # Convert the DataFrame to a list of dictionaries and extend the top_10_list
        top_10_list.extend(top_10_df.to_dict('records'))

    return top_10_list


def generate_columns_for_datatable():
    # Return the columns in the format needed for the DataTable
    return [{"name": col, "id": col} for col in columns_to_retain_in_order]


def generate_columns_to_retain_by_type(top_10_dfs, include_numeric=True, include_non_numeric=False):
    columns_to_retain = set()  # Using a set to avoid duplicate columns

    # Iterate over each DataFrame in the dictionary
    for new_column, df in top_10_dfs.items():
        # Include numeric columns (e.g., integers, floats)
        if include_numeric:
            columns_to_retain.update(df.select_dtypes(include=['number']).columns.tolist())
        
        # Include non-numeric columns (e.g., strings, dates)
        if include_non_numeric:
            columns_to_retain.update(df.select_dtypes(exclude=['number']).columns.tolist())

    # Manually add 'Unit' to the columns we want to retain
    columns_to_retain.add('Unit')
    
    # Return the columns as a list
    return list(columns_to_retain)


def update_table_based_on_result_type(animal_choice_deer, animal_choice_elk, proclamation_results, 
                                      unit_number_group, selected_result_type):
    # Process the data based on selected result type
    query_result_df, proclamation_results_df = get_data(animal_choice_deer, animal_choice_elk, proclamation_results)
    filtered_df = merge_and_process_data(query_result_df, proclamation_results_df)
    filtered_df = filter_by_selected_units(filtered_df, unit_number_group)

    # Generate the top 10 DataFrames and process them
    top_10_dfs = create_top_10_percent_success_dfs(filtered_df)
    table_data = process_top_10_dfs(top_10_dfs)

    if not table_data:
        print("Error: Table data is empty.")
        return [], []

    # Normalize and filter by the selected result type
    df = pd.DataFrame(table_data)
    df['top_10_result_type'] = df['top_10_result_type'].str.strip().str.lower()
    filtered_data = df[df['top_10_result_type'] == selected_result_type.lower()]

    return generate_columns_for_datatable(), filtered_data.to_dict('records')


def update_table_based_on_hunt_type(animal_choice_deer, animal_choice_elk, proclamation_results, 
                                    unit_number_group, selected_hunt_type):
    # Process the data based on selected hunt type
    query_result_df, proclamation_results_df = get_data(animal_choice_deer, animal_choice_elk, proclamation_results)
    filtered_df = merge_and_process_data(query_result_df, proclamation_results_df)
    filtered_df = filter_by_selected_units(filtered_df, unit_number_group)

    # Generate the top 10 DataFrames and process them
    top_10_dfs = create_top_10_percent_success_dfs(filtered_df)
    table_data = process_top_10_dfs(top_10_dfs)

    if not table_data:
        print("Error: Table data is empty.")
        return [], []

    # Normalize and filter by the selected hunt type
    df = pd.DataFrame(table_data)
    df['Hunt Type'] = df['Hunt Type'].str.strip().str.lower()
    filtered_data = df[df['Hunt Type'] == selected_hunt_type.lower()]

    return generate_columns_for_datatable(), filtered_data.to_dict('records')


def update_table_based_on_search(animal_choice_deer, animal_choice_elk, proclamation_results, unit_number_group):
    # Process the data based on search criteria or unit group selection
    query_result_df, proclamation_results_df = get_data(animal_choice_deer, animal_choice_elk, proclamation_results)
    filtered_df = merge_and_process_data(query_result_df, proclamation_results_df)
    filtered_df = filter_by_selected_units(filtered_df, unit_number_group)

    # Generate the top 10 DataFrames and process them
    top_10_dfs = create_top_10_percent_success_dfs(filtered_df)
    top_10_list = process_top_10_dfs(top_10_dfs)

    return generate_columns_for_datatable(), top_10_list


# Callbacks for finding the top 10 results of the draw
def find_top_10_callbacks(app):
    @app.callback(
        Output('top10_unit_numbers', component_property='options'),
        Input('proclamation_results', 'data')
    )
    def top10_unit_dropdown(proclamation_results):
        return Bag.get_unit_dropdown_from_bag(Bag, 'deer')


    @app.callback(
        [Output('top10_unit_numbers_group', component_property='options'),
        Output('deer_unit_group_button', component_property='n_clicks'),
        Output('elk_unit_group_button',  component_property='n_clicks'),
        Output(component_id='animal_choice_deer_unit_group', component_property='on'),
        Output(component_id='animal_choice_elk_unit_group', component_property='on')],
        [Input(component_id='animal_choice_deer_unit_group', component_property='on'),
        Input(component_id='deer_unit_group_button', component_property='n_clicks'),
        Input(component_id='animal_choice_elk_unit_group', component_property='on'),
        Input(component_id='elk_unit_group_button', component_property='n_clicks')]
    )
    def ensure_only_one_on(animal_choice_deer, n_clicks_deer, animal_choice_elk, n_clicks_elk):
        if animal_choice_deer and not(n_clicks_deer) and n_clicks_elk:
            return Bag.get_unit_dropdown_from_bag(Bag, 'deer'), 1,0, True, False
        elif animal_choice_elk and not(n_clicks_elk) and n_clicks_deer:
            return Bag.get_unit_dropdown_from_bag(Bag, 'elk'), 0,1,False, True
        elif animal_choice_deer and not(n_clicks_deer) and not(n_clicks_elk):
            return Bag.get_unit_dropdown_from_bag(Bag, 'deer'), 1,0, True, False
        elif animal_choice_elk and not(n_clicks_elk) and not(n_clicks_deer):
            return Bag.get_unit_dropdown_from_bag(Bag, 'elk'), 0,1, False, True
        else:
            return {},0,0,False,False
        

    @app.callback(
        Output('top10-pie-chart-container', 'children'),
        [Input('top10_result_info_table', 'selected_rows'),
        Input('top10_result_info_table', 'data')]
    )
    def generate_pie_charts_on_row_click(selected_rows, table_data):
        # If no row is selected, do nothing
        if not selected_rows:
            return html.Div("Please select one or more Hunt Codes from the table.")
        
        # Convert table data to DataFrame
        df = pd.DataFrame(table_data)

        # Check if 'percent_success' column exists
        if 'percent_success' not in df.columns:
            return html.Div("The 'percent_success' column is missing from the data.")

        pie_charts_for_selected_rows = []

        # Loop through each selected row index
        for selected_row in selected_rows:
            selected_row_index = selected_row  # Assuming it's 0-indexed, adjust if needed
            selected_hunt_code = df.iloc[selected_row_index]['Hunt Code']  # Retrieve Hunt Code

            # Filter the DataFrame by the selected hunt code
            filtered_df = df[df['Hunt Code'] == selected_hunt_code]

            if filtered_df.empty:
                pie_charts_for_selected_rows.append(html.Div(f"No data available for Hunt Code {selected_hunt_code}."))
                continue

            # Get the 'percent_success' value for the selected hunt code (from the first row)
            row = filtered_df.iloc[0]  # We can use the first row since they are all the same Hunt Code
            success_value = row['percent_success']  # Access the 'percent_success' column directly

            # Check if the success_value is valid for pie chart creation (non-null, non-zero)
            if pd.notnull(success_value) and success_value != 0:
                pie_charts_for_selected_rows.append(
                    html.Div(
                        dcc.Graph(
                            figure=create_pie_chart_with_raw_value(
                                row, 'percent_success', 'Success'
                            )
                        ),
                        style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}
                    )
                )
            else:
                pie_charts_for_selected_rows.append(html.Div(f"No pie chart available for Hunt Code {selected_hunt_code} due to invalid data."))

        # Return the pie chart(s) for the selected rows
        return html.Div(children=pie_charts_for_selected_rows)


    @app.callback(
        Output('top10_result_type_dropdown', 'options'),
        Output('top10_hunt_type_dropdown', 'options'),
        [Input('search_top_10_unit_group', 'n_clicks'),
        Input('top10_result_info_table', 'data')],
        prevent_initial_call=True
    )
    def update_dropdown_options(search_top_10_unit_group, data_table):
        # Get the context of the callback to see which input triggered the callback
        ctx = callback_context

        # If no input triggered, return empty values (or handle it as needed)
        if not ctx.triggered:
            return [], []
        
        # Get the ID of the component that triggered the callback
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id in ['search_top_10_unit_group']:
                top_10_result_type_list = []
                top_10_hunt_type_list = []
                for entry in data_table:
                    top_10_result_type_list.append(entry['top_10_result_type'])
                    top_10_hunt_type_list.append(entry['Hunt Type'])
                # Extract the result types based on the available data
                result_types = [item for item in desired_order if item in set(top_10_result_type_list)]
                hunt_type_types = list(set(top_10_hunt_type_list))
                result_options = [{'label': result_type, 'value': result_type} for result_type in result_types]
                hunt_type_options = [{'label': hunt_type, 'value': hunt_type} for hunt_type in hunt_type_types]

                return result_options, hunt_type_options

        return [], []  # Return empty options if no valid input or search hasn't been clicked yet


    @app.callback(
        [Output('top10_result_info_table', 'columns'),
        Output('top10_result_info_table', 'data')],
        [Input('animal_choice_deer_unit_group', 'on'),
        Input('animal_choice_elk_unit_group', 'on'),
        Input('proclamation_results', 'data'),
        Input('search_top_10_unit_group', 'n_clicks'),
        Input('top10_unit_numbers_group', 'value'),
        Input('top10_result_type_dropdown', 'value'),
        Input('top10_hunt_type_dropdown', 'value')]  # Keep only relevant inputs
    )
    def find_top_10_unit_group(animal_choice_deer, animal_choice_elk, proclamation_results,
                                search_top_10_unit_group, unit_number_group, selected_result_type, selected_hunt_type):
        ctx = callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # If the 'top10_result_type_dropdown' is triggered
        if triggered_id == 'top10_result_type_dropdown' and selected_result_type:
            return update_table_based_on_result_type(animal_choice_deer, animal_choice_elk, proclamation_results,
                                                    unit_number_group, selected_result_type)

        # If the 'top10_hunt_type_dropdown' is triggered
        elif triggered_id == 'top10_hunt_type_dropdown' and selected_hunt_type:
            return update_table_based_on_hunt_type(animal_choice_deer, animal_choice_elk, proclamation_results,
                                                unit_number_group, selected_hunt_type)

        # If the 'search_top_10_unit_group' or 'top10_unit_numbers_group' is triggered
        elif triggered_id in ['search_top_10_unit_group', 'top10_unit_numbers_group']:
            if search_top_10_unit_group and proclamation_results:
                return update_table_based_on_search(animal_choice_deer, animal_choice_elk, proclamation_results,
                                                    unit_number_group)

        # Return unchanged if no conditions match
        return dash.no_update, dash.no_update















