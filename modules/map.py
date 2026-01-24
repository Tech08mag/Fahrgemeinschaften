import os
import requests
from PIL import ImageDraw, ImageFont
from staticmap import StaticMap, Line, CircleMarker
from geopy.geocoders import Nominatim

def create_drive_map(start_address: str, end_address: str, output_dir=None) -> None:
    """
    Generates a static map image with a driving route between two addresses.
    Saves the image with distance and duration annotated.

    Args:
        start_address (str): Starting address
        end_address (str): Destination address
        output_dir (str, optional): Directory to save the image. Defaults to 'static/drive_images' in project root.

    Returns:
        str: Filepath of the saved image
    """
    # --- Setup directories ---
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    save_dir = output_dir or os.path.join(project_root, "static", "drive_images")
    os.makedirs(save_dir, exist_ok=True)

    filename = f"{start_address.replace(' ', '_')}_to_{end_address.replace(' ', '_')}.png"
    filepath = os.path.join(save_dir, filename)

    # --- Geocode addresses ---
    geolocator = Nominatim(user_agent="map_creator")
    start_location = geolocator.geocode(start_address)
    end_location = geolocator.geocode(end_address)

    if not start_location:
        raise ValueError(f"Could not geocode start address: {start_address}")
    if not end_location:
        raise ValueError(f"Could not geocode end address: {end_address}")

    start_coords = (start_location.longitude, start_location.latitude)  # (lon, lat)
    end_coords = (end_location.longitude, end_location.latitude)

    # --- Request route from OSRM ---
    osrm_url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
        f"?overview=full&geometries=geojson"
    )
    response = requests.get(osrm_url)
    if response.status_code != 200:
        raise ValueError(f"OSRM request failed: {response.status_code}")
    data = response.json()

    if "routes" not in data or len(data["routes"]) == 0:
        raise ValueError("No route found.")

    route_data = data["routes"][0]
    route_coords = [(point[0], point[1]) for point in route_data["geometry"]["coordinates"]]  # (lon, lat)

    distance_km = route_data["distance"] / 1000
    duration_min = route_data["duration"] / 60

    # --- Create static map ---
    m = StaticMap(800, 600, url_template='http://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
    m.add_line(Line(route_coords, 'blue', 4))
    m.add_marker(CircleMarker(start_coords, 'green', 12))
    m.add_marker(CircleMarker(end_coords, 'red', 12))
    image = m.render()

    # --- Annotate image with distance & duration ---
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()  # fallback if truetype not available

    text = f"Distance: {distance_km:.1f} km | Duration: {duration_min:.0f} min"
    draw.text((10, 10), text, fill='black', font=font)

    # --- Save image ---
    image.save(filepath)
