import os
from PIL import Image, ImageDraw, ImageFont
from data_handling import (
    request_manager_name, calc_week_targets, 
    calc_week_results, indicator_circle,
    month_targets, format_worked_dates,
    get_daily_results, get_worked_dates, api_date_format
)
from variables import *
import datetime

font_size = 15
myfont = ImageFont.truetype('arial.ttf', font_size)

def draw_text_centered(draw, position, text, font, cell_width, cell_height, color=(0, 0, 0)):
    """Draw text centered within a given cell."""
    text_width = draw.textlength(text, font=font)
    x_position = position[0] + round((cell_width - text_width) / 2)
    y_position = position[1] + round((cell_height - font_size) / 2)
    draw.text((x_position, y_position), text, font=font, fill=color)

def paste_circle_image(template, circle_image_path, position):
    """Paste a circle image onto the template."""
    circle_image = Image.open(circle_image_path)
    template.paste(circle_image, position, mask=circle_image)

def write_stats(inserted_date, stats, headers, output_folder, manager_id):
    manager = request_manager_name(headers, manager_id)
    targets = calc_week_targets(inserted_date, stats)
    week_results = calc_week_results(inserted_date, stats)
    circle_indicators = indicator_circle(inserted_date, stats)
    month_worked_days = month_targets(stats)
    formatted_week_worked_dates = format_worked_dates(inserted_date, stats)
    daily_results = get_daily_results(inserted_date, stats)

    formatted_inserted_date = api_date_format(inserted_date)
    worked_dates_api_format = get_worked_dates(inserted_date, stats)
    if formatted_inserted_date not in worked_dates_api_format:
        return  # Skip processing if the manager didn't work on the inserted date

    # Calculate month yaware target
    month_yaware_target = int(month_worked_days) * daily_targets["yaware"]
    yaware_seconds = month_yaware_target.total_seconds()
    yaware_hours = int(yaware_seconds // 3600)
    yaware_minutes = int(yaware_seconds % 3600) // 60
    month_yaware_target_str = f"{yaware_hours}:{yaware_minutes:02d}:00"

    # Open the template image
    template = Image.open(r"template.jpg")
    draw = ImageDraw.Draw(template)

    # Write manager name
    draw_text_centered(draw, (manager_name_position["x"], manager_name_position["y"]), manager, myfont, manager_name_position["cell_width"], manager_name_position["cell_height"])

    # Write targets
    draw_text_centered(draw, (targets_position["x"], targets_position["calls_y"]), targets["week target calls"], myfont, targets_position["cell_width"], targets_position["cell_height"])
    draw_text_centered(draw, (targets_position["x"], targets_position["uniques_y"]), targets["week target uniques"], myfont, targets_position["cell_width"], targets_position["cell_height"])
    draw_text_centered(draw, (targets_position["x"], targets_position["minutes_y"]), targets["week target minutes"], myfont, targets_position["cell_width"], targets_position["cell_height"])

    # Write week results (blue background)
    draw_text_centered(draw, (summed_stats_position["first_row_x"], summed_stats_position["calls_y"]), str(week_results["calls"]), myfont, summed_stats_position["cell_width"], summed_stats_position["cell_height"], color=(255, 255, 255))
    draw_text_centered(draw, (summed_stats_position["first_row_x"], summed_stats_position["uniques_y"]), str(week_results["uniques"]), myfont, summed_stats_position["cell_width"], summed_stats_position["cell_height"], color=(255, 255, 255))
    draw_text_centered(draw, (summed_stats_position["first_row_x"], summed_stats_position["minutes_y"]), str(week_results["minutes"]), myfont, summed_stats_position["cell_width"], summed_stats_position["cell_height"], color=(255, 255, 255))

    # Paste circle indicators
    paste_circle_image(template, f'{circle_indicators["calls circle"]}.png', (color_indicators_position["x"], color_indicators_position["calls_circle_y"]))
    paste_circle_image(template, f'{circle_indicators["uniques circle"]}.png', (color_indicators_position["x"], color_indicators_position["uniques_circle_y"]))
    paste_circle_image(template, f'{circle_indicators["minutes circle"]}.png', (color_indicators_position["x"], color_indicators_position["minutes_circle_y"]))

    # Write month stats
    draw_text_centered(draw, (month_stats_position["worked_days_x"], month_stats_position["y"]), month_worked_days, myfont, month_stats_position["cell_width"], month_stats_position["cell_height"])
    draw_text_centered(draw, (month_stats_position["yaware_target_x"], month_stats_position["y"]), month_yaware_target_str, myfont, month_stats_position["cell_width"], month_stats_position["cell_height"])

    # Write dates and daily stats
    for i, week_worked_date in enumerate(formatted_week_worked_dates):
        worked_date, worked_weekday = week_worked_date.split("/")

        draw_text_centered(draw, (dates_position["x"] + i * 62, dates_position["y"]), worked_date, myfont, dates_position["cell_width"], dates_position["cell_height"])
        draw_text_centered(draw, (dates_position["weekday_x"] + i * 62, dates_position["weekday_y"]), worked_weekday, myfont, dates_position["weekday_cell_width"], dates_position["weekday_cell_height"])

    # Write daily stats
    for i, (date, results) in enumerate(daily_results.items()):
        draw_text_centered(draw, (daily_stats_position["x"] + i * 62, daily_stats_position["y"]), str(results["calls"]), myfont, daily_stats_position["cell_width"],daily_stats_position["cell_height"])
        draw_text_centered(draw, (daily_stats_position["x"] + i * 62, daily_stats_position["y"] + 31), str(results["uniques"]), myfont, daily_stats_position["cell_width"], daily_stats_position["cell_height"])
        draw_text_centered(draw, (daily_stats_position["x"] + i * 62, daily_stats_position["y"] + 62), str(results["minutes"]), myfont, daily_stats_position["cell_width"], daily_stats_position["cell_height"])

    # Save the template with the manager's name and date in the file path
    month, day, year = inserted_date.split("/")
    folder_date = f"{day}_{month}_{year}"
    os.makedirs(os.path.join(output_folder, folder_date), exist_ok=True)
    template.save(os.path.join(output_folder, folder_date, f"{manager}.png"))

