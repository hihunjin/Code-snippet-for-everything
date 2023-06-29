import os
from typing import Tuple
from functools import partial


def glob_files(
    root_path: str,
    extensions: Tuple[str],
    recursive: bool = True,
    max_directories: int = -1,
    max_files: int = -1,
    include_hidden_paths: bool = False,
    return_info: bool = False,
):
    paths = []
    hit_max_directories = False
    hit_max_files = False
    for idx, (directory, subdirectories, fnames) in enumerate(os.walk(root_path, followlinks=True)):
        if not include_hidden_paths and os.path.basename(directory).startswith("."):
            continue

        if max_directories >= 0 and idx >= max_directories:
            hit_max_directories = True
            break

        paths += [
            os.path.join(directory, fname)
            for fname in sorted(fnames)
            if fname.lower().endswith(extensions)
        ]

        if not recursive:
            break

        if max_files >= 0 and len(paths) > max_files:
            hit_max_files = True
            paths = paths[:max_files]
            break

    if return_info:
        return paths, hit_max_directories, hit_max_files
    else:
        return paths


get_image_list = partial(
    glob_files, extensions=(".jpg", ".jpeg", ".png", ".ppm", ".bmp", ".pgm", ".tif", ".tiff", ".webp")
)
