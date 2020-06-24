from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    PublicFormat,
    Encoding,
    NoEncryption,
    PrivateFormat,
)

from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateNumbers,
    EllipticCurvePublicNumbers,
    SECP256R1,
    EllipticCurvePublicKey,
    EllipticCurvePrivateKeyWithSerialization,
    derive_private_key,
)


def generate_ecc_key(secret_number, public_number):

    secret_int = int(secret_number, 16)

    public_key = EllipticCurvePublicKey.from_encoded_point(
        SECP256R1(), bytes.fromhex(public_number)
    )
    pubkey = public_key.public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    ).decode("ascii")

    print(pubkey)

    derived_key = derive_private_key(secret_int, SECP256R1(), default_backend())
    private_key = derived_key.private_bytes(
        Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()
    ).decode("ascii")

    print(private_key)
