#!/usr/bin/python3

##################################################################################
# sentinel-layerstack.py
#
# Create a VRT stack from Sentinel-2 zip files without any resampling: 
# use the avaible jp2 files from the zip. Defaults to 20 m resolution.
#
# Author: 2025, Florian Neukirchen 
# License: MIT
#
#################################################################################

import os 
import argparse
import re 
from zipfile import ZipFile
from osgeo import gdal 

gdal.UseExceptions()


def main(zip_paths, resolution=20, outfolder="vrt"):
    basedir = os.path.dirname(zip_paths[0])
    outfolder = os.path.join(basedir, outfolder)
    os.makedirs(outfolder, exist_ok=True)
    zip_paths = [os.path.abspath(x) for x in zip_paths]

    mosaic_bands = {} 
    regex1 = re.compile(r'B.._{}m\.jp2$'.format(resolution))
    regex2 = re.compile(r"(B..)_{}m".format(resolution))

    for file in zip_paths:
        with ZipFile(file, 'r') as zipfile:
            bands = [x for x in zipfile.namelist() if re.search(regex1,x)]

        for band in bands:
            matches = re.search(regex2, band)
            bandname = matches.group(1)
            if not bandname in mosaic_bands:
                mosaic_bands[bandname] = []
            filename = f'/vsizip/{file}/{band}'
            mosaic_bands[bandname].append(filename)

    for bandname, inputs in mosaic_bands.items():
        ds = gdal.BuildVRT(f"{outfolder}/{resolution}m_{bandname}.vrt", inputs)
        ds = None

    # Create a VRT stack
    vrt_output = f"sentinel_stack_{resolution}m.vrt"
    ds = gdal.BuildVRT(vrt_output, [f"{outfolder}/{resolution}m_{bandname}.vrt" for bandname in mosaic_bands.keys()], separate=True)

    for idx, bandname in enumerate(mosaic_bands.keys()):
        ds.GetRasterBand(idx + 1).SetDescription(bandname)
    ds = None
    print(f"Created VRT stack: {vrt_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a VRT stack from Sentinel-2 zip files without any resampling: use the avaible jp2 files from the zip. Defaults to 20 m resolution.")
    parser.add_argument("files", nargs='+', help="Paths to Sentinel-2 zip files")
    parser.add_argument("-r", "--resolution", type=int, default=20, choices=[10,20,60], help="Resolution in meters (default: 20)")
    args = parser.parse_args()
    zip_paths = args.files
    resolution = args.resolution

    main(zip_paths, resolution)



