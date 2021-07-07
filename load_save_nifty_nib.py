# load and save the same image with nibabel
import nibabel as nib

# load 1) array, affine
vol_nii = nib.load('/content/104_mask_Gallbladder_rot.nii')
affine = vol_nii.affine
# link : https://nipy.org/nibabel/reference/nibabel.dataobj_images.html#nibabel.dataobj_images.DataobjImage.get_fdata
# print(vol_nii._dataobj.dtype) == 'float64'    : True
vol = vol_nii.get_fdata()       # default : dtype=np.float64 | recommend : dtype=np.float

# save both
vol_nii = nib.Nifti1Image(vol, affine)
vol_nii.to_filename('new.nii.gz')
