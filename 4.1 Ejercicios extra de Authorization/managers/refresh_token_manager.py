import secrets
from datetime import datetime, timedelta

from dbSetup import SessionLocal
from models import RefreshToken

class RefreshTokenManager:
    def create_refresh_token(self, user_id, days_valid=7):
        with SessionLocal() as session:
            try:
                refresh_token = RefreshToken(
                    user_id=user_id,
                    token=secrets.token_urlsafe(32),
                    expires_at=datetime.utcnow() + timedelta(days=days_valid),
                    revoked=False
                )
                session.add(refresh_token)
                session.commit()
                session.refresh(refresh_token)
                return refresh_token
            except Exception as e:
                session.rollback()
                print(f"Error creating refresh token: {e}")
                return None

    def get_valid_token(self, token_str):
        with SessionLocal() as session:
            token = session.query(RefreshToken).filter(RefreshToken.token == token_str).first()
            if token is None:
                return None
            if token.revoked or token.expires_at < datetime.utcnow():
                return None
            return token

    def revoke_token(self, token_str):
        with SessionLocal() as session:
            token = (
                session.query(RefreshToken)
                .filter(RefreshToken.token == token_str)
                .first()
            )
            if token is None:
                return False

            token.revoked = True

            try:
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"Error revoking token: {e}")
                return False

