from geopy.distance import geodesic


def calculate_distance(user_location, spot_location):
    """
    Calculate distance between user and spot.

    Args:
        user_location (tuple): (latitude, longitude)
        spot_location (tuple): (latitude, longitude)

    Returns:
        float: Distance in kilometers
    """

    distance = geodesic(user_location, spot_location).kilometers

    return round(distance, 2)

def calculate_walking_time(distance_km):
    walking_speed = 5  # km/hour

    time_minutes = (distance_km / walking_speed) * 60

    return round(time_minutes)