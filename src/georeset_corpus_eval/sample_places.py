import csv

import rasterio
from rasterio.warp import transform


from georeset_corpus_eval.config import EUNIS_LEGEND, EUNIS_TIF

PLACES = {
    "Paris centre": (2.3488, 48.8534),
    "Fontainebleau forest": (2.6700, 48.4000),
    "Beauce farmland": (1.7000, 48.2000),
    "Mont Blanc summit": (6.8650, 45.8326),
    "Bay of Biscay": (-5.0000, 46.0000),
    "Moscow": (37.6176, 55.7558),
}

def load_legend() -> dict[int, str]:
    with open(EUNIS_LEGEND, newline="") as f:
        return {int(row["Code"]): row["Label"] for row in csv.DictReader(f)}

def main() -> None:
    legend = load_legend()

    lons = [lon for lon, lat in PLACES.values()]
    lats = [lat for lon, lat in PLACES.values()]

    with rasterio.open(EUNIS_TIF) as src:
        xs, ys = transform("EPSG:4326", src.crs, lons, lats)
        values = src.sample(zip(xs, ys))

        for name, x, y, value in zip(PLACES, xs, ys, values):
            code = int(value[0])
            row, col = src.index(x, y)
            print(f"Name: {name}, x: {x:9.0f}, y:{y:9.0f}, Row:{row}, Col:{col}, Code: {code}, Label:{legend[code]}")


if __name__ == "__main__":
    main()
