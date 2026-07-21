import json
import os


def load_ranking_data():
    """
    Load crowd ranking data from output/ranking_output.json

    Returns:
        list: Ranking data
    """

    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, "..", "output", "ranking_output.json")

    with open(json_path, "r") as file:
        data = json.load(file)

    return data