from datetime import datetime, timedelta

from dbSetup import SessionLocal
from models import LoginHistory, RefreshToken

class LoginHistoryManager:
    def record_login(self, user_id, ip_address, success):
        with SessionLocal() as session:
            try:
                login_history = LoginHistory(
                    user_id=user_id,
                    ip_address=ip_address,
                    success=success
                )
                session.add(login_history)
                session.commit()
                session.refresh(login_history)
                return login_history
            except Exception as e:
                session.rollback()
                print(f"Error recording login history: {e}")
                return None


    def get_history_by_user(self, user_id):
        with SessionLocal() as session:
            try:
                history = session.query(LoginHistory).filter(LoginHistory.user_id == user_id).all()
                return history
            except Exception as e:
                print(f"Error retrieving login history: {e}")
                return None


    def get_all_history(self):
        with SessionLocal() as session:
            try:
                history = session.query(LoginHistory).all()
                return history
            except Exception as e:
                print(f"Error retrieving all login history: {e}")
                return None
