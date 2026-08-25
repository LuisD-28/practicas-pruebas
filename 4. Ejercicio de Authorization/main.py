from flask import Flask, Response, jsonify, request
from JWT_Manager import JWT_Manager
import jwt

from managers.product_manager import ProductManager
from managers.invoice_manager import InvoiceManager
from managers.user_manager import UserManager

app = Flask("user-service")

u = UserManager()
p = ProductManager()
i = InvoiceManager()

# RS256: private key to sign the token, public key to verify the token
jwt_manager = JWT_Manager("keys/private.pem", "keys/public.pem", "RS256")

# Read the token from the Authorization header and return it without the "Bearer " prefix
def _get_token_from_header():
    auth = request.headers.get('Authorization')
    if auth is None:
        return None
    return auth.replace("Bearer ", "")

# Read the token from the Authorization header, decode it, and return the payload
def _get_current_payload():
    token = _get_token_from_header()
    if token is None:
        return None
    return jwt_manager.decode(token)

# Check if the user is an admin based on the payload
def _is_admin(payload):
    return payload and payload.get("role") == "ADMIN"

def _require_auth_payload():
    payload = _get_current_payload()
    if payload is None:
        return None, Response(status=401)
    return payload, None

####################
# ENDPOINTS
####################
@app.route('/Test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    if data.get('name') is None or data.get('email') is None or data.get('password_hash') is None:
        return Response(status=400)

    # User will be created with the role "USER" by default
    user = u.Create_user(
        data.get('name'),
        data.get('email'),
        data.get('password_hash'),
        "USER",
    )
    if user is None:
        return Response(status=400)

    token = jwt_manager.encode({"id": user.id, "role": user.role})
    return jsonify(token=token), 200

# Authentication Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    if data.get('email') is None or data.get('password_hash') is None:
        return Response(status=400)

    user = u.get_user_by_email(data.get('email'))
    if user is None:
        return Response(status=401)

    # ??????????
    if user.password_hash != data.get('password_hash'):
        return Response(status=401)

    token = jwt_manager.encode({"id": user.id, "role": user.role})
    return jsonify(token=token), 200


@app.route('/me', methods=['GET'])
def me():
    try:
        payload = _get_current_payload()
        if payload is None:
            return Response(status=401)

        user_id = payload.get("id")
        user = u.get_user_by_id(user_id)
        if user is None:
            return Response(status=401)

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }), 200

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# User Management Endpoints
# Create a new user
# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json(silent=True) or {}

#     required_fields = ['name', 'email', 'password_hash']
#     missing_fields = [field for field in required_fields if field not in data]

#     if missing_fields:
#         return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
#     user = u.Create_user(
#         name=data.get('name'),
#         email=data.get('email'),
#         password_hash=data.get('password_hash'),
#         role=data.get('role', "USER")
#     )               
#     if user:
#         return jsonify({
#             "message": f"User {user.name} created successfully",
#             "user": {
#                 "id": user.id,
#                 "name": user.name,
#                 "email": user.email,
#                 "role": user.role
#             }
#         }), 201
#     else:
#         return jsonify({"error": "Failed to create user"}), 400

# Get all users
@app.route('/users', methods=['GET'])
def list_users():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
            return Response(status=403)

        users = u.get_users()
        return jsonify([
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
            for user in users
        ]), 200

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
            return Response(status=403)
        
        data = request.get_json(silent=True) or {}
        product = p.create_product(
            name=data.get('name'),
            price=data.get('price'),
            entry_date=data.get('entry_date'),
            quantity=data.get('quantity')
        )
        if product:
            return jsonify({
                "message": f"{product.quantity} - {product.name}'s were added successfully",
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "entry_date": product.entry_date,
                    "quantity": product.quantity
                }
            }), 201
        else:
            return jsonify({"error": "Failed to create product"}), 400

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# Get all products
@app.route('/products', methods=['GET'])
def list_products():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
            return Response(status=403)
        
        products = p.get_products()
        return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "entry_date": product.entry_date,
            "quantity": product.quantity
        }
        for product in products
    ]), 200
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)

    
# update a product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
                return Response(status=403)
        data = request.get_json(silent=True) or {}
        product = p.update_product(product_id, **data)
        if product:
            return jsonify({
                "message": f"Product {product.name} updated successfully",
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "entry_date": product.entry_date,
                    "quantity": product.quantity
                }
            }), 200
        else:
            return jsonify({"error": f"Failed to update product with ID {product_id}"}), 400
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)

# Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
            return Response(status=403)
        
        deleted = p.delete_product(product_id)
        if deleted:
            return jsonify({"message": f"Product with ID {product_id} deleted successfully"}), 200
        else:
            return jsonify({"error": f"Failed to delete product with ID {product_id}"}), 400
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)

    
# Purchase Endpoint
@app.route('/purchase', methods=['POST'])
def purchase():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        
        data = request.get_json(silent=True) or {}
        invoice = i.create_invoice(
            user_id=payload.get('id'),
            items=data.get('items', [])
)
        
        if invoice:
            return jsonify({
                "message": f"Invoice created successfully",
                "invoice": {
                    "id": invoice.id,
                    "user_id": invoice.user_id,
                    "total": invoice.total,
                    "created_at": invoice.created_at
                }
            }), 201
        else:
            return jsonify({"error": "Failed to create invoice"}), 400
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)

# Get my invoices
@app.route('/invoices/me', methods=['GET'])
def list_my_invoices():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
            
        invoices = i.get_invoices_by_user_id(payload.get('id'))
        return jsonify([
        {
            "id": invoice.id,
            "user_id": invoice.user_id,
            "total": invoice.total,
            "created_at": invoice.created_at
        }   
        for invoice in invoices
    ]), 200
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# Get all invoices (admin only)
@app.route('/invoices', methods=['GET'])
def list_all_invoices():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
            return Response(status=403)
        
        invoices = i.get_invoices()
        return jsonify([
        {
            "id": invoice.id,
            "user_id": invoice.user_id,
            "total": invoice.total,
            "created_at": invoice.created_at
        }   
        for invoice in invoices
    ]), 200
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)

    

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

