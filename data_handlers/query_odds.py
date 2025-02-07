import csv
import pandas as pd



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
    except KeyError:
        pass
    return df_display

def drop_percent_success(result_set):
    try:
        df_display = df_display.drop(columns=["resident_percent_success"])
        df_display = df_display.drop(columns=["resident_1stDraw_percent_success"])
        df_display = df_display.drop(columns=["resident_2ndDraw_percent_success"])
        df_display = df_display.drop(columns=["resident_3rdDraw_percent_success"])
    except KeyError:
        pass
    return df_display

def filter_on_boolean_switches(filtered_list, residency_choice, choice_result, success_total, success_percentage, percent_success):
    df = pd.DataFrame(filtered_list)
    
    try:
        if not(residency_choice.resident):
            df = df.drop(columns=["1st_resident", "2nd_resident", "3rd_resident", "Total_resident"])
        if not(residency_choice.nonresident):
            df = df.drop(columns=["1st_nonresident", "2nd_nonresident", "3rd_nonresident", "Total_nonresident"])
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
        if not(success_total.nonresident_total):
            df = df.drop(columns=["Nonresident_successfull_draw_total"])
        if not(success_total.outfitter_total):
            df = df.drop(columns=["Outfitter_successfull_draw_total"])
    except KeyError:
        pass

    try:
        if not(success_percentage.resident_percentages):
            df = df.drop(columns=["Resident_percentage_allocation"])
        if not(success_percentage.nonresident_percentages):
            df = df.drop(columns=["nonresident_percentage_allocation"])
        if not(success_percentage.outfitter_percentages):
            df = df.drop(columns=["outfitter_percentage_allocation"])
    except KeyError:
        pass
    
    try:
        if not(percent_success.resident_percent_success):
            df = df.drop(columns=["resident_percent_success"])
        if not(percent_success.resident_percent_success_first_choice):
            df = df.drop(columns=["resident_1stDraw_percent_success"])
        if not(percent_success.resident_percent_success_second_choice):
            df = df.drop(columns=["resident_2ndDraw_percent_success"])
        if not(percent_success.resident_percent_success_third_choice):
            df = df.drop(columns=["resident_3rdDraw_percent_success"])

        if not(percent_success.nonresident_percent_success):
            df = df.drop(columns=["nonresident_percent_success"])
        if not(percent_success.nonresident_percent_success_first_choice):
            df = df.drop(columns=["nonresident_1stDraw_percent_success"])
        if not(percent_success.nonresident_percent_success_second_choice):
            df = df.drop(columns=["nonresident_2ndDraw_percent_success"])
        if not(percent_success.nonresident_percent_success_third_choice):
            df = df.drop(columns=["nonresident_3rdDraw_percent_success"])

        if not(percent_success.outfitter_percent_success):
            df = df.drop(columns=["outfitter_percent_success"])
        if not(percent_success.outfitter_percent_success_first_choice):
            df = df.drop(columns=["outfitter_1stDraw_percent_success"])
        if not(percent_success.outfitter_percent_success_second_choice):
            df = df.drop(columns=["outfitter_2ndDraw_percent_success"])
        if not(percent_success.outfitter_percent_success_third_choice):
            df = df.drop(columns=["outfitter_3rdDraw_percent_success"])
    except KeyError:
        pass
    
    return df.to_dict('records')


def query_odds(odds_summary, unit_number, residency_choice, choice_result, success_total, success_percentage, percent_success, add_private, add_youth,):
    filtered_list = []
    filtered_list = GetListFromQuery.get_unit_by_number(odds_summary, unit_number)

    if not(add_private):
        filtered_list = GetListFromQuery.get_no_private(filtered_list)
    if not(add_youth):
        filtered_list = GetListFromQuery.get_no_youth(filtered_list)
    filtered_list = filter_on_boolean_switches(filtered_list, residency_choice, choice_result, success_total, success_percentage, percent_success)
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
                        "1st_nonresident": "",
                        "2nd_nonresident": "",
                        "3rd_nonresident": "",
                        "Total_nonresident":"",
                        "1st_outfitter": "",
                        "2nd_outfitter": "",
                        "3rd_outfitter": "",
                        "Total_outfitter":"",
                        "Resident_successfull_draw_total": "",
                        "Nonresident_successfull_draw_total": "",
                        "Outfitter_successfull_draw_total": "",
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


def get_df_for_pie_chart(df, new_column, total_column, factored_column):
    """
    This function computes a new column for pie chart percentages. It handles cases where 
    the total_column or factored_column is 0 or None to avoid division errors.
    """
    # Initialize the new column to be 0 by default and ensure it's of type float
    df[new_column] = 0.0  # Make sure the column is of float type

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Check if total_column or factored_column is 0 or None
        if row[total_column] == 0 or row[total_column] is None or row[factored_column] == 0 or row[factored_column] is None:
            # If condition met, leave value as 0
            df.at[index, new_column] = 0.0  # Make sure the assignment is of type float
        else:
            # Otherwise, calculate the percentage and ensure it's stored as a float
            df.at[index, new_column] = float(row[total_column] / row[factored_column]) * 100

    return df



