import pandas as pd
import shapely
from shapely.ops import transform
import rasterio
from pathlib import Path
from pyproj import Transformer

from georeset_corpus_eval.config import EUNIS_TIF
from georeset_corpus_eval.raster import overlaps_raster



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
