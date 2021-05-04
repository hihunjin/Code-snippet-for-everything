!pip install SimpleITK

####### import
import numpy as np
import SimpleITK as sitk
import time
import os

####### import ct
ct = sitk.ReadImage('102_CT_rot.nii', sitk.sitkInt16)

out_dir = '.'

####### function to write
def writeSlices(series_tag_values, new_img, out_dir, i):
    image_slice = new_img[:, :, i]

    # Tags shared by the series.
    list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0],
                                                       tag_value[1]),
             series_tag_values))

    # Slice specific tags.
    #   Instance Creation Date
    image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d"))
    #   Instance Creation Time
    image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S"))

    # Setting the type to CT so that the slice location is preserved and
    # the thickness is carried over.
    image_slice.SetMetaData("0008|0060", "CT")

    # (0020, 0032) image position patient determines the 3D spacing between
    # slices.
    #   Image Position (Patient)
    image_slice.SetMetaData("0020|0032", '\\'.join(
        map(str, new_img.TransformIndexToPhysicalPoint((0, 0, i)))))
    #   Instance Number
    image_slice.SetMetaData("0020,0013", str(i))

    # Write to the output directory and add the extension dcm, to force
    # writing in DICOM format.
    writer.SetFileName(os.path.join(out_dir, str(i) + '.dcm'))
    writer.Execute(image_slice)


    
######## write

writer = sitk.ImageFileWriter()
writer.KeepOriginalImageUIDOn()     ###
modification_time = time.strftime("%H%M%S")
modification_date = time.strftime("%Y%m%d")

direction = ct.GetDirection()
series_tag_values = [
    ("0008|0031", modification_time),  # Series Time
    ("0008|0021", modification_date),  # Series Date
    ("0008|0008", "DERIVED\\SECONDARY"),  # Image Type
    ("0020|000e", "1.2.826.0.1.3680043.2.1125."
     + modification_date + ".1" + modification_time),  # Series Instance UID
    ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],
                                      direction[1], direction[4],
                                      direction[7])))),  # Image Orientation
    # (Patient)
    ("0008|103e", "Created-SimpleITK")  # Series Description
]

# Write slices to output directory
list(map(lambda i: writeSlices(series_tag_values, ct, out_dir, i),
         range(ct.GetDepth())))








######### re-read

data_directory = out_dir
series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(data_directory)
if not series_IDs:
    print("ERROR: given directory \"" + data_directory +
          "\" does not contain a DICOM series.")
    sys.exit(1)
series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
    data_directory, series_IDs[0])

series_reader = sitk.ImageSeriesReader()
series_reader.SetFileNames(series_file_names)

series_reader.LoadPrivateTagsOn()       # bring tags from series_tag_values. series_tag_values에서 정의한 tag들을 가져온다.
image3D = series_reader.Execute()
# print(image3D.GetSpacing(), 'vs', ct.GetSpacing())
