import os
from typing import Literal, List
from pathlib import Path
import subprocess
import shutil

RASTER_URL = 'https://mghydro.com/watersheds/rasters'
SHAPE_URL = 'https://merit.mmaelicke.de'
LOWRES_URL = 'https://mghydro.com/watersheds/share/catchments_simplified.zip'

ALL_CODES = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56, 57, 61, 62, 63, 64, 65, 66, 67, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 91]

def download(region_code: int | List[int] | Literal['all'], path: str = '/data'):
    if region_code == 'all':
        codes = ALL_CODES
    elif isinstance(region_code, int):
        codes = [region_code]
    else:
        codes = region_code
    
    for code in codes:
        # first download the basin rasters
        download_merit_basins(code, path)

        # then download the catchment and river shapefiles
        download_merit_catchments(code, path)

        # only download the lowres catchments if they are not yet there
        lowres_path = Path(path) / 'shp' / 'catchments_simplified'
        if  len(list(lowres_path.glob(f"*pfaf_{code}_*.shp")))  == 0:
            download_simplified_catchments(path)
    

def download_merit_basins(region_code: int, path: str = '/data'):
    # download the accumulation raster
    accu_url = f"{RASTER_URL}/accum_basins/accum{region_code}.tif"

    # make sure the path exists
    PATH = Path(path) / 'raster'
    (PATH / 'accum_basins').mkdir(parents=True, exist_ok=True)
    (PATH / 'flowdir_basins').mkdir(parents=True, exist_ok=True)

    # get the file
    accu_target = PATH / 'accum_basins' / f'accum{region_code}.tif'
    subprocess.run(['wget', '--no-clobber', accu_url, '-O', accu_target])

    # download the flow direction raster
    flow_dir_url = f"{RASTER_URL}/flow_dir_basins/flowdir{region_code}.tif"
    
    # get the file
    flow_dir_target = PATH / 'flowdir_basins' / f'flowdir{region_code}.tif'
    subprocess.run(['wget', '--no-clobber', flow_dir_url, '-O', flow_dir_target])


def download_merit_catchments(region_code: int, path: str = '/data'):
    # download the zip file of the catchment and river shapefiles
    file_name = f"pfaf_{region_code}_MERIT_Hydro_v07_Basins_v01.zip"
    catch_url = f"{SHAPE_URL}/{file_name}"
    subprocess.run(['wget', '--no-clobber', catch_url, '-O', file_name])

    # unzip the file into a temporary folder and copy to the right place
    subprocess.run(['unzip', '-d', 'tmp', '-o', file_name])
    
    # create the target directory if not exists
    PATH = Path(path) / 'shp'
    (PATH / 'merit_catchments').mkdir(parents=True, exist_ok=True)
    (PATH / 'merit_rivers').mkdir(parents=True, exist_ok=True)

    # move the files to the right place
    subprocess.run(f"mv tmp/cat_* {PATH / 'merit_catchments'}", shell=True)
    subprocess.run(f"mv tmp/riv_* {PATH / 'merit_rivers'}", shell=True)

    # remove the temporary folder
    shutil.rmtree('tmp')
    
    # remove the zipfile
    os.unlink(file_name)


def download_simplified_catchments(path: str = '/data'):
    # get the path
    PATH = Path(path) / 'shp' / 'catchments_simplified'
    
    # download the lowres files
    subprocess.run(['wget', '--no-clobber', LOWRES_URL, '-O', 'catchments_simplified.zip'])

    # unzip
    subprocess.run(['unzip', 'catchments_simplified.zip'])

    # move all the stuoff over
    subprocess.run(f"mv catchments_simplified/* {PATH}", shell=True)

    # remove the folder
    shutil.rmtree('catchments_simplified')

    # remove the zipfile
    os.unlink('catchments_simplified.zip')

if __name__ == "__main__":
    import fire
    fire.Fire(download)
