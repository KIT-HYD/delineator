from pathlib import Path

import pandas as pd
import geopandas as gpd


def get_outlets(outlet_path: str) -> gpd.GeoDataFrame:
    # first load the data paths
    outlet_path = Path(outlet_path)

    # switch the extension
    if outlet_path.suffix == '.geojson':
        return gpd.read_file(outlet_path)
    elif outlet_path.suffix == '.csv':
        df = pd.read_csv(outlet_path)
        # figure out the geometry columns
        if 'lon' in df.columns and 'lat' in df.columns:
            geometry_cols = [df.lon, df.lat]
        elif 'lng' in df.columns and 'lat' in df.columns:
            geometry_cols = [df.lng, df.lat]
        elif 'x' in df.columns and 'y' in df.columns:
            geometry_cols = [df.x, df.y]
        elif 'longitude' in df.columns and 'latitude' in df.columns:
            geometry_cols = [df.longitude, df.latitude]
        else:
            raise RuntimeError("Could not find geometry columns in CSV file")
        
        return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(*geometry_cols, crs='epsg:4326'))
    else:
        raise RuntimeError(f"Input files of type {outlet_path.suffix} are not supported. Please use a GeoJSON or CSV file.")

def save_temporary_outlets(gdf: gpd.GeoDataFrame, target_path: str = '/out/outlets.csv'):
    # reproject the data to EPSG:4326 if it is not already
    gdf = gdf.to_crs(epsg=4326)
    # create an empty container for the file
    data = gpd.GeoDataFrame()

    # check if the GeoDataFrame has an id. Otherwise we create one
    if 'id' not in gdf.columns:
        data['id'] = gdf.index.astype(str)
    else:
        data['id'] = gdf['id']
    
    # add the geometry
    data['lng'] = gdf.geometry.x
    data['lat'] = gdf.geometry.y

    # check if the two optional columns 'name' and 'area' are present
    if 'name' in gdf.columns:
        data['name'] = gdf['name']
        
    if 'area' in gdf.columns:
        data['area'] = gdf['area']

    # save the data to a temporary CSV file
    data.to_csv(target_path, index=False)