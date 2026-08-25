from database import SessionLocal
from models import Car, User
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class UserManager:

    def create_user(self, full_name, email, username, password):
        with SessionLocal() as session:
            new_user = User(
                full_name=full_name,
                email=email,
                username=username,
                password=password
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
    
    # Only the fields listed in ALLOWED_UPDATE_FIELDS can be updated
    ALLOWED_UPDATE_FIELDS = {"full_name", "email", "username", "password"}
    def update_user(self, user_id, **kwargs):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                return None
            
            for key, value in kwargs.items():
                if key in self.ALLOWED_UPDATE_FIELDS:
                    setattr(user, key, value)
                else:
                    print(f"Field User'{key}' is not allowed to be updated.")

            session.commit()
            session.refresh(user)
            return user
        
    def delete_user(self, user_id):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                return False
            
            session.delete(user)
            session.commit()
            return True
        
    def get_users(self, min_cars=None, has_cars=None):
        with SessionLocal() as session:
        
            # Query all users
            if min_cars is None and has_cars is None:
                return (
                    session.query(User)
                    .outerjoin(Car)
                    .order_by(User.id)
                    .all()
                )

            # User without cars associated
            if has_cars is False:
                return (
                    session.query(User)
                    .outerjoin(Car)
                    .group_by(User.id)
                    .having(func.count(Car.id) == 0)
                    .options(joinedload(User.cars))
                    .all()
                )
            
            # Users with at least min_cars associated
            if min_cars is not None:
                return (
                    session.query(User)
                    .outerjoin(Car)
                    .group_by(User.id)
                    .having(func.count(Car.id) >= min_cars)
                    .options(joinedload(User.cars))
                    .all()
                )
            
    def get_user_by_id(self, user_id):
        with SessionLocal() as session:
            return (
                session.query(User)
                .options(
                    joinedload(User.cars),
                    joinedload(User.addresses)
                )
                .filter(User.id == user_id)
                .first()
            )
    
    def print_user_details(self, User_id):
        user = self.get_user_by_id(User_id)

        if not user:
            print(f"User with ID {User_id} not found.")
            return
        
        print(f"\nUser ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Username: {user.username}")

        print("\nCars:")
        if user.cars:
            for car in user.cars:
                print(f"  Car ID: {car.id}, brand: {car.brand}, Model: {car.model}, Year: {car.manufacture_year}")
        else:
            print("  No cars associated with this user.")

        print("\nAddresses:")
        for address in user.addresses:
            print(f"  Address ID: {address.id}, Street: {address.street}, City: {address.city}, State: {address.state}, Zip Code: {address.zip_code}")

        







    # def get_user_by_id(self, user_id):
    #     with SessionLocal() as session:
    #         return session.get(User, user_id)