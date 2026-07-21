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