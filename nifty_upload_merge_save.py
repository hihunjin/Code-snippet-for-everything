'''
class num   : organ name
1           : Gallbladder
2           : Liver
3           : Pancreas
4           : Spleen
5           : Stomach
'''
import numpy as np
import SimpleITK as sitk

def check_if_overlap(seg_arrays):
    for i in range(len(seg_arrays)-1):
        for j in range(len(seg_arrays)):
            if (seg_arrays[i]==seg_arrays[j]).sum()!=0:
                return True
    return False


def check_if_overlap_count(seg_arrays):
    num_voxels = 0
    for i in range(len(seg_arrays)-1):
        for j in range(len(seg_arrays)):
            if (seg_arrays[i]==seg_arrays[j]).sum()!=0:
                num_voxels += (seg_arrays[i]==seg_arrays[j]).sum()
    if num_voxels > 0:
        return True, num_voxels
    else:
        return False

seg=[]
ct = sitk.ReadImage('102_CT_rot.nii', sitk.sitkInt16)
seg.append(sitk.ReadImage('102_mask_Gallbladder_rot.nii', sitk.sitkUInt8))
seg.append(sitk.ReadImage('102_mask_Liver_rot.nii', sitk.sitkUInt8))
seg.append(sitk.ReadImage('102_mask_Pancreas_rot.nii', sitk.sitkUInt8))
seg.append(sitk.ReadImage('102_mask_Spleen_rot.nii', sitk.sitkUInt8))
seg.append(sitk.ReadImage('102_mask_Stomach_rot.nii', sitk.sitkUInt8))

seg_array=[]
seg=seg[:5]
ct_array = sitk.GetArrayFromImage(ct)
gt = np.zeros_like(ct_array)
for i in range(len(seg)):
    gt+=(i+1)*sitk.GetArrayFromImage(seg[i]) *(gt==0)

for i in range(len(seg)):
    seg_array += sitk.GetArrayFromImage(seg[i]),
print(check_if_overlap_count(seg_array))

print(gt.min(), gt.max())
gt = sitk.GetImageFromArray(gt)

gt.SetDirection(ct.GetDirection())
gt.SetOrigin(ct.GetOrigin())
gt.SetSpacing(ct.GetSpacing())
sitk.WriteImage(gt,'102_mask_all.nii')


####### calculate voxel mean    #######
'''
gal = np.average(ct_array, weights=(seg_array[0]==1))
pan = np.average(ct_array, weights=(seg_array[1]==1))
sto = np.average(ct_array, weights=(seg_array[2]==1))
spl = np.average(ct_array, weights=(seg_array[3]==1))
liv = np.average(ct_array, weights=(seg_array[4]==1))
print(gal, pan, sto, spl, liv)
63.55165289256198 106.12858224016145 -274.9645386253461 142.19617071833304 134.38175158858587
'''
