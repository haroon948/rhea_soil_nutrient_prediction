"""Extract WorldClim 2.1 bioclimatic variables and elevation at sample locations."""
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
WORLDCLIM_DIR = RAW / "worldclim"

# These are the column names in the train CSV file
LAT_COL = "Latitude"
LON_COL = "Longitude"


def get_raster_paths():
    """Return the 19 bio rasters followed by the elevation raster, in order."""
    bio = sorted(
        WORLDCLIM_DIR.glob("wc2.1_2.5m_bio_*.tif"),
        key=lambda p: int(p.stem.split("_")[-1]),
    )
    elev = sorted(WORLDCLIM_DIR.glob("wc2.1_2.5m_elev.tif"))
    if len(bio) != 19 or len(elev) != 1:
        raise FileNotFoundError(
            f"Expected 19 bio files and 1 elev file in {WORLDCLIM_DIR}, "
            f"found {len(bio)} and {len(elev)}."
        )
    return bio + elev

def get_monthly_paths(variables=("tavg", "prec")):
    """Return the 12 monthly rasters for each requested variable, in month order."""
    paths = []
    for var in variables:
        files = sorted(WORLDCLIM_DIR.glob(f"wc2.1_2.5m_{var}_*.tif"))
        if len(files) != 12:
            raise FileNotFoundError(
                f"Expected 12 monthly {var} files in {WORLDCLIM_DIR}, found {len(files)}."
            )
        paths.extend(files)
    return paths


def extract_at_points(coords, paths):
    """Sample each raster at (lat, lon) points. Returns one column per raster."""
    # rasterio expects (x, y), which is (lon, lat)
    xy = list(zip(coords[LON_COL], coords[LAT_COL]))
    columns = {}
    for path in paths:
        with rasterio.open(path) as src:
            if src.crs.to_epsg() != 4326:
                raise ValueError(f"{path.name} is not in WGS84 (EPSG:4326)")
            values = np.array([v[0] for v in src.sample(xy)], dtype=float)
            if src.nodata is not None:
                values[values == src.nodata] = np.nan
        columns[path.stem.replace("wc2.1_2.5m_", "")] = values
    return pd.DataFrame(columns)


def process_file(csv_name, paths):
    df = pd.read_csv(RAW / csv_name)
    print(f"{csv_name} columns: {df.columns.tolist()}")

    # Extract once per unique location, then map back to every row
    unique = df[[LAT_COL, LON_COL]].drop_duplicates().reset_index(drop=True)
    feats = pd.concat([unique, extract_at_points(unique, paths)], axis=1)
    rows = df[[LAT_COL, LON_COL]].merge(feats, on=[LAT_COL, LON_COL], how="left")
    rows = rows.drop(columns=[LAT_COL, LON_COL])

    missing = rows.isna().any(axis=1).sum()
    print(f"{csv_name}: {len(rows)} rows, {missing} with missing values")
    return rows

INCLUDE_MONTHLY = True  # set to True for the seasonal experiment

def main():
    paths = get_raster_paths()
    if INCLUDE_MONTHLY:
        paths = paths + get_monthly_paths()
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for csv_name, out_name in [
        ("Train.csv", "worldclim_train.csv"),
        ("TestSet.csv", "worldclim_test.csv"),
    ]:
        feats = process_file(csv_name, paths)
        feats.to_csv(PROCESSED / out_name, index=False)
        print(f"Saved {PROCESSED / out_name}")


if __name__ == "__main__":
    main()