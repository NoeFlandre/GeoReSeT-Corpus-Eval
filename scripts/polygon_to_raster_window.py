import rasterio
import numpy as np
from rasterio.features import geometry_window, geometry_mask
from shapely.geometry import box

from georeset_corpus_eval.config import EUNIS_TIF
from georeset_corpus_eval.raster import load_legend

with rasterio.open(EUNIS_TIF) as src:

    square = box(4000000, 3000000, 4010000, 3010000)
    window = geometry_window(src, [square])
    pixels = src.read(1, window=window)

    mask = geometry_mask([square], out_shape = pixels.shape, transform=src.window_transform(window), invert=True)
    inside = pixels[mask]

    valid = inside[inside != 65535]
    print(valid.size)

    values, counts = np.unique(valid, return_counts=True)
    shares = counts / counts.sum()
    print(f"Here are the values present in this geometry: {values}")
    print(f"Here are the shares of these values in this geometry: {shares.round(3)}")

    legend = load_legend()
    max_share, max_share_index = shares.max(), shares.argmax()
    max_share_code = values[max_share_index]
    max_share_label = legend[max_share_code]
    print(f"Dominant share code: {max_share_code}")
    print(f"Dominant share label: {max_share_label}")
