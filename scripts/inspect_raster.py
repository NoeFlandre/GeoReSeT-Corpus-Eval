import rasterio

from georeset_corpus_eval.config import EUNIS_TIF


def main() -> None:
    with rasterio.open(EUNIS_TIF) as src:
        print("CRS:", src.crs.to_epsg())
        print("Size (cols x rows):", src.width, "x", src.height)
        print("Pixel size (m):", src.res)
        print("Bounds:", src.bounds)
        print("Transform:", src.transform)
        print("DType:", src.dtypes[0], "| nodata:", src.nodata)
        print("Block shape:", src.block_shapes[0], "| compression:", src.compression)


if __name__ == "__main__":
    main()
