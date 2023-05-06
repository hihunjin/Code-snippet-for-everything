import os
import subprocess
import time
import json
import warnings
from typing import Tuple, List
from datetime import datetime

import click
import pynvml

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

def get_gpu_memory() -> List[Tuple]:
    """GPU device당 GPU메모리를 NVML 모듈로부터 바이트 단위로 읽어옵니다.

    Returns:
        List[Tuple]: GPU memory in bytes

    Note:
        Use --pid=host flag with Docker.
    """
    pynvml.nvmlInit()
    memories = []
    for device_id in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(device_id)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem_used = mem_info.used
        if mem_used is None:
            memories.append(
                (device_id, 0)
            )
        else:
            memories.append(
                (device_id, mem_used)
            )
    return memories


def to_abs_path(path: str) -> str:
    return os.path.abspath(path)


@click.command()
@click.option("--csv_loc", type=str, default="_my_csv.csv")
@click.option("--plot_loc", type=str, default="_plt.jpg")
@click.option("-d", "--data", type=str, default="nsys_220224_segmentation_bottom")
@click.option("-m", "--model", type=str, default="patchcore")
@click.option("--logdir", type=str, default="../results")
@click.option("--device", type=str, default="cuda")
@click.option("--show_plot", type=bool, default=True)
def track(csv_loc, plot_loc, data, model, logdir, device, show_plot, **kwargs):
    csv_loc = to_abs_path(csv_loc)
    plot_loc = to_abs_path(plot_loc)
    os.makedirs(os.path.dirname(csv_loc), exist_ok=True)
    os.makedirs(os.path.dirname(plot_loc), exist_ok=True)
    process = subprocess.Popen(
        [
            "python",
            "api/train.py",
            "-d",
            data,
            "--network_type",
            model,
            "--logdir",
            logdir,
            "--device",
            str(device),  # should be string
        ]
    )
    df = pd.DataFrame(columns=["time", "device_id", "GPU_memory_usage"])
    df.to_csv(csv_loc, index=False)
    while process.poll() is None:
        # print("Subprocess is still running")
        # print("process.poll()", process.poll())
        memories = get_gpu_memory()
        df = pd.DataFrame(columns=["time", "device_id", "GPU_memory_usage"])
        for device_id, memory in memories:
            # print(memory)
            df = df.append(
                {
                    "time": datetime.now().strftime("%H:%M:%S.%f"),
                    "device_id": int(device_id),
                    "GPU_memory_usage": round(memory / 1024 ** 2, 5),
                }, ignore_index=True
            )
        df.to_csv(csv_loc, mode="a", index=False, header=False)
        time.sleep(0.2)

    process.terminate()  # Terminate the subprocess
    time.sleep(2)

    df = pd.read_csv(csv_loc)
    # GPU_memory_usage_max = df["GPU_memory_usage"].max()
    # print("GPU_memory_usage_max", GPU_memory_usage_max)
    num_device = len(df["device_id"].unique())
    fig, axs = plt.subplots(num_device, figsize=(10, 10))
    if num_device == 1:
        axs = [axs]
    GPU_memory_max = {}
    for device_id in df["device_id"].unique():
        df_device = df[df["device_id"] == device_id]
        GPU_memory_max[str(device_id)] = df_device["GPU_memory_usage"].max() - df_device["GPU_memory_usage"].min()
        print(f"GPU_memory_usage_max(df_device:{device_id})", GPU_memory_max[str(device_id)])
        axs[device_id].plot(df_device["GPU_memory_usage"],".-")
        axs[device_id].set_title(csv_loc[:-4] + f" | device_id: {device_id}")
        axs[device_id].set_ylabel("GPU memory (MiB)")
    # save json
    json_loc = os.path.join(os.path.dirname(csv_loc), "max.json")
    with open(json_loc, "w") as outfile:
        json.dump(GPU_memory_max, outfile)
    # save fig
    fig.savefig(plot_loc)
    if show_plot:
        # show
        plt.show()


if __name__ == "__main__":
    track()
