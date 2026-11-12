from georeset_corpus_eval.config import EUNIS_TIF, POLYGONS_DIR, DATA
from georeset_corpus_eval.label_coordinates import label_coordinates


COLUMNS = ["polygon_id", "lat", "lon"]
OUTPUT = DATA / "processed" / "polygon_labels.parquet"

def main():

    label_coordinates(input_dir=POLYGONS_DIR, columns=COLUMNS, eunis_tif=EUNIS_TIF, output_dir=OUTPUT)

if __name__ == "__main__":
    main()
