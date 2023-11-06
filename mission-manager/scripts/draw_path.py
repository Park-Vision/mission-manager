import os

import folium
import numpy as np
from mission.path import create_path
from mission.waypoint import Waypoint


def generate_map(points_ordered):
    # Create a map centered at a specific location
    route_points = points_ordered
    centre = np.mean([x for (x, y) in route_points]), np.mean(
        [y for (x, y) in route_points]
    )

    route_line = points_ordered  # folium needs lat, long

    m = folium.Map(location=centre, zoom_start=12, zoom_control=False, max_zoom=21)

    # Create a feature group for the route line
    route_line_group = folium.FeatureGroup(name="Route Line")

    # Add the route line to the feature group
    folium.PolyLine(route_line, color="red", weight=2).add_to(route_line_group)

    # Add the feature group to the map
    route_line_group.add_to(m)

    # Create a feature group for the route points
    route_points_group = folium.FeatureGroup(name="Route Points")

    # Add the route points to the feature group
    names = route_points

    for i, (point, name) in enumerate(zip(route_points, names)):
        folium.Marker(location=point, tooltip=f"{i}: {name}").add_to(route_points_group)

    # Add the feature group to the map
    route_points_group.add_to(m)

    # Create a custom tile layer with a partially greyed out basemap
    custom_tile_layer = folium.TileLayer(
        tiles="http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
        attr="CartoDB Positron",
        name="Positron",
        overlay=True,
        control=True,
        opacity=0.7,  # Adjust opacity to control the level of greying out
    )

    # Add the custom tile layer to the map
    custom_tile_layer.add_to(m)

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    m.save("map.html")
    os.system("firefox map.html")


def draw():
    points = [
        (51.11010, 17.05910),
        (51.11050, 17.05910),
        (51.11050, 17.05920),
        (51.11030, 17.05950),
        (51.11010, 17.05920),
        (51.11010, 17.05930),
        (51.11050, 17.05960),
        (51.11010, 17.05950),
        (51.11050, 17.05940),
        (51.11030, 17.05910),
        (51.11010, 17.05960),
        (51.11010, 17.05940),
        (51.11050, 17.05930),
        (51.11030, 17.05920),
        (51.11030, 17.05930),
        (51.11030, 17.05960),
        (51.11050, 17.05950),
        (51.11030, 17.05940),
    ]
    wps = [Waypoint(1, point[0], point[1]) for point in points]
    path = create_path(wps)
    tuples = [wp.position for wp in path]
    generate_map(tuples)


draw()
