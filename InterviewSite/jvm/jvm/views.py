# import json
# from django.shortcuts import render
#from matplotlib.font_manager import json_dump

from django.template import loader
from django.http import HttpResponse, JsonResponse
import numpy as np
import pandas as pd

"""Default path view"""
def index(request):
    # Load data from previously processed file
    df = pd.read_csv("jvm\data\consolidated_records.csv")

    # Slice off the count row and the id column
    desc_continuous = df.describe().iloc[1:,1:]

    # This has some code smell to it...
    desc_categorical = df.describe(include='all').iloc[[0,1,2,3],[2,3,5,6,7,8,9,13]]

    # Use pandas to get the built-in HTML table representation
    table_string_con = desc_continuous.to_html(justify='left', classes='table table-striped', table_id='sum_stat_table_con')
    table_string_cat = desc_categorical.to_html(justify='left', classes='table table-striped', table_id='sum_stat_table_cat')
    template = loader.get_template('index.html')

    context = {
        'summary_table_con': table_string_con,
        'summary_table_cat': table_string_cat
    }

    # Pass the literal DOM strings to the render call so they can be included directly
    return HttpResponse(template.render(context, request))

"""Get the hours worked per week grouped by 1st gen immigrant status"""
def get_work_hours(request):
    # Load the DF from the generated file
    df = pd.read_csv("jvm\data\consolidated_records.csv")

    # Add a column indicator for whether or not someone is a first-generation immigrant
    df['is_immigrant'] = df['country'] != 'United-States'
    immigrant_hours = df[df['is_immigrant'] == 1].groupby(['age']).mean()['hours_week']
    non_immigrant_hours = df[df['is_immigrant'] == 0].groupby(['age']).mean()['hours_week']

    # Turn the series into an [[]] for use in our constructed JSON return
    ih_str = series_to_nested_arrays(immigrant_hours)
    nh_str = series_to_nested_arrays(non_immigrant_hours)

    # Highcharts expects a JSON array of arrays for 2D series data 
    series_data = f"{{\"immigrant_hours\": {ih_str}, \"non_immigrant_hours\": {nh_str}}}"

    return HttpResponse(series_data, 'application/json')

"""Get the population distribution by age grouped by the 1st gen immigrant status"""
def get_pop_distr(request):
    df = pd.read_csv("jvm\data\consolidated_records.csv")

    # Add a column indicator for whether or not someone is a first generation immigrant
    df['is_immigrant'] = df['country'] != 'United-States'

    # Group the DFs by age and include the id column in the result to control the format  - #TODO is this needed?
    immigrant_pop = df[df['is_immigrant'] == 1].groupby(['age']).count()['id']
    non_immigrant_pop = df[df['is_immigrant'] == 0].groupby(['age']).count()['id']

    # Turn the series in an [[]] for use in our constructed JSON return
    ih_str = series_to_nested_arrays(immigrant_pop)
    nh_str = series_to_nested_arrays(non_immigrant_pop)

    #Build and return the expected JSON string
    series_data = f"{{\"immigrant_pop\": {ih_str}, \"non_immigrant_pop\": {nh_str}}}"
    return HttpResponse(series_data, 'application/json')

"""Take a given series and turn it into an array of arrays appropriate for use in constructing a JSON response"""
def series_to_nested_arrays(ser):
    # There must be a better way to do this ... :)
    ser_dict = ser.to_dict()
    j_str = "["

    # Turn the KVP from the Dict into an array
    for d in ser_dict:
        j_str += f"[{d}, {ser_dict[d]}],"
    j_str = j_str[:-1] + "]"

    # Return the manually formatted JSON string
    return j_str

"""Provide the census data formatted for use in the Datatables.net table """
def load_census(request):
    # The datatable call will provide a lot of possible options but we only need the pagination options for now
    start = int(request.GET['start'])
    take = int(request.GET['length'])
    end = start + take

    # Make sure to include this so DT can sync ajax call responses - failure to do so will make the table look like it's stuck loading
    draw = int(request.GET['draw'])
    
    # Load the previously generated file to the DF
    df = pd.read_csv("jvm\data\consolidated_records.csv")

    # Get the data represented by the page selection and page length
    results = df.iloc[start:end]
    jresults = results.to_json(orient='records', lines=False)

    # Get the total records so DT can determine how many pages to include in pagination control
    total_records = len(df)

    # This format is dictated by DT and would be better represented by a DT_Response object that defined its own to_string
    fk = f'{{"draw": {int(draw)}, "recordsTotal": {total_records} , "recordsFiltered": {total_records} , "data": {jresults} }}' 

    return HttpResponse(fk, 'application/json')