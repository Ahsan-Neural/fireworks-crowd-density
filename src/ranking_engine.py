from dataclasses import dataclass
from typing import List
import json


@dataclass
class SpotReading:
    spot_id: str
    spot_name: str
    head_count: int
    density: float = None  # optional, filled in once calibration exists
    timestamp: str = None


def rank_spots(readings: List[SpotReading], use_density: bool = False) -> List[dict]:
    def score(r):
        if use_density and r.density is not None:
            return r.density
        return r.head_count

    sorted_readings = sorted(readings, key=score)

    ranked = []
    for i, r in enumerate(sorted_readings, start=1):
        ranked.append({
            "rank": i,
            "spot_id": r.spot_id,
            "spot_name": r.spot_name,
            "head_count": r.head_count,
            "density": r.density,
            "crowd_level": crowd_level_label(score(r), use_density),
        })
    return ranked


def crowd_level_label(value: float, use_density: bool) -> str:
    if use_density:
        if value < 0.5:
            return "Low"
        elif value < 1.5:
            return "Moderate"
        else:
            return "High"
    else:
        if value < 40:
            return "Low"
        elif value < 60:
            return "Moderate"
        elif value < 90:
            return "High"
        else:
            return "Very High"


def export_ranking_json(ranked: List[dict], filepath: str = "ranking_output.json"):
    with open(filepath, "w") as f:
        json.dump(ranked, f, indent=2)
    return filepath