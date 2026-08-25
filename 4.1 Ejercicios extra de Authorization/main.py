from flask import Flask, Response, jsonify, request
from JWT_Manager import JWT_Manager
import jwt

from managers.contact_manager import ContactManager
from managers.user_manager import UserManager
from managers.refresh_token_manager  import RefreshTokenManager
from managers.login_history_manager import LoginHistoryManager

app = Flask("Address Book API")

u = UserManager()
c = ContactManager()
rt = RefreshTokenManager()
lh = LoginHistoryManager()

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

# Register Endpoint
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json(silent=True) or {}

        if data.get("name") is None or data.get("email") is None or data.get("password_hash") is None:
            return jsonify({"error": "Missing required fields"}), 400

        # User will be created with the default role "USER"
        user = u.create_user(
            data.get("name"),
            data.get("email"),
            data.get("password_hash"),
            "USER"
        )
        if user is None:
            return Response(status=400)

        token = jwt_manager.encode({"user_id": user.id, "role": user.role})
        return jsonify(token=token), 201

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)
    
# Authentication endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    if data.get("email") is None or data.get("password_hash") is None:
        return jsonify({"error": "Missing required fields"}), 400

    ip = request.remote_addr
    user = u.get_user_by_email(data.get("email"))

    if user is None:
        lh.record_login(None, ip, False)
        return Response(status=401)

    if user.password_hash != data.get("password_hash"):
        lh.record_login(user.id, ip, False)
        return Response(status=401)

    token = jwt_manager.encode({"user_id": user.id, "role": user.role})
    refresh = rt.create_refresh_token(user.id)
    if refresh is None:
        return Response(status=500)

    lh.record_login(user.id, ip, True)
    return jsonify(token=token, refresh_token=refresh.token), 200

# Login history endpoint
@app.route('/login-history', methods=['GET'])
def login_history():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error
        if not _is_admin(payload):
            return Response(status=403)

        user_id = request.args.get("user_id", type=int)
        history = lh.get_history_by_user(user_id) if user_id is not None else lh.get_all_history()

        return jsonify([
            {
                "id": h.id,
                "user_id": h.user_id,
                "timestamp": h.timestamp.isoformat(),
                "ip_address": h.ip_address,
                "success": h.success
            }
            for h in history
        ]), 200

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# Refresh token endpoint
@app.route('/refresh-token', methods=['POST'])
def refresh_token():
    try:
        # Get a valid access token(authenticated user)
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error

        # Get the refresh token from the request
        data = request.get_json(silent=True) or {}
        token_str = data.get("refresh_token")
        if token_str is None:
            return jsonify({"error": "Missing refresh token"}), 400

        # Validate the refresh token
        stored = rt.get_valid_token(token_str)
        if stored is None:
            return Response(status=401)

        # Check if the refresh token belongs to the authenticated user
        if stored.user_id != payload.get("user_id"):
            return Response(status=403)

        user = u.get_user_by_id(stored.user_id)
        if user is None:
            return Response(status=401)

        # Revoke the used token
        revoked = rt.revoke_token(token_str)
        if not revoked:
            return Response(status=500)

        # Generate a new tokens for the user
        new_access_token = jwt_manager.encode({"user_id": user.id, "role": user.role})
        new_refresh_token = rt.create_refresh_token(user.id)
        if new_access_token is None or new_refresh_token is None:
            return Response(status=500)

        return jsonify(
            token=new_access_token,
            refresh_token=new_refresh_token.token
        ), 200
    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# Actual user Information Endpoint
@app.route('/me', methods=['GET'])
def me():
    try:
        payload = _get_current_payload()
        if payload is None:
            return Response(status=401)

        user_id = payload.get("user_id")
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



# Create a new contact
@app.route('/contacts', methods=['POST'])
def create_contact():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error

        data = request.get_json(silent=True) or {}
        user_id = payload.get("user_id")
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")

        contact = c.create_contact(user_id, name, phone, email)
        if contact is None:
            return jsonify({"error": "Failed to create contact"}), 400

        return jsonify({"id": contact.id, "name": contact.name, "phone": contact.phone, "email": contact.email}), 201

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)
    

# List contacts, admin can see all, user can see only their own
@app.route('/contacts', methods=['GET'])
def list_contacts():
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error

        if _is_admin(payload):
            contacts = c.get_all_contacts()
        else:
            contacts = c.get_contacts_by_user(payload.get("user_id"))

        contacts_list = [
            {"id": contact.id, "user_id": contact.user_id, "name": contact.name, "phone": contact.phone, "email": contact.email}
            for contact in contacts
        ]
        return jsonify(contacts_list), 200

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


# Get contacts by ID
@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contacts_by_user(contact_id):
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error

        contacts = c.get_contact_by_id(contact_id)
        if contacts is None:
            return jsonify({"error": "Contact not found"}), 404
        if contacts.user_id != payload.get("user_id") and not _is_admin(payload):
            return Response(status=403)

        return jsonify({"id": contacts.id, "user_id": contacts.user_id, "name": contacts.name, "phone": contacts.phone, "email": contacts.email}), 200

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


######## Update contact
@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error

        # Actual Contact
        contact = c.get_contact_by_id(contact_id)
        if contact is None:
            return jsonify({"error": "Contact not found"}), 404

        # Validate user permissions
        if contact.user_id != payload.get("user_id") and not _is_admin(payload):
            return Response(status=403)
        
        # Get updated data from request
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")

        # Update contact with new data
        contact = c.update_contact(
            contact_id,
            name=name,
            phone=phone,
            email=email
        )
        if contact is None:
            return jsonify({"error": "Contact not found"}), 404

        return jsonify({"id": contact.id, "name": contact.name, "phone": contact.phone, "email": contact.email}), 200

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)

# Delete contact
@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        payload, auth_error = _require_auth_payload()
        if auth_error is not None:
            return auth_error

        # Actual Contact
        contact = c.get_contact_by_id(contact_id)
        if contact is None:
            return jsonify({"error": "Contact not found"}), 404

        # Validate user permissions
        if contact.user_id != payload.get("user_id") and not _is_admin(payload):
            return Response(status=403)

        # Delete contact
        success = c.delete_contact(contact_id)
        if not success:
            return jsonify({"error": "Contact not found"}), 404

        return Response(status=204)

    except jwt.InvalidTokenError:
        return Response(status=401)
    except Exception as e:
        print(e)
        return Response(status=500)


if __name__ == '__main__':
    app.run(host="localhost", debug=True)



