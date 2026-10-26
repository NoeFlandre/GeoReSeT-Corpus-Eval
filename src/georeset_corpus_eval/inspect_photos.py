import pandas as pd

from georeset_corpus_eval.config import PHOTOS_DIR

COLUMNS = ["scene_id", "platform", "photo_id", "lat", "lon", "country", "continent"]


def main() -> None:
    photos = pd.read_parquet(PHOTOS_DIR, columns=COLUMNS)
    print(f"First rows {photos.head()}")
    print(f"Number of rows: {len(photos)}")
    print(f"Is photo_id unique?: {photos["photo_id"].is_unique}")
    print(f"Is (platform, photo_id) unique?: {not photos.duplicated(["platform", "photo_id"]).any()}")
    print(f"Number of countries: {photos["country"].nunique()}")
    print(f"Number of continents: {photos["continent"].nunique()}")
    print(f"Number of missing (lat, lon): {photos[["lat", "lon"]].isna().sum()}")



if __name__ == "__main__":
    main()
