import os
from time import time

from json2args import get_parameter
from json2args.logger import logger
from json2args.data import get_data_paths

from config import Config
from delineate import delineate
import utils

# get the tool name
toolname = os.environ.get('TOOL_RUN', 'delineate').lower()

if toolname == 'delineate':
    # start the tool
    logger.info("##TOOL START - delineate")
    start = time()

    # inform about the original tool
    logger.info("This tool is a wrapper for the great delineate.py (https://github.com/mheberger/delineator). Please cite that and give credit to the original author! Heberger, M. (2021). delineator.py: Fast, accurate watershed delineation using hybrid vector- and raster-based methods and data from MERIT-Hydro (Version 1.0) [Computer software]. https://doi.org/10.5281/zenodo.7314287.")

    # get the parameters
    params = get_parameter(typed=True)
    logger.debug(f"PARAMETERS: {params}")

    # get the input data paths
    data_paths = get_data_paths()
    outlet_path = data_paths['outlets']
    logger.debug(f"Outlets: {outlet_path}")

    # create the CSV as delineate.py expects it
    gdf = utils.get_outlets(outlet_path=outlet_path)
    outles_target_path = '/out/outlets.csv'
    utils.save_temporary_outlets(gdf=gdf, target_path=outles_target_path)
    logger.debug(f"Generated input outlets CSV for delineate.py: {outles_target_path}")

    # actual tool 
    conf = Config(
        # pass down the tool parameters to the config
        LOW_RES_THRESHOLD=params.lowres_threshold,

        # settings to overwrite the internals of delineate.py
        # these are needed to run the tool inside the container
        OUTLETS_CSV=outles_target_path,
        MERIT_FDIR_DIR='/data/raster/flowdir_basins',
        MERIT_ACCUM_DIR='/data/raster/accum_basins',
        HIGHRES_CATCHMENTS_DIR='/data/shp/merit_catchments',
        LOWRES_CATCHMENTS_DIR='/data/shp/catchments_simplified',
        RIVERS_DIR='/data/shp/merit_rivers',
        MERIT_BASINS_SHP='/data/shp/basins_level2/merit_hydro_vect_level2.shp',

        # these are the settings that the user should not change - currently
        # the plan is to make these settings controllable for the user
        PLOTS=False,
        MAKE_MAP = False,
        SEARCH_DIST = 0.025,

        # these are the settings that should not be changed by the user
        OUTPUT_DIR='/out',
        PICKLE_DIR = '',
    )
    logger.debug(f"Starting delineate.py with config: {conf}")
    delineate(conf=conf)

    # finish the tool
    logger.info(f"Total runtime: {time() - start:.2f} seconds.")
    logger.info("##TOOL FINISH - delineate")
