import jwt
import os

class JWT_Manager:
    def __init__(self, private_key_path, public_key_path, algorithm="RS256"):
        self.algorithm = algorithm

        base_dir = os.path.dirname(os.path.abspath(__file__))

        private_abs = os.path.join(base_dir, private_key_path)
        public_abs = os.path.join(base_dir, public_key_path)

        with open(private_abs, "r", encoding="utf-8") as f:
            self.private_key = f.read()

        with open(public_abs, "r", encoding="utf-8") as f:
            self.public_key = f.read()

    def encode(self, data):
        try:
            encoded = jwt.encode(data, self.private_key, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            print(e)
            return None

    def decode(self, token):
        try:
            decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return decoded
        except Exception as e:
            print(e)
            return None