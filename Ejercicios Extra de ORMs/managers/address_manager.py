from database import SessionLocal
from models import Address
from sqlalchemy.orm import joinedload

class AddressManager:

    def create_address(self, street, city, state, zip_code, user_id):
        with SessionLocal() as session:
            address = Address(
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                user_id=user_id
            )
            session.add(address)
            session.commit()
            session.refresh(address)
            return address
        
    ALLOWED_UPDATE_FIELDS = {"street", "city", "state", "zip_code", "user_id"}
    def update_address(self, address_id, **kwargs):
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if not address:
                return None
            
            for key, value in kwargs.items():
                if key in self.ALLOWED_UPDATE_FIELDS:
                    setattr(address, key, value)
                else:
                    print(f"Field Address '{key}' is not allowed to be updated.")

            session.commit()
            session.refresh(address)
            return address
        
    def delete_address(self, address_id):
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if not address:
                return False
            
            session.delete(address)
            session.commit()
            return True

    def get_addresses(self, substring=None):
        with SessionLocal() as session:
            query = (
                session.query(Address)
                .options(joinedload(Address.user))
                .order_by(Address.id)
            )

            # If a substring is provided, filter addresses by street containing the substring
            if substring:
                query = query.filter(Address.street.ilike(f"%{substring}%"))

            return query.all()

            