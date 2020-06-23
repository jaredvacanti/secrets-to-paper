from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    PublicFormat,
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateNumbers,
    RSAPublicNumbers,
    rsa_crt_iqmp,
    rsa_crt_dmp1,
    rsa_crt_dmq1,
)
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateNumbers,
    EllipticCurvePublicNumbers,
    SECP256R1,
    EllipticCurvePublicKey,
    EllipticCurvePrivateKeyWithSerialization,
    derive_private_key,
)


def generate_rsa_key(public_key_path, p, q, n, e):

    with open(public_key_path) as public_key:

        pubkey = serialization.load_pem_public_key(
            public_key.read().encode("ascii"), backend=default_backend()
        )

    q = int(q, 16)
    p = int(p, 16)

    e = pubkey.public_numbers().e
    n = pubkey.public_numbers().n

    # private exponent
    d = int(pow(e, -1, (p - 1) * (q - 1)))

    dmp1 = rsa_crt_dmp1(d, p)
    dmq1 = rsa_crt_dmq1(d, q)
    iqmp = rsa_crt_iqmp(p, q)

    priv_nums = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, pubkey.public_numbers())
    priv_key = priv_nums.private_key(default_backend())

    pem = priv_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption(),
    )

    print(pem.decode("ascii"))

    # pub_nums = RSAPublicNumbers(e, n)
    # priv_nums = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, pub_nums)
    # priv_key = priv_nums.private_key(default_backend())

    # pem = priv_key.private_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PrivateFormat.TraditionalOpenSSL,
    #     encryption_algorithm=serialization.NoEncryption(),
    # )

    # print(pem.decode("ascii"))


def construct_rsa_key(prime1, prime2, mod, exp):

    # a lot of software (including openssl) expects p to be the larger prime
    # instead of expected the user to get it right, just reassign them here
    if prime1 > prime2:
        p = prime1
        q = prime2
    else:
        p = prime2
        q = prime1


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
