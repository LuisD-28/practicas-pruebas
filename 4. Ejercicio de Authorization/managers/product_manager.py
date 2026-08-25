from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from dbSetup import SessionLocal
from models import Product

class ProductManager:
    ALLOWED_UPDATE_FIELDS = {'name', 'price', 'entry_date', 'quantity'}

    def create_product(self, name, price, entry_date, quantity):
        with SessionLocal() as session:
            try:
                product = Product(
                    name=name,
                    price=Decimal(price),
                    entry_date=datetime.strptime(entry_date, "%Y-%m-%d").date(),
                    quantity=quantity
                )
                session.add(product)
                session.commit()
                session.refresh(product)
                return product
            except Exception as e:
                session.rollback()
                print(f"Error creating product: {e}")
                return None

    def get_products(self):
        with SessionLocal() as session:
            return (
                session.query(Product)
                .options(joinedload(Product.items))
                .order_by(Product.id.asc())
                .all()
            )

    def get_product_by_id(self, product_id):
        with SessionLocal() as session:
            return (
                session.query(Product)
                .options(joinedload(Product.items))
                .filter(Product.id == product_id)
                .first()
            )

    def update_product(self, product_id, **kwargs):
        with SessionLocal() as session:
            product = session.get(Product, product_id)
            if not product:
                return None

            for key, value in kwargs.items():
                if key in self.ALLOWED_UPDATE_FIELDS:
                    if key == 'price':
                        setattr(product, key, Decimal(value))
                    elif key == 'entry_date':
                        setattr(product, key, datetime.strptime(value, "%Y-%m-%d").date())
                    else:
                        setattr(product, key, value)

            try:
                session.commit()
                session.refresh(product)
                return product
            except Exception as e:
                session.rollback()
                print(f"Error updating product: {e}")
                return None

    def delete_product(self, product_id):
        with SessionLocal() as session:
            product = session.get(Product, product_id)
            if not product:
                return None

            try:
                session.delete(product)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                print(f"Error deleting product: {e}")
                return None

    