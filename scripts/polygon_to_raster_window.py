import rasterio
from rasterio.windows import Window

import pandas as pd
import numpy as np

import shapely
from shapely.ops import transform

from pyproj import Transformer

from georeset_corpus_eval.config import EUNIS_TIF, POLYGONS_DIR, DATA
from georeset_corpus_eval.raster import load_legend, overlaps_raster, compute_label_shares_polygon_raster, NODATA


input_path = POLYGONS_DIR / "train-00000-of-00015.parquet"
output_path = DATA / "processed" / "polygons_labels_shares.parquet"

df = pd.read_parquet(input_path)
geoms = shapely.from_wkb(df["geometry"].to_numpy())

to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True).transform

with rasterio.open(EUNIS_TIF) as src:

    r = src.bounds
    overlaps = [overlaps_raster(g, to_3035, r) for g in geoms]
    df["overlaps_raster"] = overlaps

    reason = ["bounding_box_no_overlap" if not flag else None for flag in overlaps]


    overlapping = [(i, transform(to_3035, g)) for i, g in enumerate(geoms) if overlaps[i]]

    legend = load_legend()

    all_values = [None] * len(df)
    all_shares = [None] * len(df)
    all_max_share_code = [None] * len(df)
    all_max_share_label = [None] * len(df)
    label_method = [None] * len(df)


    for row, polygon in overlapping:

        result, failure = compute_label_shares_polygon_raster(src, polygon, legend)

        if  result is not None:
            values, shares, max_share_code, max_share_label = result

            all_values[row] = values
            all_shares[row] = shares
            all_max_share_code[row] = max_share_code
            all_max_share_label[row] = max_share_label
            label_method[row] = "polygon"

        elif failure == "all_nodata":
            reason[row] = "all_nodata"

        else:
            x, y = polygon.centroid.x, polygon.centroid.y
            if not (r.left <= x < r.right and r.bottom < y <= r.top):
                reason[row] = "centroid_outside_raster"
                continue

            pixel_row, pixel_col = src.index(x, y)
            code = int(src.read(1, window=Window(pixel_col, pixel_row, 1, 1))[0, 0])

            if code == NODATA:
                reason[row] = "nodata"
                continue

            all_values[row] = np.array([code], dtype=np.uint16)
            all_shares[row] = np.array([1.0])
            all_max_share_code[row] = code
            all_max_share_label[row] = legend[code]
            label_method[row] = "centroid"



    df["eunis_code"] = all_values
    df["eunis_shares"] = all_shares
    df["max_eunis_share_code"] = all_max_share_code
    df["max_eunis_share_label"] = all_max_share_label
    df["label_method"] = label_method
    df["unlabelled_reason"] = reason

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path)

    print(f"Total number of polygons: {len(df)}")
    print(f"We found {sum(overlaps)} overlapping polygons")
    print(f"In the resulting dataset we have {sum(df["eunis_code"].notna())} labeled polygons")
    print(f"Unlabelled reason: {df["unlabelled_reason"].value_counts()}")
