from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, available_weapon_dropdown, create_pie_chart, create_pie_chart_with_raw_value, encoded_image, create_choice_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, PercentSuccess, SuccessTotals, Choice, Bag

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
                row_selectable='single',  # Allow row selection
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



def get_odds_summary():
    csv_filename = '2024OddsSummary_Deer.csv'
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
            "new_column": new_column,
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
        new_column = success_dict["new_column"]
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
    Create a list of DataFrames, each containing the top 10 largest percent values for each new_column.
    """
    success_dict_list = create_all_percent_success()  # Get the list of dictionaries
    
    # List to store the top 10 DataFrames for each new_column
    top_10_dfs = []

    # Iterate over each dictionary in success_dict_list
    for success_dict in success_dict_list:
        new_column = success_dict["new_column"]
        
        # Get the top 10 DataFrame for this new_column
        top_10_df = get_top_10_percent_success(filtered_df, new_column)
        
        # Append the top 10 DataFrame to the list
        top_10_dfs.append(top_10_df)

    # Concatenate all top 10 DataFrames and drop duplicates
    if len(top_10_dfs) > 0:  # Ensure there is at least one DataFrame to concatenate
        top_10_df_combined = pd.concat(top_10_dfs, ignore_index=True).drop_duplicates(subset=['Hunt Code', 'Licenses', 'Bag'])
    else:
        top_10_df_combined = pd.DataFrame()  # Return an empty DataFrame if no data

    return top_10_df_combined



# Callbacks for finding the top 10 results of the draw
def find_top_10_callbacks(app):
    @app.callback(
        Output('top10_unit_numbers', component_property='options'),
        Input('proclamation_results', 'data')
    )
    def top10_unit_dropdown(proclamation_results):
        return Bag.get_unit_dropdown_from_bag(Bag, 'deer')


    # @app.callback(
    #     Output("top_10_results", "data"), 
    #     Input('top_10_results_deer', 'data'),
    #     Input('top_10_results_elk', 'data'),
    #     Input('top_10_results_unit', 'data'),
    #     Input('top_10_results_hunt_type', 'data'),
    #     allow_duplicate=True)
    # def display_top_10_results(proclamation_results):
    #     return []

    @app.callback(
        Output('top10-pie-chart-container', 'children'),
        [Input('top10_result_info_table', 'selected_rows'),
        Input('proclamation_results', 'data')]
    )
    def generate_pie_charts_on_row_click(selected_rows, proclamation_results):
        # If no row is selected, do nothing
        if not selected_rows:
            return html.Div("Please select a Hunt Code from the table.")

        # Get the selected row's Hunt Code
        selected_row = selected_rows[0]  # Assumes only one row can be selected at a time
        selected_hunt_code = proclamation_results[selected_row]['Hunt Code']  # Retrieve Hunt Code from the selected row
        
        # Convert proclamation results to DataFrame
        proclamation_results_df = pd.DataFrame(proclamation_results)
        
        # Filter the DataFrame by the selected hunt code
        filtered_df = proclamation_results_df[proclamation_results_df['Hunt Code'] == selected_hunt_code]

        if filtered_df.empty:
            return html.Div(f"No data available for Hunt Code {selected_hunt_code}.")

        # Create success_dict list
        success_dict_list = create_all_percent_success()

        # Apply percentage calculations
        filtered_df = apply_all_percent_success_to_df(filtered_df)

        pie_charts_for_this_hunt_code = []

        # Loop through the success_dict list to dynamically generate pie charts
        for success_dict in success_dict_list:
            new_column = success_dict["new_column"]
            label = success_dict["new_column"].replace("_percent_success", " Success")  # Creating a label for the pie chart

            # Loop through the rows to create pie charts
            for _, row in filtered_df.iterrows():
                pie_charts_for_this_hunt_code.append(
                    dcc.Graph(figure=create_pie_chart_with_raw_value(row, new_column, label))
                )

        if not pie_charts_for_this_hunt_code:
            return html.Div(f"No pie charts available for Hunt Code {selected_hunt_code}.")
        
        return html.Div(
            children=pie_charts_for_this_hunt_code,
            style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-bottom': '20px'}
        )


    @app.callback(
        [Output('top10_result_info_table', 'columns'),
        Output('top10_result_info_table', 'data')],
        [Input('proclamation_results', 'data'),
        Input('search_top_10_deer', 'n_clicks'),
        Input('top10_unit_numbers', 'value')],
        prevent_initial_call=True
    )
    def find_top_10_deer(proclamation_results, search_top_10_deer, unit_number):
        # Only proceed if the button is clicked and the data is not None
        if search_top_10_deer and proclamation_results is not None:
            try:
                query_result_df = get_odds_summary()
                proclamation_results_df = pd.DataFrame(proclamation_results)

                # Merge the dataframes based on 'Hunt Code', 'Licenses', 'Bag'
                filtered_df = pd.merge(query_result_df, proclamation_results_df, on=['Hunt Code', 'Licenses', 'Bag'], how='inner')

                # Check for duplicates after merge and remove them
                filtered_df = filtered_df.drop_duplicates(subset=['Hunt Code', 'Licenses', 'Bag'])
                filtered_df = apply_all_percent_success_to_df(filtered_df)

                # Create a list of dataframes containing the top 10 largest percentages found
                top_10_dfs_list = create_top_10_percent_success_dfs(filtered_df)

                # Apply necessary filters to the dataframe
                residency_choice = Residency(False, False, False)
                choice_result = Choice(False, False, False, False, False)
                success_total = SuccessTotals(False, False, False)
                success_percentage = SuccessPercentages(False, False, False)
                percent_success = PercentSuccess(True, False, False, False,True, False, False, False,True, False, False, False)

                hunt_code_df = filter_on_boolean_switches(top_10_dfs_list, residency_choice, choice_result, success_total, success_percentage, percent_success)
                hunt_code_df = drop_success(hunt_code_df)
                hunt_code_df = hunt_code_df.drop(columns=["Unit/Description"])

                # Dynamically generate columns from the DataFrame
                columns = [{"name": col, "id": col} for col in hunt_code_df.columns]

                # Return columns and data to be displayed in the DataTable
                return columns, hunt_code_df.to_dict('records')

            except Exception as e:
                print(f"Error: {e}")
                return [], []  # Return empty columns and data in case of error

        # Return empty columns and data if the search button isn't clicked or data is invalid
        return [], []



    
    # @app.callback(
    #     Output("top_10_results_elk", "data"), 
    #     Input('proclamation_results', 'data'),
    #     Input(component_id='unit_number', component_property='value'),
    #     allow_duplicate=True)
    # def find_top_10_elk(proclamation_results):
    #     return []
    
    # @app.callback(
    #     Output("top_10_results_unit", "data"), 
    #     Input('proclamation_results', 'data'),
    #     Input(component_id='unit_number', component_property='value'),
    #     allow_duplicate=True)
    # def find_top_10_unit(proclamation_results, unit):
    #     return []

    # @app.callback(
    #     Output("top_10_results_hunt_type", "data"), 
    #     Input('proclamation_results', 'data'),
    #     Input(component_id='weapon_dropdown', component_property='value'),
    #     allow_duplicate=True)
    # def find_top_10_hunt_type(proclamation_results, hunt_type):
    #     return []

