import os
import sys
from git import Repo


url = "https://github.com/hihunjin/Code-snippet-for-everything"
master_path = "main"
to_path = "temp_"
number_of_loop = 5
transform_config = dict(
    resize=dict(
        size=(300, 150),
    ),
)

# clone main branch
cloned_repo = Repo.clone_from(
    url=url,
    to_path=master_path,
    branch=master_path,
)

# get commit ids
commit_ids = cloned_repo.git.log(f"-{number_of_loop}", "--pretty=format:%h").split("\n")


def clone_and_checkout(prefix: str = "", commit_id: str = "") -> Repo:
    cloned_repo = Repo.clone_from(
        url=url,
        to_path=prefix + commit_id,
        branch="main",
    )
    print(f"======== cloned at {prefix + commit_id} ========")
    cloned_repo.git.checkout(commit_id)
    return cloned_repo


if __name__ == "__main__":
    # do preprocess
    print("init")
    for commit_id in commit_ids:
        print(f" << commit id: {commit_id} >>")
        # clone and checkout
        cloned_repo = clone_and_checkout(to_path, commit_id)

        # add system path
        dir_name = cloned_repo.working_dir.split("/")[-1]
        sys.path.append(dir_name)

        # do jobs
        L = os.listdir()
        print("os.listdir()", L)

        # remove system path and del
        sys.path.pop()
        del L
