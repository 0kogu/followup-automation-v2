import datetime

# --- Daily Targets ---
daily_targets = {
    "calls": 130,
    "uniques": 110,
    "minutes": 60,
    "yaware": datetime.timedelta(hours=7, minutes=30)
}

# --- Manager Name Position ---
manager_name_position = {
    "x": 20,
    "y": 85,
    "cell_width": 189,
    "cell_height": 20
}

# --- Dates Position ---
dates_position = {
    "x": 488,
    "y": 60,
    "cell_width": 60,
    "cell_height": 26,
    "weekday_x": 488,
    "weekday_y": 84,
    "weekday_cell_width": 60,
    "weekday_cell_height": 20,
    "cells_gap": 2
}

# --- Targets Position ---
targets_position = {
    "x": 292,
    "cell_width": 81,
    "cell_height": 27,
    "calls_y": 115,
    "uniques_y": 146,
    "minutes_y": 178,
    "yaware_y": 209
}

# --- Summed Stats Position (Blue Background) ---
summed_stats_position = {
    "first_row_x": 372,
    "cell_height": 27,
    "cell_width": 81,
    "cells_gap": 4,
    "calls_y": 115,
    "uniques_y": 146,
    "minutes_y": 178,
    "yaware_y": 209
}

# --- Daily Stats Position (White Background) ---
daily_stats_position = {
    "x": 488,
    "y": 115,
    "cell_width": 59,
    "cell_height": 27
}

# --- Color Indicators Position (Circles) ---
color_indicators_position = {
    "x": 460,
    "calls_circle_y": 120,
    "uniques_circle_y": 150,
    "minutes_circle_y": 182,
    "yaware_circle_y": 215
}

# --- Month Stats Position ---
month_stats_position = {
    "y": 285,
    "worked_days_x": 208,
    "yaware_target_x": 292,
    "yaware_result_x": 372,
    "cell_width": 82,
    "cell_height": 27,
    "circle_x": 460,
    "circle_y": 290
}

# --- Months & Weekdays ---
months = {
    "01": "jan",
    "02": "fev",
    "03": "mar",
    "04": "abr",
    "05": "mai",
    "06": "jun",
    "07": "jul",
    "08": "ago",
    "09": "set",
    "10": "out",
    "11": "nov",
    "12": "dez"
}

weekdays = {
    "0": "seg",
    "1": "ter",
    "2": "qua",
    "3": "qui",
    "4": "sex",
    "5": "sab",
    "6": "dom"
}
