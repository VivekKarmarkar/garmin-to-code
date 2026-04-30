import os
from datetime import date, timedelta

from fastmcp import FastMCP
from garminconnect import Garmin

TOKEN_DIR = os.path.expanduser("~/.garmin-tokens")

mcp = FastMCP(
    name="garmin-connect",
    instructions=(
        "This server provides Garmin watch data. "
        "Dates use YYYY-MM-DD format. "
        "Use get_daily_stats for rich daily summaries (any date, defaults to today), "
        "get_steps_in_range for multi-day step/distance trends, "
        "and get_heart_rate for HR data on a specific date."
    ),
)


def get_client() -> Garmin:
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    if not email or not password:
        raise ValueError(
            "Set GARMIN_EMAIL and GARMIN_PASSWORD environment variables"
        )
    client = Garmin(email, password)
    client.login(tokenstore=TOKEN_DIR)
    return client


@mcp.tool(annotations={"readOnlyHint": True})
def get_daily_stats(target_date: str = "") -> dict:
    """Get rich daily activity summary: steps, distance, calories, stress, Body Battery, and more.

    YYYY-MM-DD format. Defaults to today.
    """
    client = get_client()
    cdate = target_date or date.today().isoformat()
    stats = client.get_stats(cdate)
    result = format_daily_stats(stats)
    result["date"] = cdate
    return result


@mcp.tool(annotations={"readOnlyHint": True})
def get_steps_in_range(start_date: str, end_date: str) -> list[dict]:
    """Get daily step counts and distance for a date range.

    Both dates are inclusive, YYYY-MM-DD format.
    Max range: 30 days.
    """
    client = get_client()
    steps = client.get_daily_steps(start_date, end_date)
    result = []
    for day in steps:
        meters = day.get("totalDistance", 0) or 0
        result.append({
            "date": day.get("calendarDate", ""),
            "steps": day.get("totalSteps", 0),
            "distance_km": round(meters / 1000, 2),
            "distance_miles": round(meters / 1609.34, 2),
        })
    return result


@mcp.tool(annotations={"readOnlyHint": True})
def get_heart_rate(target_date: str = "") -> dict:
    """Get heart rate data for a specific date (YYYY-MM-DD). Defaults to today."""
    client = get_client()
    cdate = target_date or date.today().isoformat()
    hr_data = client.get_heart_rates(cdate)
    return format_heart_rate(hr_data)


def format_daily_stats(stats: dict) -> dict:
    """Extract the most useful fields from Garmin's verbose stats response."""
    meters = stats.get("totalDistanceMeters", 0) or 0
    active_sec = stats.get("activeSeconds", 0) or 0
    highly_active_sec = stats.get("highlyActiveSeconds", 0) or 0

    return {
        "steps": stats.get("totalSteps", 0),
        "distance_km": round(meters / 1000, 2),
        "distance_miles": round(meters / 1609.34, 2),
        "calories_total": stats.get("totalKilocalories"),
        "calories_active": stats.get("activeKilocalories"),
        "floors_ascended": stats.get("floorsAscended"),
        "floors_descended": stats.get("floorsDescended"),
        "active_minutes": round(active_sec / 60),
        "highly_active_minutes": round(highly_active_sec / 60),
        "moderate_intensity_minutes": stats.get("moderateIntensityMinutes"),
        "vigorous_intensity_minutes": stats.get("vigorousIntensityMinutes"),
        "stress_level": stats.get("stressQualifier"),
        "avg_stress": stats.get("averageStressLevel"),
        "body_battery_high": stats.get("bodyBatteryChargedValue"),
        "body_battery_low": stats.get("bodyBatteryDrainedValue"),
    }


def format_heart_rate(hr_data: dict) -> dict:
    """Extract useful HR summary from Garmin's heart rate response."""
    return {
        "date": hr_data.get("startTimestampLocal", ""),
        "resting_hr": hr_data.get("restingHeartRate"),
        "max_hr": hr_data.get("maxHeartRate"),
        "min_hr": hr_data.get("minHeartRate"),
        "avg_hr": hr_data.get(
            "currentDayRestingHeartRate",
            hr_data.get("restingHeartRate"),
        ),
    }


if __name__ == "__main__":
    mcp.run()
