import pandas as pd
import rasterio
from rasterio.warp import transform
from georeset_corpus_eval.config import PHOTOS_DIR, EUNIS_TIF
from georeset_corpus_eval.raster import coordinates_finite_and_in_bounds

COLUMNS = ["lat", "lon"]

def main():

    dataset = pd.read_parquet(PHOTOS_DIR, columns=COLUMNS)

    lons = dataset["lon"].tolist()
    lats = dataset["lat"].tolist()

    with rasterio.open(EUNIS_TIF) as src:
        xs, ys = transform("EPSG:4326", src.crs, lons, lats)
        bounds = src.bounds
        print(f"First three longitude in degrees: {lons[:3]}")
        print(f"First three longitude in meters: {xs[:3]}")
        print(f"First three latitude in degrees: {lats[:3]}")
        print(f"First three latitude in meters: {ys[:3]}")
        print(f"Bounds: {bounds}")

        inside, valid = coordinates_finite_and_in_bounds(xs, ys, bounds)

        missing_count = len(valid) - sum(valid)
        inside_count = sum(inside)
        outside_count = sum(valid) - inside_count


        print(f"Are the first three photos in bounds? {inside[:3]}")

        print(f"How many photos without coordinates throughout the dataset? {missing_count}")
        print(f"How many photos inside and outside the raster? {inside_count}")
        print(f"How many photos outside the raster? {outside_count}")

if __name__ == "__main__":
    main()
