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
