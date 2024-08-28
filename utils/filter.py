from datetime import datetime


def filter_episode_year_by_range(episode: dict, start_year: int, end_year: int) -> bool:
    year = datetime.strptime(episode['air_date'], '%B %d, %Y').year
    return start_year <= year <= end_year
