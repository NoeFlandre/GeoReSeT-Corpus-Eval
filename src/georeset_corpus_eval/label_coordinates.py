import rasterio
import pandas as pd

from rasterio.warp import transform
from rasterio.transform import rowcol
from georeset_corpus_eval.raster import load_legend
from georeset_corpus_eval.raster import coordinates_finite_and_in_bounds


def label_coordinates(input_dir, columns, eunis_tif, output_dir):
    dataset = pd.read_parquet(input_dir, columns=columns)

    assert {"lat", "lon"}.issubset(dataset.columns), (
        "Dataset must contain 'lat' and 'lon' columns"
    )

    lons = dataset["lon"].tolist()
    lats = dataset["lat"].tolist()
    legend = load_legend()

    with rasterio.open(eunis_tif) as src:
        xs, ys = transform("EPSG:4326", src.crs, lons, lats) # we transform the longitudes and latitudes into the raster CRS
        bounds = src.bounds # bounds of the raster

        inside, _ = coordinates_finite_and_in_bounds(xs, ys, bounds)
        inside_rows = [i for i, flag in enumerate(inside) if flag] # which rows of coordinates indeed fall inside the bounds?

        rows, cols = rowcol(src.transform, [xs[i] for i in inside_rows], [ys[i] for i in inside_rows]) # to which rows and cols the coordinates falling inside the bounds correspond to inside my raster?
        band = src.read(1)

        codes = band[rows, cols]
        labels = [legend.get(int(code)) for code in codes]

        code_by_row = [None] * len(dataset)
        label_by_row = [None] * len(dataset)

        for i, code, label in zip(inside_rows, codes, labels):
            code = int(code)
            if code != 65535:
                code_by_row[i] = code
                label_by_row[i] = label
        dataset["eunis_code"] = pd.array(code_by_row, dtype="Int64")
        dataset["eunis_label"] = label_by_row


        output_dir.parent.mkdir(parents=True, exist_ok=True)
        dataset.to_parquet(output_dir)
