from collections import defaultdict
import requests
import pytz
from datetime import datetime, timedelta, date
from variables import months, weekdays


# Utility Functions

def format_date(inserted_date: str) -> str:
    """Format date to fit the datetime library (YYYY-MM-DD)."""
    month, day, year = inserted_date.split("/")
    return f"20{year}-{month.zfill(2)}-{day.zfill(2)}"

def api_date_format(inserted_date: str) -> str:
    """Format date to the required API format (YYYY-MM-DD)."""
    return format_date(inserted_date)

def get_weekday(inserted_date: str) -> int:
    """Return the weekday index for the given date."""
    if "/" in inserted_date:
        inserted_date = format_date(inserted_date)
    year, month, day = map(int, inserted_date.split("-"))
    return date(year, month, day).weekday()

def get_monday_date(inserted_date: str) -> date:
    """Return the date of the Monday of the given week."""
    weekday = get_weekday(inserted_date)
    month, day, year = map(int, inserted_date.split("/"))
    if year < 100:  # Handling two-digit year input
        year += 2000
    return date(year, month, day) - timedelta(days=weekday)


# API Interaction Functions

def request_manager_name(bearer: str, manager_id: str) -> str:
    """Request the manager's name based on the manager ID."""
    headers = {"authorization": f"{bearer}"}
    try:
        response = requests.get(f'https://licacrm.co/api/user/index/{manager_id}/callcenter', headers=headers)
        response.raise_for_status()
        data = response.json()
        first_name = data['data']['user_info']['first_name']
        second_name = data['data']['user_info']['second_name']
        return f"{first_name} {second_name}"
    except requests.RequestException as e:
        print(f"Error fetching manager name: {e}")
        return "Unknown Manager"


def request_manager_stats(inserted_date: str, bearer: str, manager_id: str) -> list:
    """Request the manager's stats from the API."""
    try:
        formatted_date = datetime.strptime(inserted_date, "%m/%d/%y")
        adjusted_date = formatted_date + timedelta(days=1)  # Adjust for Lica timezone
        start_of_month = formatted_date.replace(day=1).strftime("%Y-%m-%d")
        adjusted_date_str = adjusted_date.strftime("%Y-%m-%d")
        headers = {"authorization": f"{bearer}"}
        response = requests.get(
            f'https://licacrm.co/api/v2/calls/report/hour?manager_id={manager_id}&date={start_of_month}|{adjusted_date_str}',
            headers=headers
        )
        response.raise_for_status()
        return response.json()["data"]["hours"]
    except requests.RequestException as e:
        print(f"Error fetching manager stats: {e}")
        return []

def get_stats(inserted_date: str, headers: str, manager_id: str) -> dict:
    """Process the manager's stats and aggregate them by date."""
    stats = request_manager_stats(inserted_date, headers, manager_id)
    kyiv_timezone = pytz.timezone('Europe/Kyiv')
    brazil_timezone = pytz.timezone('Etc/GMT+3')

    # Aggregate data by date
    aggregated_data = defaultdict(lambda: {'all_cnt': 0, 'unique_cnt': 0, 'duration': 0})
    
    for entry in stats:
        time_str = entry['time']
        time_gmt_plus_3 = kyiv_timezone.localize(datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
        time_gmt_minus_3 = time_gmt_plus_3.astimezone(brazil_timezone)
        date_gmt_minus_3 = time_gmt_minus_3.date()  # Convert to date object

        aggregated_data[date_gmt_minus_3]['all_cnt'] += entry['all_cnt'] or 0
        aggregated_data[date_gmt_minus_3]['unique_cnt'] += entry['unique_cnt'] or 0
        aggregated_data[date_gmt_minus_3]['duration'] += entry['duration'] or 0

    # Initialize stats dictionary
    total_stats = {}
    inserted_date_dt = datetime.strptime(inserted_date, "%m/%d/%y")
    start_of_month_dt = inserted_date_dt.replace(day=1)

    # Convert datetime to date for comparison
    inserted_date_date = inserted_date_dt.date()
    start_of_month_date = start_of_month_dt.date()

    # Process each date
    for date_, totals in aggregated_data.items():
        # Ensure both dates are of type 'datetime.date' for comparison
        if start_of_month_date <= date_ <= inserted_date_date:
            total_stats[str(date_)] = {
                "date": str(date_),
                "calls": totals['all_cnt'],
                "uniques": totals['unique_cnt'],
                "minutes": totals['duration']
            }

    return total_stats



def month_targets(stats: dict) -> str:
    """Calculate the number of worked days in the month."""
    return str(len(stats))


# Weekly Calculations

def get_worked_dates(inserted_date: str, stats: dict) -> list:
    """Return the worked dates in the given week."""
    weekday = get_weekday(inserted_date)
    monday_date = str(get_monday_date(inserted_date))
    sorted_dates = sorted(stats.keys(), reverse=True)
    if monday_date in sorted_dates:
        weekday += 1  # Add one because Monday == 0
    worked_dates = sorted_dates[:weekday]
    worked_dates.reverse()
    return worked_dates


def calc_week_targets(inserted_date: str, stats: dict) -> dict:
    """Calculate weekly targets based on worked days."""
    worked_days = len(get_worked_dates(inserted_date, stats))
    return {
        "week target calls": str(worked_days * 130),
        "week target uniques": str(worked_days * 110),
        "week target minutes": str(worked_days * 60)
    }


def calc_week_results(inserted_date: str, stats: dict) -> dict:
    """Calculate weekly results (blue background) based on worked dates."""
    worked_dates = get_worked_dates(inserted_date, stats)
    week_result = {"calls": 0, "uniques": 0, "minutes": 0}
    
    for date in worked_dates:
        if date in stats:
            week_result["calls"] += stats[date]["calls"]
            week_result["uniques"] += stats[date]["uniques"]
            week_result["minutes"] += stats[date]["minutes"]

    return week_result


# Daily Calculations

def get_daily_results(inserted_date: str, stats: dict) -> dict:
    """Get daily results for the inserted date."""
    worked_dates = get_worked_dates(inserted_date, stats)
    return {date: {
        "calls": stats[date]["calls"],
        "uniques": stats[date]["uniques"],
        "minutes": stats[date]["minutes"]
    } for date in worked_dates if date in stats}


def format_worked_dates(inserted_date: str, stats: dict) -> list:
    """Format the worked dates for display on the template."""
    formatted_dates = []
    worked_dates = get_worked_dates(inserted_date, stats)

    for worked_date in worked_dates:
        month = months[worked_date.split("-")[1]]
        day = worked_date.split("-")[2]
        weekday = weekdays[str(get_weekday(worked_date))]
        formatted_dates.append(f"{day}-{month}/{weekday}")

    return formatted_dates 


# Indicator Circle Color

def indicator_circle(inserted_date: str, stats: dict) -> dict:
    """Determine the color of the indicator circles based on performance."""
    targets = calc_week_targets(inserted_date, stats)
    week_results = calc_week_results(inserted_date, stats)

    def circle_color(result, target):
        return "green_circle" if int(result) >= int(target) else "red_circle"

    return {
        "calls circle": circle_color(week_results["calls"], targets["week target calls"]),
        "uniques circle": circle_color(week_results["uniques"], targets["week target uniques"]),
        "minutes circle": circle_color(week_results["minutes"], targets["week target minutes"]),
    }
