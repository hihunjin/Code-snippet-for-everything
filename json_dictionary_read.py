import json
  
# Opening JSON file
f = open('sample_label.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i,j in data.items():
    print(i,j)
# pretty print
print(json.dumps(data, indent=4, sort_keys=True))

# Closing file
f.close()
