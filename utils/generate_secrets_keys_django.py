from jwcrypto import jwk
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_and_save_keys():
    # Create RSA keys (public and private)
    key = jwk.JWK.generate(kty="RSA", size=2048)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Get the private key in PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Save private key in a file
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_key_pem)

    # Get the public key in PEM format
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Save public key in a file
    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_key_pem)

    print("Keys generate and save successfully.")


# Call the function to generate and save the keys
if __name__ == "__main__":
    generate_and_save_keys()
