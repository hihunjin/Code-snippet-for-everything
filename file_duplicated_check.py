import os

all_file_names = {}
for path, subdirs, files in os.walk(p):
    for name in files:
        if name in all_file_names:
            all_file_names[name].append(os.path.join(path, name))
        else:
            all_file_names[name] = [os.path.join(path, name)]
for keys, values in all_file_names.items():
    if len(values) > 1:
        print(f"The name '{keys}' is duplicated. loc : {values}")

# The name 'hi' is duplicated. loc : ['/content/hi', '/content/sample_data/hi']
