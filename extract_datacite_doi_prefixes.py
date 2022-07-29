## Get datacite providers and all doi prefixes!
# Caution: This does not mean all dois with one of this prefix needs to be a dataset!

import json
from datetime import datetime
from pathlib import Path
import requests

today = datetime.now().strftime("%Y-%m-%d")
datacite_url = "https://api.test.datacite.org/providers"

def get_datacite_provider():
    all_provider = []
    new_provider = True
    next_url = datacite_url
    while new_provider and next_url:
        print(f"\r* {len(all_provider)}", end="")
        response = requests.get(next_url)
        data_json = response.json()
        new_provider = data_json["data"]
        all_provider.extend(new_provider)
        next_url = data_json.get("links", {}).get("next")
    print("\r")
    return all_provider

def extract_prefixes(datacite_provider):
    all_datacite_prefixes = []
    for provider in datacite_provider:
        for prefix in provider["relationships"]["prefixes"]["data"]:
            assert prefix["type"] == "prefixes"
            all_datacite_prefixes.append(prefix["id"])
    all_datacite_prefixes = list(set(all_datacite_prefixes))
    return all_datacite_prefixes

  
if __name__ == "__main__":
    datacite_provider = get_datacite_provider()
    datacite_prefixes = extract_prefixes(datacite_provider)
    # save the data as json in data folder (not synced with repo)    
    data_path = Path("data")
    data_path.mkdir(parents=True, exist_ok=True)
    provider_file = data_path / Path(f"datacite_provider_{today}.json")
    with provider_file.open("w") as f:
        json.dump(datacite_provider, f)
    prefix_path = data_path / Path(f"datacite_doi_prefixes_{today}.json")
    with prefix_path.open("w") as f:
        json.dump(datacite_prefixes, f)
