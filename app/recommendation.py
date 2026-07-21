def get_best_spot(ranking_data):
    """
    Return the highest-ranked spot.

    Args:
        ranking_data (list): List of ranked spots

    Returns:
        dict: Best spot
    """

    if not ranking_data:
        return None

    # JSON is already sorted by rank
    return ranking_data[0]