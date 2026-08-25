from database import (validate_connection, validate_and_create_schema, validate_and_create_tables)
from managers.user_manager import UserManager
from managers.car_manager import CarManager
from managers.address_manager import AddressManager


def setup_database():
    validate_connection()
    validate_and_create_schema()
    validate_and_create_tables()

def run_exercise():
    u = UserManager()
    c = CarManager()
    a = AddressManager()

    print('\nUsers with more than 1 car:')
    users = u.get_users(min_cars=2)
    for user in users:
        print(f"User ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Username: {user.username}")
        for car in user.cars:
            print(f"  Car ID: {car.id}, Make: {car.brand}, Model: {car.model}, Year: {car.manufacture_year}")
    
    # print('\nUsers without cars:')
    # users_without_cars = u.get_users(has_cars=False)
    # for user in users_without_cars:
    #     print(f"User ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Username: {user.username}")

    # print('\nAll users:')
    # all_users = u.get_users()
    # for user in all_users:
    #     print(f"User ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Username: {user.username}")

    # print('\nAll cars:')
    # all_cars = c.get_cars()
    # for car in all_cars:
    #     print(f"Car ID: {car.id}, Make: {car.brand}, Model: {car.model}, Year: {car.manufacture_year}, User ID: {car.user_id}")

    # print('\nCars assigned to users:')
    # cars_with_users = c.get_cars(owner=True)
    # for car in cars_with_users:
    #     print(f"Car ID: {car.id}, Make: {car.brand}, Model: {car.model}, Year: {car.manufacture_year}, User ID: {car.user_id}")

    print('\nCars without owner:')
    cars_without_users = c.get_cars(owner=False)
    for car in cars_without_users:
        print(f"Car ID: {car.id}, Make: {car.brand}, Model: {car.model}, Year: {car.manufacture_year}, User ID: {car.user_id}")
    
    # Address with a filter substring
    print('\nAddresses with the word "Suite":')
    addresses_with_suite = a.get_addresses(substring="Suite")
    for address in addresses_with_suite:
        print(f"Address ID: {address.id}, Street: {address.street}, City: {address.city}, State: {address.state}, Zip Code: {address.zip_code}, User ID: {address.user_id}")

    # Print user details by ID
    u.print_user_details(1) 
    u.print_user_details(10)  




if __name__ == "__main__":
    setup_database()
    run_exercise()
    