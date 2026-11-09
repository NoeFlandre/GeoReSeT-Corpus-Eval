import rasterio
import math
import pandas as pd

from rasterio.warp import transform
from rasterio.transform import rowcol
from georeset_corpus_eval.config import PHOTOS_DIR, EUNIS_TIF, DATA
from georeset_corpus_eval.sample_places import load_legend
from georeset_corpus_eval.raster import coordinates_finite_and_in_bounds

COLUMNS = ["photo_id", "lat", "lon"]
OUTPUT = DATA / "processed" / "photo_labels.parquet"

def main():
    dataset = pd.read_parquet(PHOTOS_DIR, columns=COLUMNS)

    lons = dataset["lon"].tolist()
    lats = dataset["lat"].tolist()
    legend = load_legend()

    with rasterio.open(EUNIS_TIF) as src:
        xs, ys = transform("EPSG:4326", src.crs, lons, lats) # we transform the longitudes and latitudes into the raster CRS
        bounds = src.bounds # bounds of the raster

        inside, _ = coordinates_finite_and_in_bounds(xs, ys, bounds)
        inside_rows = [i for i, flag in enumerate(inside) if flag] # which rows of coordinates indeed fall inside the bounds?

        rows, cols = rowcol(src.transform, [xs[i] for i in inside_rows], [ys[i] for i in inside_rows]) # to which rows and cols the coordinates falling inside the bounds correspond to inside my raster?
        band = src.read(1)

        codes = band[rows, cols]
        labels = [legend.get(int(code)) for code in codes]

        label_by_row = [None] * len(dataset)
        for i, label in zip(inside_rows, labels):
            label_by_row[i] = label
        dataset["label"] = label_by_row

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        dataset.to_parquet(OUTPUT)

if __name__ == "__main__":
    main()
