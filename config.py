"""
Configuration / Settings for delineator.py

Edit this file carefully before running delineator.py

See README for more information about the options and for instructions
on how to download the input data for delineating watersheds in areas
outside of the sample data provided for Iceland.

"""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# load any configuration which might be available in a .env file
load_dotenv()

# autoload the settings from the environment. 
class Config(BaseSettings):
    # Path to your CSV file with the watershed outlet data
    OUTLETS_CSV: str = 'outlets_sample.csv'

    # Set to True for "higher resolution" mode or False for "lower resolution."
    HIGH_RES: bool = True

    # Directory containing the merged, basin-scale MERIT-Hydro flow direction rasters (.tif)
    # Download from https://mghydro.com/watersheds/rasters
    # For all paths, do not include a trailing slash.
    MERIT_FDIR_DIR: str = "data/raster/flowdir_basins"

    # Directory containing the merged, basin-scale MERIT-Hydro flow accumulation rasters (.tif)
    # Download from https://mghydro.com/watersheds/rasters
    MERIT_ACCUM_DIR: str = "data/raster/accum_basins"

    # Set to True if you want the script to write status messages to the console
    VERBOSE: bool = True

    # Set to True to make a bunch of plots of each watershed.
    # (Just for debugging. Slows down the script a lot.)
    PLOTS: bool = True

    # Folder where you have stored the Merit-BASINS catchment shapefiles.
    # These files need to be downloaded from: https://www.reachhydro.org/home/params/merit-basins
    HIGHRES_CATCHMENTS_DIR: str = "data/shp/merit_catchments"

    # Location of simplified unit catchment boundaries vector data (shapefiles)
    # Download from: https://mghydro.org/watersheds/share/catchments_simplified.zip
    LOWRES_CATCHMENTS_DIR: str = "data/shp/catchments_simplified"

    # Folder where you have stored the MERIT-Basins River flowline shapefiles
    # Download from: https://www.reachhydro.org/home/params/merit-basins
    RIVERS_DIR: str = "C:/Data/GIS/MERITBasins/rivers"

    # EDIT mmaelicke:
    # This file was in the original repo and hardcoded in the script.
    # I move this into the config for reasons of readability and clarity.
    # This file has the merged "megabasins_gdf" in it
    MERIT_BASINS_SHP: str = 'data/shp/basins_level2/merit_hydro_vect_level2.shp'

    # Folder where the script will write the output GeoJSON files or shapefiles
    OUTPUT_DIR: str = "output"

    # The file extension will determine the types of geodata files the script creates.
    #   "gpkg" for GeoPackage (recommended)
    #   "geojson" for GeoJSON files
    #   "shp" for shapefile
    # Use a blank string "" if you DO NOT want any geodata files (for example,
    # you are only making the interactive map and don't need geodata).
    # Other file formats are available;
    # see: https://geopandas.org/en/stable/docs/user_guide/io.html#writing-spatial-data
    OUTPUT_EXT: str = "gpkg"

    # Set to True to ouput a summary of the delineation in OUTPUT.CSV
    OUTPUT_CSV: bool = True

    # Directory to store Python pickle files. Because it can be slow for Python to
    # read shapefiles and create a GeoDataFrame. Once you have done this once, you
    # can save time in the future by storing the GeoDataFrame as a .pkl file.
    # Enter a blank string, '' if you do NOT want the script to create .pkl files.
    # Please note that these files can be large! (Up to around 1 GB for large basins.)
    PICKLE_DIR: str = 'pkl'

    # Threshold for watershed size in km² above which the script will revert to
    # low-resolution mode 
    LOW_RES_THRESHOLD: int = 50000

    # If the requested watershed outlet is not inside a catchment, how far away 
    # from the point should we look for the nearest catchment (in degrees). 0.025 recommended
    SEARCH_DIST: float = 0

    # Watersheds created with Merit-Hydro data tend to have many "donut holes"
    # ranging from one or two pixels to much larger.
    FILL: bool = True

    # If FILL = True, you many choose to to fill donut holes that are below a
    # certain size. This is the number of pixels, on the 3 arcsecond grid. 
    # Set to 0 to fill ALL holes.
    FILL_THRESHOLD: int = 100

    # Simplify the watershed boundary? This will remove some vertices 
    # from the watershed boundary and output smaller files.
    SIMPLIFY: bool = False

    # If SIMPLIFY is True, set SIMPLIFY_TOLERANCE to a value in decimal degrees.
    SIMPLIFY_TOLERANCE: float = 0.0008

    # Set to TRUE if you want the script to create a local web page where you 
    # can review the results.
    MAKE_MAP: bool = True

    # Folder where the script should put the map files. (MAKE sure it exists!)
    # The mapping routine will make _viewer.html and .js files for every watershed
    MAP_FOLDER: str = "map"

    # On the map, do you also want to include the rivers?
    MAP_RIVERS: bool = True

    # On the web page map, if MAP_RIVERS is True, how many stream orders shall we display?
    # I recommend 4 or less. More than this and the browser may not display all the rivers in a large watershed.
    NUM_STREAM_ORDERS: int = 3

    # Set to True to use the experimental match areas feature. 
    # You must include the field `area` in your outlets CSV file to use this feature (in km²)
    MATCH_AREAS: bool = False

    # If you set MATCH_AREAS = True, how close of a match should the script look for?
    # Enter 0.25 for 25%. If you set MATCH_AREAS to False you can ignore this parameter.
    AREA_MATCHING_THRESHOLD: float = 0.25

    # If you set MATCH_AREAS = True, how far away from the original outlet point should the script look 
    # for a river reach that is a better match in terms of upstream area?
    # Units are decimal degrees (sorry, not a proper distance measurement, this feature could be improved!)
    # 0.1° is about 11 km near the equator, and about 8 km near at a latitude of 45°
    MAX_DIST: float = 0.075

    # Threshold for number of upstream pixels that defines a stream
    # These values worked will in my testing, but you might try changing if the
    # outlet is not getting snapped to a river centerline properly
    THRESHOLD_SINGLE: int = 500
    THRESHOLD_MULTIPLE: int = 5000
