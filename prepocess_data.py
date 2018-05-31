import json
import uuid
from base64 import urlsafe_b64encode

processed_data = {
    "blackCards": {},
    "whiteCards": {}
}

NUM_WHITE_CARDS = 200

def get_nice_id(prefix):
    return prefix + urlsafe_b64encode(uuid.uuid4().bytes).decode()[:-2]

with open('base_deck.json') as f:
    data = json.load(f)
    for c in data['blackCards']:
        uid = get_nice_id('B')
        if c['pick'] != 1:
            continue
        processed_data['blackCards'][uid] = {
            "text": c['text'],
            "color": 'b',
            "features": {}
        }
    for c in data['whiteCards'][:NUM_WHITE_CARDS]:
        uid = get_nice_id('W')
        processed_data['whiteCards'][uid] = {
            "text": c,
            "color": 'w',
            "features": {}
        }


with open('processed_deck.json', 'w') as f:
    json.dump(processed_data, f, indent=2)