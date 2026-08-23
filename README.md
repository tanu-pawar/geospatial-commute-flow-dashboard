# Exercise 5 — Geospatial Commute Flow Dashboard

## Purpose
This project implements the Exercise 5 workflow for Big Data Visualization in Geoinformatics.
It creates an interactive 3D origin-destination commute-flow map and an additional visualization
from the same filtered dataset.

## Dataset
Bay Area commute-route CSV specified in the practical task sheet:

`https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv`

## Important fields

- `lng_h` — home longitude / source X
- `lat_h` — home latitude / source Y
- `lng_w` — work longitude / target X
- `lat_w` — work latitude / target Y
- `S000` — flow / job count

## Spatial filter

The dashboard uses the downtown San Francisco bounding box specified in Exercise 5:

- West: `-122.43135291617365`
- South: `37.766492914983864`
- East: `-122.38706428091974`
- North: `37.80583561830737`

Both home and workplace coordinates must fall inside the box.

## Visualizations

1. **Interactive 3D Arc Map**
   - Home/source: orange-red
   - Work/destination: green
   - Arc width: proportional to `S000`
   - 3D pitch/bearing
   - Hover tooltip
   - Pan/zoom/rotation

2. **Additional visualization**
   - Interactive Top 10 Commute Flows bar chart
   - Uses `S000` from the same filtered dataset

## Files

- `index.html` — dashboard landing page
- `arc_layer_map.html` — browser-runnable 3D ArcLayer map
- `extra_visualization.html` — interactive Plotly bar chart
- `analysis.py` — Python/PyDeck/Plotly source workflow
- `Geospatial_Bigdata_and_3D_Visualization.ipynb` — provided notebook
- `README.md` — project documentation

## Python execution

Install the required packages:

```bash
python -m pip install pandas pydeck plotly
```

Then run:

```bash
python analysis.py
```

This generates `arc_layer_map.html` and `extra_visualization.html` using PyDeck and Plotly.

