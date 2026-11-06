In this repository we are evaluating the following dataset: https://huggingface.co/datasets/NoeFlandre/GeoReSeT-Corpus-Fused

We are first focusing on using EUNIS to evaluate this dataset. The EUNIS data was fetched using the following commands: 

curl -L -o data/raw/eunis/wall_to_wall.zip "https://zenodo.org/records/16985100/files/wall_to_wall.zip?download=1"

curl -L -o data/raw/eunis/eunis_legend_detailed.csv "https://zenodo.org/records/16985100/files/eunis_legend_detailed.csv?download=1"

The scene photos were downloaded using the following command: 

uvx --from huggingface_hub hf download \
  NoeFlandre/GeoReSeT-Corpus-Fused \
  --repo-type dataset \
  --include "scene_photos/*" \
  --local-dir data/raw/georeset
