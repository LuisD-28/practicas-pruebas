from faker import Faker
import random
from datetime import datetime, timedelta
from pg_manager import PgManager

faker = Faker()

db = PgManager(
    dbname="postgres",
    user="postgres",
    password="280596",
    host="localhost"
)

# Insert users
def seed_users(num_users=200):
    for _ in range(num_users):
        full_name = faker.name()
        email = faker.email()
        username = faker.user_name()
        password = faker.password(length=10)
        birthdate = faker.date_of_birth(minimum_age=18, maximum_age=60)

        db.cursor.execute(
            """
            INSERT INTO lyfter_car_rental.users 
            (full_name, email, username, password, birthdate)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (full_name, email, username, password, birthdate)# account_status is defaulted to 'active'
        )
        db.connection.commit()
        print(f"{num_users} users inserted successfully.")

# Insert cars
def seed_cars(num_cars=100):
    car_catalog = {
        "Toyota": [
            "Corolla", "Camry", "Yaris", "RAV4", "Highlander",
            "Prius", "Avalon", "Tacoma", "Tundra", "4Runner"
        ],
        "Honda": [
            "Civic", "Accord", "Fit", "CR-V", "HR-V",
            "Pilot", "Odyssey", "Ridgeline"
        ],
        "Ford": [
            "Mustang", "Focus", "Fiesta", "Fusion", "Escape",
            "Explorer", "Expedition", "F-150", "Bronco"
        ],
        "Chevrolet": [
            "Camaro", "Cruze", "Malibu", "Impala", "Tahoe",
            "Suburban", "Silverado", "Equinox", "Trailblazer"
        ],
        "Nissan": [
            "Altima", "Sentra", "Versa", "Maxima", "Rogue",
            "Murano", "Pathfinder", "Frontier", "Titan"
        ],
        "BMW": [
            "320i", "330i", "M3", "M4", "X1",
            "X3", "X5", "X6", "i3", "i8", "Z4", "X6 M competition",
            "M5 competition", "M8 competition", "X7 M50i", "X5 M competition",
            "X3 M competition"
        ],
        "Audi": [
            "A3", "A4", "A5", "A6", "A7",
            "Q3", "Q5", "Q7", "RS3", "RS5",
            "RS7", "S3", "S4", "S5", "S6", "S7", "S8"
        ],
        "Hyundai": [
            "Elantra", "Sonata", "Accent", "Tucson", "Santa Fe",
            "Palisade", "Veloster", "Kona"
        ],
        "Kia": [
            "Rio", "Forte", "Optima", "Soul", "Sportage",
            "Sorento", "Telluride", "Stinger"
        ],
        "Volkswagen": [
            "Golf", "Jetta", "Passat", "Tiguan", "Atlas",
            "Beetle", "GTI", "Arteon"
        ],
        "Mazda": [
            "Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9",
            "MX-5 Miata"
        ],
        "Subaru": [
            "Impreza", "Legacy", "Outback", "Forester", "Crosstrek",
            "Ascent"
        ],
        "Mercedes-Benz": [
            "A-Class", "C-Class", "E-Class", "S-Class", "GLA",
            "GLC", "GLE", "GLS"
        ],
        "Jeep": [
            "Wrangler", "Cherokee", "Grand Cherokee", "Renegade", "Compass",
            "Gladiator", "Patriot", "Commander", "Wagoneer", "Grand Wagoneer"
        ],
        "Tesla": [
            "Model S", "Model 3", "Model X", "Model Y"
        ],
        "Volvo": [
            "S60", "S90", "V60", "V90", "XC40",
            "XC60", "XC90"
        ],
        "Porsche": [
            "911", "Cayenne", "Macan", "Panamera", "Taycan"
        ],
        "Lexus": [
            "IS", "ES", "GS", "LS", "NX",
            "RX", "GX", "LX"
        ],
        "Acura": [
            "ILX", "TLX", "RLX", "RDX", "MDX"
        ],
        "Infiniti": [
            "Q50", "Q60", "Q70", "QX50", "QX60",
            "QX80"
        ],
        "Mitsubishi": [
            "Mirage", "Lancer", "Outlander", "Eclipse Cross", "Pajero"
        ],
        "Land Rover": [
            "Range Rover", "Discovery", "Defender", "Evoque", "Velar"
        ],
        "Jaguar": [
            "XE", "XF", "XJ", "F-PACE", "E-PACE",
            "I-PACE"
        ],
        "Ferrari": [
            "488", "812", "Portofino", "SF90 Stradale", "Roma"
        ],
        "Lamborghini": [
            "Huracan", "Aventador", "Urus", "Gallardo", "Murcielago"
        ],
        "Maserati": [
            "Ghibli", "Quattroporte", "Levante", "GranTurismo", "GranCabrio"
        ],
        "Alfa Romeo": [
            "Giulia", "Stelvio", "4C", "Giulietta", "MiTo"
        ],
        "Bentley": [
            "Continental GT", "Flying Spur", "Mulsanne", "Bentayga"
        ],
        "Rolls-Royce": [
            "Phantom", "Ghost", "Wraith", "Dawn", "Cullinan"
        ],
        "Aston Martin": [
            "Vantage", "DB11", "DBS Superleggera", "Rapide", "Vanquish"
        ],
        "McLaren": [
            "720S", "570S", "600LT", "GT", "P1"
        ],
        "Bugatti": [
            "Chiron", "Veyron", "Divo", "Centodieci", "La Voiture Noire"
        ],
        "Pagani": [
            "Huayra", "Zonda"
        ]
    }
    
    for _ in range(num_cars):
        brand = random.choice(list(car_catalog.keys()))
        model = random.choice(car_catalog[brand])
        year = random.randint(2000, 2025)

        db.cursor.execute(
            """
            INSERT INTO lyfter_car_rental.cars
            (brand, model, manufacturing_year)
            VALUES (%s, %s, %s);
            """,
            (brand, model, year)# car_status is defaulted to 'available'
        )
        db.connection.commit()
        print(f"{num_cars} cars inserted successfully.")

# Insert rentals
def seed_rentals(num_rentals=50):
    # Get Users and Cars from the database
    db.cursor.execute("SELECT user_id FROM lyfter_car_rental.users;")
    users = [row[0] for row in db.cursor.fetchall()]

    db.cursor.execute("SELECT car_id FROM lyfter_car_rental.cars WHERE car_status = 'available';")
    cars = [row[0] for row in db.cursor.fetchall()]

    for _ in range(num_rentals):
        if not cars:
            print("No cars available for rental.")
            break # No more cars available for rental

        user_id = random.choice(users)
        car_id = random.choice(cars)

        # Random rental dates for the last 2 years
        rental_date = faker.date_between(start_date='-2y', end_date='today')

        # Random rental_status
        rental_status = random.choice(['ongoing', 'completed', 'cancelled'])

        # Insert rental
        db.cursor.execute(
            """
            INSERT INTO lyfter_car_rental.rentals
            (user_id, car_id, rental_date, rental_status)
            VALUES (%s, %s, %s, %s);
            """,
            (user_id, car_id, rental_date, rental_status)
        )

        # Set car_status to 'rented' if rental_status is 'ongoing'
        if rental_status == 'ongoing':
            db.cursor.execute(
                """
                UPDATE lyfter_car_rental.cars
                SET car_status = 'rented'
                WHERE car_id = %s;
                """,
                (car_id,)
            )
            # Remove the rented car from the available cars list
            cars.remove(car_id)
    
    db.connection.commit()
    print(f"{num_rentals} rentals inserted successfully.")


if __name__ == "__main__":
    seed_users()
    seed_cars()
    seed_rentals()
    print("Database seeding completed successfully.")