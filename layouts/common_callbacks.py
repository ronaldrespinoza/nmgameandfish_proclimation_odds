from dash import Input, Output, callback
from data_handlers.query_odds import parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag
import pandas as pd

# original callbacks to show draw result odds
def common_callbacks(app):
    pass


