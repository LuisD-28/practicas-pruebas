from faker import Faker
import random

from managers.user_manager import UserManager
from managers.car_manager import CarManager
from managers.address_manager import AddressManager

from database import (
    validate_connection,
    validate_and_create_schema,
    validate_and_create_tables
)

fake = Faker()

u = UserManager()
c = CarManager()
a = AddressManager()

def seed_database():

    print("\nSeed initialization...")

    # User seed
    users = []
    for _ in range(25):
        full_name = fake.name()
        email = fake.email()
        username = fake.user_name()
        password = fake.password()

        user = u.create_user(
            full_name=full_name,
            email=email,
            username=username,
            password=password
        )

        users.append(user)
        print(f"User created: ID:{user.id}, Name:{user.full_name}")

        # Adress seed for each user
        street = fake.street_address()
        city = fake.city()
        state = fake.state()
        zip_code = fake.zipcode()

        address = a.create_address(
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            user_id=user.id
        )

        print(f"Address created for User Name:{user.full_name}, Street:{address.street}, City:{address.city}, State:{address.state}, Zip Code:{address.zip_code}")

        # Car seed for some users
        num_cars = random.randint(0, 2) 

        for _ in range(num_cars):
            brand = fake.company()
            model = fake.word()
            manufacture_year = random.randint(1995, 2026)

            # Some cars will be assigned to users, while others will not have an associated user
            owner_id = user.id if random.random() < 0.5 else None

            car = c.create_car(
                brand=brand,
                model=model,
                manufacture_year=manufacture_year,
                user_id=owner_id
            )
            if owner_id:
                print(f"Car created for User Name:{user.full_name}, Brand:{car.brand}, Model:{car.model}, Year:{car.manufacture_year}")

if __name__ == "__main__":
    validate_connection()
    validate_and_create_schema()
    validate_and_create_tables()
    seed_database()
    
    print("\nSeed completed successfully.")




