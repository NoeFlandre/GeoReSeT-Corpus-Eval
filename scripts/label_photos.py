from georeset_corpus_eval.label_coordinates import label_coordinates
from georeset_corpus_eval.config import PHOTOS_DIR, EUNIS_TIF, DATA

COLUMNS = ["photo_id", "lat", "lon"]
OUTPUT_DIR = DATA / "processed" / "photo_labels.parquet"

def main():

    label_coordinates(input_dir=PHOTOS_DIR, columns=COLUMNS, eunis_tif=EUNIS_TIF, output_dir=OUTPUT_DIR)

if __name__ == "__main__":
    main()
