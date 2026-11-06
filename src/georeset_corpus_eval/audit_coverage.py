import pandas as pd
import rasterio
import math
from rasterio.warp import transform
from georeset_corpus_eval.config import PHOTOS_DIR, EUNIS_TIF

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

        xs_in_bounds = [bounds.left <= x <= bounds.right for x in xs]
        ys_in_bounds = [bounds.bottom <= y <= bounds.top for y in ys]

        valid = [math.isfinite(x) and math.isfinite(y) for x, y in zip(xs, ys)]
        inside = [v and x and y for v, x, y in zip(valid, xs_in_bounds, ys_in_bounds)]

        missing_count = len(valid) - sum(valid)
        inside_count = sum(inside)
        outside_count = sum(valid) - inside_count

        print(f"Are the first three longitudes in bounds? {xs_in_bounds[:3]}")
        print(f"Are the first three latitudes in bounds? {ys_in_bounds[:3]}")
        print(f"Are the first three photos in bounds? {inside[:3]}")

        print(f"How many photos without coordinates throughout the dataset? {missing_count}")
        print(f"How many photos inside and outside the raster? {inside_count}")
        print(f"How many photos outside the raster? {outside_count}")

if __name__ == "__main__":
    main()
