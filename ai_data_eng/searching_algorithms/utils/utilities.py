import re


def stop_name(stop: str):
    return re.sub(r"\W+", "", stop.lower())
