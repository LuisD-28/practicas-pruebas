from dbSetup import SessionLocal
from models import Contact

class ContactManager:
    ALLOWED_UPDATE_FIELDS = {'name', 'phone', 'email'}

    def create_contact(self, user_id, name, phone, email):
        with SessionLocal() as session:
            try:
                contact = Contact(
                    user_id=user_id,
                    name=name,
                    phone=phone,
                    email=email
                )
                session.add(contact)
                session.commit()
                session.refresh(contact)
                return contact
            except Exception as e:
                session.rollback()
                print(f"Error creating contact: {e}")
                return None

    def get_contacts_by_user(self, user_id):
        with SessionLocal() as session:
            return (
                session.query(Contact)
                .filter(Contact.user_id == user_id)
                .order_by(Contact.id.asc())
                .all()
            )


    def get_all_contacts(self):
        with SessionLocal() as session:
            return (
                session.query(Contact)
                .order_by(Contact.id.asc())
                .all()
            )


    def get_contact_by_id(self, contact_id):
        with SessionLocal() as session:
            return (
                session.query(Contact)
                .filter(Contact.id == contact_id)
                .first()
            )


    def update_contact(self, contact_id, **kwargs):
        with SessionLocal() as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                return None

            for key, value in kwargs.items():
                if key in self.ALLOWED_UPDATE_FIELDS:
                    setattr(contact, key, value)

            try:
                session.commit()
                session.refresh(contact)
                return contact
            except Exception as e:
                session.rollback()
                print(f"Error updating contact: {e}")
                return None


    def delete_contact(self, contact_id):
        with SessionLocal() as session:
            contact = session.get(Contact, contact_id)
            if not contact:
                return None

            try:
                session.delete(contact)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"Error deleting contact: {e}")
                return None