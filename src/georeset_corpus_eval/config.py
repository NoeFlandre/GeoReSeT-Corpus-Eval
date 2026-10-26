from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
EUNIS_DIR = DATA / "raw" / "eunis"
EUNIS_TIF = EUNIS_DIR / "wall_to_wall" / "eunis_dominant.tif"
EUNIS_LEGEND = EUNIS_DIR / "eunis_legend_detailed.csv"
