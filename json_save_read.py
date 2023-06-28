import json

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})


####### json save = dump #######
import json
def save_json(p, data):
    with open(p, 'w') as outfile:
        json.dump(data, outfile)
####### json read = load #######
import json
def load_json(p):
    with open(p) as json_file:
        data = json.load(json_file)
        return data


save_json("data.txt", data)
data = load_json("data.txt")
for p in data['people']:
    print('Name: ' + p['name'])
    print('Website: ' + p['website'])
    print('From: ' + p['from'])
