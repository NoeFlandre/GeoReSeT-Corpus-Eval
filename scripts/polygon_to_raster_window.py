import rasterio

import pandas as pd

import shapely
from shapely.ops import transform

from pyproj import Transformer

from georeset_corpus_eval.config import EUNIS_TIF, POLYGONS_DIR, DATA
from georeset_corpus_eval.raster import load_legend, overlaps_raster, compute_label_shares_polygon_raster


input_path = POLYGONS_DIR / "train-00000-of-00015.parquet"
output_path = DATA / "processed" / "polygons_labels_shares.parquet"

df = pd.read_parquet(input_path)
geoms = shapely.from_wkb(df["geometry"].to_numpy())

to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True).transform

with rasterio.open(EUNIS_TIF) as src:

    r = src.bounds
    overlaps = [overlaps_raster(g, to_3035, r) for g in geoms]

    overlapping = [(i, transform(to_3035, g)) for i, g in enumerate(geoms) if overlaps[i]]

    legend = load_legend()

    all_values = [None] * len(df)
    all_shares = [None] * len(df)
    all_max_share_code = [None] * len(df)
    all_max_share_label = [None] * len(df)

    for row, polygon in overlapping:

        result = compute_label_shares_polygon_raster(src, polygon, legend)

        if  result is not None:
            values, shares, max_share_code, max_share_label = result

            all_values[row] = values
            all_shares[row] = shares
            all_max_share_code[row] = max_share_code
            all_max_share_label[row] = max_share_label

    df["overlaps_raster"] = overlaps
    df["eunis_code"] = all_values
    df["eunis_shares"] = all_shares
    df["max_eunis_share_code"] = all_max_share_code
    df["max_eunis_share_label"] = all_max_share_label

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path)

    print(f"We found {sum(overlaps)} overlapping polygons")
    print(f"In the resulting dataset we have {sum(df["eunis_code"].notna())} labeled polygons")
    print(f"There are {((df["area_m2"] < 10_000) & (df["eunis_code"].isna()) & (df["overlaps_raster"])).sum()} polygons with an area smaller than 10,000 m2 and having no eunis label but still overlapping")
