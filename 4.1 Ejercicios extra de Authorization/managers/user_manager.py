from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from dbSetup import SessionLocal
from models import User

class UserManager:
    ALLOWED_UPDATE_FIELDS = {"name", "email", "password_hash", "role"}

    def Create_user(self, name, email, password_hash, role="USER"):
        with SessionLocal() as session:
            new_user = User(
                name=name,
                email=email,
                password_hash=password_hash,
                role=role
            )
            session.add(new_user)
            try:
                session.commit()
                session.refresh(new_user)
                return new_user
            except IntegrityError:
                session.rollback()
                return None

    def create_user(self, name, email, password_hash, role="USER"):
        return self.Create_user(name, email, password_hash, role)

    def get_users(self):
        with SessionLocal() as session:
            return (
                session.query(User)
                .order_by(User.id.asc())
                .all()
            )

    def get_user_by_id(self, user_id):
        with SessionLocal() as session:
            return (
                session.query(User)
                .filter(User.id == user_id)
                .first()
            )

    def get_user_by_email(self, email):
        with SessionLocal() as session:
            return session.query(User).filter(User.email == email).first()

    def update_user(self, user_id, **kwargs):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                return None

            for key, value in kwargs.items():
                if key in self.ALLOWED_UPDATE_FIELDS:
                    setattr(user, key, value)

            try:
                session.commit()
                session.refresh(user)
                return user
            except IntegrityError:
                session.rollback()
                return None

    def delete_user(self, user_id):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                return None
            session.delete(user)
            session.commit()
            return True