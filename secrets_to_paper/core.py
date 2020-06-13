import click
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateNumbers,
    RSAPublicNumbers,
    rsa_crt_iqmp,
    rsa_crt_dmp1,
    rsa_crt_dmq1,
)


@click.command(
    "gen-key", short_help="Helper function to generate private key from P and Q.",
)
@click.argument("public-key-path", type=click.Path())
@click.option(
    "--p", help="The prime p.",
)
@click.option(
    "--q", help="The prime q.",
)
@click.option(
    "--n",
    help="The private number n.",
    default="BD0C4A0F6C341365CCD24CE66C8FCDD9A896A2FB7655A83E5F1482EA13DDB0DF395C1BED2A9ED2E1C310A7610211BF4ADE0092104F910DE160B444FFAF1F68F8DE89CCFA8DA857108FAA5724738C10D120F78779DC6C53B8D3348A2C6AFD90977B208C72BDC7ACE99B5575CC4EE3D51CBFBE01C780FF8D61404408AB9E053A2D",
)
@click.option(
    "--e", help="The private exponent e. Defaults to 010001.", default="010001"
)
def generate_key(public_key_path, p, q, n, e):
    """
    Generate a pdf of the secrets.
    """

    q = int(q, 16)
    p = int(p, 16)
    n = int(n, 16)
    e = int(e, 16)

    with open(public_key_path) as public_key:

        pubkey = serialization.load_pem_public_key(
            public_key.read().encode("ascii"), backend=default_backend()
        )

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
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
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


@click.command(
    "secrets-to-paper",
    short_help="Helper functions for encrypting/decrypting keys to paper and back.",
)
@click.argument("private-key-path", type=click.Path())
def secrets_to_paper(private_key_path):
    """
    Generate a pdf of the secrets.
    """

    with open(private_key_path) as private_key:

        priv_key = serialization.load_pem_private_key(
            private_key.read().encode("ascii"), backend=default_backend(), password=None
        )

    print(
        priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("ascii")
    )


def construct_rsa_key(prime1, prime2, mod, exp):

    # a lot of software (including openssl) expects p to be the larger prime
    # instead of expected the user to get it right, just reassign them here
    if prime1 > prime2:
        p = prime1
        q = prime2
    else:
        p = prime2
        q = prime1
