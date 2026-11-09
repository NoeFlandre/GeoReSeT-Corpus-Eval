import pandas as pd
import shapely
from shapely.ops import transform
import rasterio
from pathlib import Path
from pyproj import Transformer

from georeset_corpus_eval.config import EUNIS_TIF

def overlaps_raster(g, to_crs, reference_bounds):
    r = reference_bounds
    x0, y0, x1, y1 = transform(to_crs, g).bounds
    return x0 < r.right and x1 > r.left and y0 < r.top and y1 > r.bottom

def main():

    total_polygons = 0
    polygons_overlapping_raster = 0

    for path in sorted(Path("data/raw/georeset/polygons").glob("*.parquet")):
        df = pd.read_parquet(path, columns=["polygon_id", "geometry"])
        geoms = shapely.from_wkb(df["geometry"].to_numpy())

        with rasterio.open(EUNIS_TIF) as src:
            r = src.bounds
            to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True).transform
            overlaps = [overlaps_raster(g, to_3035, r) for g in geoms]
            total_polygons += len(overlaps)
            polygons_overlapping_raster += sum(overlaps)

    print(f"There are {polygons_overlapping_raster} polygons overlapping the raster out of {total_polygons} polygons")


if __name__ == "__main__":
    main()
