import yaml
import json

data = {
    "name": "video1.mp4",
    "properties": {
        "사람": "O",
        "동물": "X",
    },
}

# yaml save
with open('new.yml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

# json save
with open('new.json', 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, default=str, indent=4, sort_keys=True, ensure_ascii=False)
