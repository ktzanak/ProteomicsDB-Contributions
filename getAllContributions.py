import json
import requests

TOKEN = '<my_token>'  # Replace with token from gitlab
USER_ID = '61949'
BASE_URL = f"https://gitlab.lrz.de/api/v4/users/{USER_ID}/events"

headers = {"PRIVATE-TOKEN": TOKEN}

all_events = []
page = 1
per_page = 100

while True:
    params = {'per_page': per_page, 'page': page}
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    events = response.json()
    if not events:
        break
    all_events.extend(events)
    page += 1

# Save all events to a file
with open('ktzan_contributions.json', 'w') as f:
    json.dump(all_events, f, indent=2)

print(f"Downloaded {len(all_events)} events in total.")

