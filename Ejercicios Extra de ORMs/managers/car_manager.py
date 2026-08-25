from database import SessionLocal
from models import Car, User
from sqlalchemy.orm import joinedload

class CarManager:

    def create_car(self, brand, model, manufacture_year, user_id=None):
        with SessionLocal() as session:
            car = Car(
                brand=brand,
                model=model,
                manufacture_year=manufacture_year,
                user_id=user_id
            )
            session.add(car)
            session.commit()
            session.refresh(car)
            return car
    
    ALLOWED_UPDATE_FIELDS = {"brand", "model", "manufacture_year", "user_id"}
    def update_car(self, car_id, **kwargs):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if not car:
                return None
            
            for key, value in kwargs.items():
                if key in self.ALLOWED_UPDATE_FIELDS:
                    setattr(car, key, value)
                else:
                    print(f"Field Car '{key}' is not allowed to be updated.")

            session.commit()
            session.refresh(car)
            return car
    
    def assign_car_to_user(self, car_id, user_id):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            user = session.get(User, user_id)
            if not car or not user:
                return None

            car.user_id = user_id
            session.commit()
            session.refresh(car)
            return car
    
    def delete_car(self, car_id):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if not car:
                return None

            session.delete(car)
            session.commit()
            return car
        
    def get_cars(self, owner=None):
        with SessionLocal() as session:

            # Get all cars if no owner filter is provided
            if owner is None:
                return (
                    session.query(Car)
                    .options(joinedload(Car.user))
                    .order_by(Car.id)
                    .all()
                )
            
            # Get cars that are assigned to users if owner is True
            if owner is True:
                return (
                    session.query(Car)
                    .filter(Car.user_id.isnot(None))
                    .options(joinedload(Car.user))
                    .order_by(Car.id)
                    .all()
                )
            
            # Get cars that are not assigned to users if owner is False
            if owner is False:
                return (
                    session.query(Car)
                    .filter(Car.user_id.is_(None))
                    .options(joinedload(Car.user))
                    .order_by(Car.id)
                    .all()
                )