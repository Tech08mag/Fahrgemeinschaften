import random
import csv
from datetime import date, timedelta
from main import register_user, add_drive
from modules.map import create_drive_map

# -------------------------------
# Helper functions
# -------------------------------
def create_test_user(email, username, password):
    register_user(username, email, password)

def create_test_drive(
    organizer, date, time, price,
    start_address, start_house_number, start_postal_code, start_place,
    end_address, end_house_number, end_postal_code, end_place, seat_amount
):
    add_drive(
        organizer, date, time, price, seat_amount,
        start_address, start_house_number, start_postal_code, start_place,
        end_address, end_house_number, end_postal_code, end_place
    )

def load_addresses_from_csv(filename):
    addresses = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("street") and row.get("housenumber"):
                addresses.append({
                    "addr:street": row["street"],
                    "addr:housenumber": row["housenumber"],
                    "addr:postcode": row.get("postcode", ""),
                    "addr:city": row.get("city", "Unknown City")
                })
    return addresses

# -------------------------------
# Main script
# -------------------------------
if __name__ == "__main__":
    test_username = "testuser"
    test_email = "testuser@example.com"
    test_password = "testpass"

    create_test_user(test_email, test_username, test_password)
    print(f"Test user '{test_username}' created.")

    # Load addresses from CSV
    all_addresses = load_addresses_from_csv("germany_addresses.csv")
    if len(all_addresses) < 2:
        raise RuntimeError("Not enough addresses in CSV to create test drives.")

    base_date = date(2024, 12, 25)

    # Generate 100 test drives
    for i in range(100):
        start = random.choice(all_addresses)
        end = random.choice(all_addresses)
        while end == start:
            end = random.choice(all_addresses)

        try:
            create_test_drive(
            organizer=test_username,
            date=(base_date + timedelta(days=i % 30)).isoformat(),
            time=f"{8 + (i % 12):02d}:{'00' if i % 2 == 0 else '30'}",
            price=12.0 + (i % 10),
            seat_amount=(i % 4) + 1,

            start_address=start.get("addr:street", "Unknown Street"),
            start_house_number=start.get("addr:housenumber", "0"),
            start_postal_code=start.get("addr:postcode", ""),
            start_place=start.get("addr:city", "Unknown City"),

            end_address=end.get("addr:street", "Unknown Street"),
            end_house_number=end.get("addr:housenumber", "0"),
            end_postal_code=end.get("addr:postcode", ""),
            end_place=end.get("addr:city", "Unknown City")
        )
            start_address = f"{start.get('addr:street', 'Unknown Street')} " \
                f"{start.get('addr:housenumber', '0')} " \
                f"{start.get('addr:postcode', '')} " \
                f"{start.get('addr:city', 'Unknown City')}"

            end_address = f"{end.get('addr:street', 'Unknown Street')} " \
              f"{end.get('addr:housenumber', '0')} " \
              f"{end.get('addr:postcode', '')} " \
              f"{end.get('addr:city', 'Unknown City')}"
            create_drive_map(start_address, end_address)
        except:
            pass

        print(f"Test drive {i+1} created: {start.get('addr:street')} ({start.get('addr:city')}) → "
              f"{end.get('addr:street')} ({end.get('addr:city')})")
