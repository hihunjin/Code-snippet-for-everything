from tqdm import tqdm




pbar = tqdm(["a", "b", "c", "d"])
for char in pbar:
    pbar.set_description("Processing %s" % char)
# Processing d: 100%|██████████| 4/4 [00:00<00:00, 224.94it/s]
