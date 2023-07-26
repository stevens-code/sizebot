from datetime import datetime

def format_datetime(time: datetime) -> str:
    """Formats a date and time to a clean format."""

    return datetime.strftime(time, f"%I:%M %p ({time.astimezone().tzname()}) on %m/%d/%Y")

def format_date(date: datetime) -> str:
    """Formats a date to a clean format."""

    return datetime.strftime(date, f"%m/%d/%Y")

def log_message(message: str):
    """Log a message to the console."""

    formatted_time = format_datetime(datetime.now())
    print(f"{formatted_time}: {message}")