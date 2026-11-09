import rasterio
import numpy as np
from rasterio.features import geometry_window, geometry_mask
from shapely.geometry import box

from georeset_corpus_eval.config import EUNIS_TIF

with rasterio.open(EUNIS_TIF) as src:

    square = box(4000000, 3000000, 4010000, 3010000)
    window = geometry_window(src, [square])
    pixels = src.read(1, window=window)

    mask = geometry_mask([square], out_shape = pixels.shape, transform=src.window_transform(window), invert=True)
    inside = pixels[mask]
    values, counts = np.unique(inside, return_counts=True)
    print(values, counts)
