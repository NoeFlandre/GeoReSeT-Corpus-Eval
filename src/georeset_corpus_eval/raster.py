import math
import csv
import numpy as np
from shapely.ops import transform
from georeset_corpus_eval.config import EUNIS_LEGEND
from rasterio.features import geometry_window, geometry_mask


def load_legend() -> dict[int, str]:
    with open(EUNIS_LEGEND, newline="") as f:
        return {int(row["Code"]): row["Label"] for row in csv.DictReader(f)}

def coordinates_finite_and_in_bounds(xs, ys, bounds):
    xs_in_bounds = [bounds.left <= x < bounds.right for x in xs]
    ys_in_bounds = [bounds.bottom < y <= bounds.top for y in ys]

    valid = [math.isfinite(x) and math.isfinite(y) for x, y in zip(xs, ys)]

    inside = [v and x and y for v, x, y in zip(valid, xs_in_bounds, ys_in_bounds)]

    return inside, valid

def overlaps_raster(g, to_crs, reference_bounds):
    r = reference_bounds
    x0, y0, x1, y1 = transform(to_crs, g).bounds
    return x0 < r.right and x1 > r.left and y0 < r.top and y1 > r.bottom

def compute_label_shares_polygon_raster(src, polygon, legend):

    window = geometry_window(src, [polygon])
    pixels = src.read(1, window=window)

    mask = geometry_mask([polygon], out_shape = pixels.shape, transform=src.window_transform(window), invert=True)
    inside = pixels[mask]

    valid = inside[inside != 65535]
    if len(valid) == 0:
        return None

    values, counts = np.unique(valid, return_counts=True)
    shares = counts / counts.sum()

    max_share_index = shares.argmax()
    max_share_code = values[max_share_index]
    max_share_label = legend[max_share_code]


    return values, shares, max_share_code, max_share_label
