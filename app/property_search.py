import json
from urllib.parse import urlencode, quote
from typing import Dict, Any

BASE_URL = "https://www.butterflo.com/properties"

def submit_search_api(search_json: Dict[str, Any]) -> str:
    print("Calling Butterflo Search API with:", json.dumps(search_json, indent=2))
    params = {}
    # Price range
    if "price_min" in search_json or "price_max" in search_json:
        params["pr"] = f"{search_json.get('price_min','')}:{search_json.get('price_max','')}"
    # Year built
    if "year_min" in search_json or "year_max" in search_json:
        params["yb"] = f"{search_json.get('year_min','')}:{search_json.get('year_max','')}"
    # Cap Rate
    if "cap_rate_min" in search_json or "cap_rate_max" in search_json:
        params["cr"] = f"{search_json.get('cap_rate_min','')}:{search_json.get('cap_rate_max','')}"
    # ROI Rate
    if "roi_min" in search_json or "roi_max" in search_json:
        params["roi"] = f"{search_json.get('roi_min','')}:{search_json.get('roi_max','')}"
    # Order by
    if "order_by" in search_json:
        params["ob"] = search_json["order_by"]
    # Home types
    if "home_types" in search_json:
        params["ht"] = ":".join(search_json["home_types"])
    # Bedrooms and Bathrooms
    if "beds" in search_json:
        params["bd"] = search_json["beds"]
    if "baths" in search_json:
        params["ba"] = search_json["baths"]
    # Area size
    if "area_min" in search_json or "area_max" in search_json:
        params["as"] = f"{search_json.get('area_min','')}:{search_json.get('area_max','')}"
    # Lot size
    if "lot_min" in search_json or "lot_max" in search_json:
        params["ls"] = f"{search_json.get('lot_min','')}:{search_json.get('lot_max','')}"
    # School ratings
    for level in ["primary", "middle", "high"]:
        key = f"school_{level}"
        if key in search_json:
            params[key] = search_json[key]
    # Growth metrics
    growth_keys = ["growth_1yr", "growth_3yr", "growth_5yr", "growth_10yr", "population_growth"]
    for k in growth_keys:
        if k in search_json:
            params[k] = search_json[k]
    query_str = urlencode(params, quote_via=quote)
    return f"{BASE_URL}?{query_str}"

class PropertySearchAgent:
    def __init__(self, user_profile_agent):
        self.user_profile_agent = user_profile_agent
        self.mandatory_fields = ["location"]
        self.defaults = {
            "price_min": 200000,
            "price_max": 600000,
            "year_min": 2009,
            "year_max": 2023,
            "cap_rate_min": None,
            "cap_rate_max": 9,
            "roi_min": None,
            "roi_max": None,
            "order_by": "cr",  # cap rate
            "home_types": ["single_family", "multi_family", "condo", "townhouse"],
            "beds": None,
            "baths": None,
            "area_min": None,
            "area_max": None,
            "lot_min": None,
            "lot_max": None,
            # school ratings: Any
            "school_primary": None,
            "school_middle": None,
            "school_high": None,
            # growth metrics: Any
            "growth_1yr": None,
            "growth_3yr": None,
            "growth_5yr": None,
            "growth_10yr": None,
            "population_growth": None
        }


    def build_search_json(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        # Start with defaults
        search_json = {**self.defaults}
        # Fill mandatory
        for key in self.mandatory_fields:
            if key not in user_input and not search_json.get(key):
                default = self.user_profile_agent.get_user_default(key)
                if default:
                    search_json[key] = default
                else:
                    raise ValueError(f"Missing required field: {key}")
        # Override with user provided
        search_json.update({k: v for k, v in user_input.items() if v is not None})
        return search_json

    def run_search(self, user_input: Dict[str, Any]) -> str:
        search_json = self.build_search_json(user_input)
        return submit_search_api(search_json)