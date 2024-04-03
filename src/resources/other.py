from datetime import datetime


def date_time_as_string(date=datetime.now()) -> str:
    start_time_as_string = date.strftime("%Y-%m-%d_%H_%M")
    return start_time_as_string


def get_time_difference_in_minutes(start: datetime, untill=datetime.now()) -> float:
    difference_in_minutes = (start - untill).total_seconds() / 60

    return round(difference_in_minutes, 4)
