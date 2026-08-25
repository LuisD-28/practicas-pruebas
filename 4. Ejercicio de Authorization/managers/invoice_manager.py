from decimal import Decimal
from sqlalchemy.orm import joinedload
from dbSetup import SessionLocal
from models import Invoice, InvoiceItem, Product

class InvoiceManager:
    def create_invoice(self, user_id, items):
        with SessionLocal() as session:
            try:
                if not user_id or not isinstance(items, list) or len(items) == 0:
                    return None

                total = Decimal("0.00")
                invoice = Invoice(user_id=user_id, total=total)
                session.add(invoice)
                session.flush()

                for item_data in items:
                    product_id = item_data.get("product_id")
                    quantity = item_data.get("quantity")

                    if product_id is None or quantity is None:
                        session.rollback()
                        return None

                    quantity = int(quantity)
                    if quantity <= 0:
                        session.rollback()
                        return None

                    product = session.get(Product, product_id)
                    if not product or product.quantity < quantity:
                        session.rollback()
                        return None

                    unit_price = Decimal(product.price)
                    subtotal = unit_price * Decimal(quantity)
                    total += subtotal
                    product.quantity -= quantity

                    invoice_item = InvoiceItem(
                        invoice_id=invoice.id,
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )
                    session.add(invoice_item)

                invoice.total = total
                session.commit()
                session.refresh(invoice)
                return invoice
            except Exception:
                session.rollback()
                return None

    def get_invoices(self):
        with SessionLocal() as session:
            return (
                session.query(Invoice)
                .options(joinedload(Invoice.user), joinedload(Invoice.items))
                .order_by(Invoice.id.asc())
                .all()
            )

    def get_invoices_by_user_id(self, user_id):
        with SessionLocal() as session:
            return (
                session.query(Invoice)
                .options(joinedload(Invoice.user), joinedload(Invoice.items))
                .filter(Invoice.user_id == user_id)
                .order_by(Invoice.id.asc())
                .all()
            )