from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def generate_booking_data():
    """Generate random booking data"""
    checkin = datetime.now() + timedelta(days=random.randint(1, 30))
    checkout = checkin + timedelta(days=random.randint(1, 14))

    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": random.randint(100, 1000),
        "depositpaid": random.choice([True, False]),
        "bookingdates": {
            "checkin": checkin.strftime("%Y-%m-%d"),
            "checkout": checkout.strftime("%Y-%m-%d")
        },
        "additionalneeds": random.choice(["Breakfast", "Lunch", "Dinner", "Parking", None])
    }