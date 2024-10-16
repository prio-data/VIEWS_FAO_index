import sys
import os
import numpy as np
import pandas as pd

from viewser import Queryset, Column

def get_base_input_data_config():
    """
    Contains the configuration for the base input data in the form of a viewser queryset. 
    This configuration is "behavioral" so modifying it will affect the model's runtime behavior 
    and integration into the deployment system. There is no guarantee that the model will work 
    if the input data configuration is changed here without changing the model settings and architecture accordingly.

    It is considered the base input data configuration because it contains the data for state based conflicts, non-state based conflicts, one-sided violence,
    population data, month_id, year_id, country_id, and the grid row and column.

    Returns:
    queryset_base (Queryset): A queryset containing the base data for the model training.
    """

    queryset_base = (Queryset("FAO_simon_experiments", "priogrid_month")
        .with_column(Column("sb_best", from_loa = "priogrid_month", from_column = "ged_sb_best_sum_nokgi").transform.missing.replace_na())
        .with_column(Column("ns_best", from_loa = "priogrid_month", from_column = "ged_ns_best_sum_nokgi").transform.missing.replace_na())
        .with_column(Column("os_best", from_loa = "priogrid_month", from_column = "ged_os_best_sum_nokgi").transform.missing.replace_na())
        .with_column(Column("pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum").transform.missing.fill().transform.missing.replace_na())
        .with_column(Column("month", from_loa = "month", from_column = "month"))
        .with_column(Column("year_id", from_loa = "country_year", from_column = "year_id"))
        .with_column(Column("c_id", from_loa = "country_year", from_column = "country_id"))
        .with_column(Column("col", from_loa = "priogrid", from_column = "col"))
        .with_column(Column("row", from_loa = "priogrid", from_column = "row")))

    return queryset_base

