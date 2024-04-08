import responses
import urllib.parse
from datetime import datetime

from src.resources.other import get_time_difference_in_minutes

def test_get_slug():
    
    startTime = datetime(2024, 12, 12, 12, 12)
    finishTime = datetime(2024, 12, 12, 12, 13)
    timeDifference = get_time_difference_in_minutes(startTime, finishTime)

    assert timeDifference == 1.0

    startTime = datetime(2024, 12, 12, 12, 12)
    finishTime = datetime(2024, 12, 12, 13, 13)
    timeDifference = get_time_difference_in_minutes(startTime, finishTime)

    assert timeDifference == 61.0

    startTime = datetime(2024, 12, 12, 12, 12)
    finishTime = datetime(2024, 12, 12, 12, 20)
    timeDifference = get_time_difference_in_minutes(startTime, finishTime)

    assert timeDifference == 8.0
