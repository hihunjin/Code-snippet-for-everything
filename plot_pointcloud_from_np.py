# !pip install torch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0
# import os
# import sys
# import torch
# need_pytorch3d=False
# try:
#     import pytorch3d
# except ModuleNotFoundError:
#     need_pytorch3d=True
# if need_pytorch3d:
#     if torch.__version__.startswith("1.7") and sys.platform.startswith("linux"):
#         # We try to install PyTorch3D via a released wheel.
#         version_str="".join([
#             f"py3{sys.version_info.minor}_cu",
#             torch.version.cuda.replace(".",""),
#             f"_pyt{torch.__version__[0:5:2]}"
#         ])
#         !pip install pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/{version_str}/download.html
#     else:
#         # We try to install PyTorch3D from source.
#         !curl -LO https://github.com/NVIDIA/cub/archive/1.10.0.tar.gz
#         !tar xzf 1.10.0.tar.gz
#         os.environ["CUB_HOME"] = os.getcwd() + "/cub-1.10.0"
#         !pip install 'git+https://github.com/facebookresearch/pytorch3d.git@stable'
# !pip install SimpleITK
from pytorch3d.structures import Pointclouds

import SimpleITK as sitk
import numpy as np

seg = sitk.ReadImage('102_mask_Gallbladder_rot.nii', sitk.sitkUInt8)

seg = sitk.GetArrayFromImage(seg)
print(seg.min(),seg.max())
vert = np.argwhere(seg)
# print(len(get_pointcloud_from_np(seg)))

device = torch.device("cuda:0")
verts = torch.FloatTensor(vert).to(device)
point_cloud = Pointclouds(points=[verts])

from pytorch3d.vis.plotly_vis import plot_scene
plot_scene({
    "Pointcloud": {
        "person": point_cloud
    }
})
