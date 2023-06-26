import os
import subprocess
import time
import json
import warnings
from typing import Tuple, List
from datetime import datetime

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


def track():
    device_type = "3090"
    device_num = 1
    csv_loc = f"./memory_train_{device_type}.csv"
    temp_csv_loc = f"./memory_train_temp{device_type}.csv"
    csv_loc = to_abs_path(csv_loc)
    if os.path.exists(csv_loc):
        os.remove(csv_loc)


    batch_sizes = [2, 4, 8, 12, 16]
    image_sizes = [[256, 256], [512, 512], [1024, 1024], [2048, 2048]]
    models = ["wrn50", "resnet18", "resnet34"]
    df = pd.DataFrame(columns=["model", "batch_size", "image_size", "gpu_type", "gpu_usage"])
    df.to_csv(csv_loc, index=False)
    for model in models:
        for batch_size in batch_sizes:
            for image_size in image_sizes:
                print(model, batch_size, image_size)
                if os.path.exists(temp_csv_loc):
                    os.remove(temp_csv_loc)
                process = subprocess.Popen(
                    [
                        "sudo",
                        "-H",
                        "-E",
                        f"CUDA_VISIBLE_DEVICES={device_num}",
                        "python",
                        "test_model_train.py",
                        model,
                        str(batch_size),
                        str(image_size[0]),
                    ]
                )
                _df = pd.DataFrame(columns=["time", "device_id", "GPU_memory_usage"])
                _df.to_csv(temp_csv_loc, index=False)
                while process.poll() is None:
                    # print("Subprocess is still running")
                    # print("process.poll()", process.poll())
                    memories = get_gpu_memory()
                    _df = pd.DataFrame(columns=["time", "device_id", "GPU_memory_usage"])
                    for device_id, memory in memories:
                        # print(memory)
                        _df = _df.append(
                            {
                                "time": datetime.now().strftime("%H:%M:%S.%f"),
                                "device_id": int(device_id),
                                "GPU_memory_usage": round(memory / 1024 ** 2, 5),
                            }, ignore_index=True
                        )
                    _df.to_csv(temp_csv_loc, mode="a", index=False, header=False)
                    time.sleep(0.2)

                process.terminate()  # Terminate the subprocess
                time.sleep(2)
                if process.returncode != 0:
                    gpu_usage_max = "OOM"
                else:
                    _df = pd.read_csv(temp_csv_loc)
                    gpu_usage_max = _df[_df["device_id"] == device_num]["GPU_memory_usage"].max()
                df = pd.DataFrame(columns=["model", "batch_size", "image_size", "gpu_type", "gpu_usage"])
                df = df.append(
                    {
                        "model": model,
                        "batch_size": batch_size,
                        "image_size": image_size,
                        "gpu_type": device_type,
                        "gpu_usage": gpu_usage_max,
                    },
                    ignore_index=True,
                )
                df.to_csv(csv_loc, mode="a", index=False, header=False)



    df = pd.read_csv(csv_loc)
    print(df)

if __name__ == "__main__":
    track()
