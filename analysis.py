"""
Exercise 5 - Big Data Visualization in Geoinformatics
Interactive Geospatial Commute-Flow Dashboard

Run:
    python analysis.py

Requirements:
    pandas
    pydeck
    plotly

The script follows the Exercise 5 workflow:
load -> validate -> clean -> bounding-box filter ->
PyDeck ArcLayer -> HTML export -> Plotly visualization.
"""

import pandas as pd
import pydeck as pdk
import plotly.express as px

DATA_URL = (
    "https://raw.githubusercontent.com/ajduberstein/"
    "sf_public_data/master/bay_area_commute_routes.csv"
)

REQUIRED_COLUMNS = ["lng_h", "lat_h", "lng_w", "lat_w", "S000"]

DOWNTOWN_BOUNDING_BOX = [
    -122.43135291617365,  # west
    37.766492914983864,   # south
    -122.38706428091974,  # east
    37.80583561830737,    # north
]

HOME_COLOR = [240, 100, 0, 160]
WORK_COLOR = [0, 200, 100, 160]

# 1. Load and inspect
df = pd.read_csv(DATA_URL)
print(f"Rows loaded: {len(df):,}")
print(df.head())
print(df.columns.tolist())

# 2. Validate
missing_columns = [c for c in REQUIRED_COLUMNS if c not in df.columns]
if missing_columns:
    raise ValueError("Missing required columns: " + ", ".join(missing_columns))

# 3. Clean
for column in REQUIRED_COLUMNS:
    df[column] = pd.to_numeric(df[column], errors="coerce")
df = df.dropna(subset=REQUIRED_COLUMNS).copy()

# 4. Bounding-box filter
west, south, east, north = DOWNTOWN_BOUNDING_BOX

home_inside = (
    df["lng_h"].between(west, east)
    & df["lat_h"].between(south, north)
)
work_inside = (
    df["lng_w"].between(west, east)
    & df["lat_w"].between(south, north)
)

commutes = df.loc[home_inside & work_inside].copy()

print(f"Rows before filtering: {len(df):,}")
print(f"Rows after filtering: {len(commutes):,}")

if commutes.empty:
    raise ValueError("No commute records remain after filtering.")

# 5. 3D ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=commutes,
    get_source_position=["lng_h", "lat_h"],
    get_target_position=["lng_w", "lat_w"],
    get_source_color=HOME_COLOR,
    get_target_color=WORK_COLOR,
    get_width="S000",
    width_scale=2,
    width_min_pixels=1,
    width_max_pixels=12,
    get_tilt=15,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=37.786,
    longitude=-122.409,
    zoom=12,
    bearing=35,
    pitch=50,
)

tooltip = {
    "html": """
        <b>Commute Flow</b><br>
        Jobs: <b>{S000}</b><br>
        Home: Orange-Red<br>
        Work: Green
    """,
    "style": {
        "color": "white",
        "backgroundColor": "#222222",
    },
}

deck = pdk.Deck(
    layers=[arc_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
)

deck.to_html("arc_layer_map.html", open_browser=False)

# 6. Additional visualization: top 10 commute flows
top10 = commutes.nlargest(10, "S000").reset_index(drop=True)
top10["Flow Rank"] = range(1, len(top10) + 1)
top10["Commute"] = [
    f"Flow {i}" for i in top10["Flow Rank"]
]

fig = px.bar(
    top10.sort_values("S000"),
    x="S000",
    y="Commute",
    orientation="h",
    title="Top 10 Commute Flows by Job Count",
    labels={"S000": "Flow / Job Count", "Commute": "Commute Flow"},
    hover_data=["lng_h", "lat_h", "lng_w", "lat_w"],
)
fig.write_html(
    "extra_visualization.html",
    include_plotlyjs="cdn",
)

print("Created arc_layer_map.html")
print("Created extra_visualization.html")
