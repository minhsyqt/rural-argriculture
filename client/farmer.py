from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Farmer:
    def __init__(self, farmerID, geolocation):
        self.farmerID = farmerID
        self.geolocation = geolocation

        # Signup related
        self.private_key = None
        self.public_key = None
        self.cloudlab_token = None
        self.already_signup = False

    #================= Actions that farmers can do =================

    # The first action should always be sign up, onetime event
    # 1) generate RSA private, public key
    # 2) send public key to cloudlab through API
    # 3) receive token from cloudlab
    def signup(self):
        if not already_signup:
            # Generate an RSA key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # Serialize the private and public keys to PEM format
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Store the keys
            self.private_key = private_pem
            self.public_key = public_pem

    # Login: recuring first step everytime farmer connect to server
    # 1) pass token to cloudlab for verification
    # 2) send request for updates like weather, alarm
    def login(self):
        pass