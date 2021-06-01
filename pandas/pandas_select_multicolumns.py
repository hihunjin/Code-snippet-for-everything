colnames=['background', "Gallbladder", "Liver", "Pancreas", "Spleen", "Stomach"]
df = pd.read_csv('test.csv',names=colnames, header=None)
df = df[["Gallbladder", "Liver", "Pancreas", "Spleen", "Stomach"]]
df
