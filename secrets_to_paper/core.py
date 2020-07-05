import click
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

# from pretty_bad_protocol import gnupg
from pathlib import Path, PurePath

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from secrets_to_paper.generate.rsa import generate_rsa_key
from secrets_to_paper.generate.ecc import generate_ecc_key
from secrets_to_paper.export import write_secret_to_disk, export_gpg_b64
from secrets_to_paper.parse import pdf_to_secret

# Primary Click Group
@click.group()
@click.option("--debug/--no-debug", default=False)
def stp(debug):
    if debug:
        click.echo("Debug mode is on")


# Generate RSA Subcommand
@stp.command(
    "gen-rsa", short_help="Helper function to generate RSA private key from P and Q.",
)
@click.option("--public-key-path", type=click.Path())
@click.option("--public-key")
@click.option("--p-path")
@click.option("--p", help="The prime p.")
@click.option("--q-path")
@click.option("--q", help="The prime q.")
@click.option(
    "--n",
    help="The private number n.",
    default="BD0C4A0F6C341365CCD24CE66C8FCDD9A896A2FB7655A83E5F1482EA13DDB0DF395C1BED2A9ED2E1C310A7610211BF4ADE0092104F910DE160B444FFAF1F68F8DE89CCFA8DA857108FAA5724738C10D120F78779DC6C53B8D3348A2C6AFD90977B208C72BDC7ACE99B5575CC4EE3D51CBFBE01C780FF8D61404408AB9E053A2D",
)
@click.option(
    "--e", help="The private exponent e. Defaults to 010001.", default="010001"
)
def generate(
    public_key_path=None,
    public_key=None,
    p_path=None,
    p=None,
    q_path=None,
    q=None,
    n=None,
    e=None,
):
    """
    Generate a secret key from public key and secret numbers.
    """
    if p_path is not None and q_path is not None:

        with open(p_path) as f:
            p = f.readline()

        with open(q_path) as f:
            q = f.readline()
        generate_rsa_key(public_key_path, p, q, n, e)

    elif p is not None and q is not None:
        generate_rsa_key(public_key_path, p, q, n, e)

    else:
        p = click.prompt("P")
        q = click.prompt("Q")


# Generate ECC Subcommand
@stp.command(
    "gen-ecc",
    short_help="Helper function to generate ECC private key from A, B, and D.",
)
@click.option("--secret-number", help="The secret number.")
@click.option("--public-number", help="The public number.")
def generate(secret_number=None, public_number=None):
    """
    Generate an ECC secret key from public and secret numbers.
    """
    generate_ecc_key(secret_number, public_number)


# Export GPG Key Subcommand
@stp.command(
    "export-gpg", short_help="Helper function to generate archive of GPG keys.",
)
@click.option(
    "--gpg-dir", type=click.Path(), default=PurePath(Path.home(), ".gnupg"),
)
@click.option("--keygrip", help="The GPG keygrip.")
def export_gpg(keygrip=None, gpg_dir=None):
    """
    Generate a PDF archive document froma  GPG fingerprint ID.
    """

    # gpg = gnupg.GPG(homedir=gpg_dir)
    # c = gpg.Context(armor=False)

    # key = c.get_key(keygrip, secret=True)
    # print(dir(key))

    # with open("output.txt", "wb") as f:
    #     f.write(key)

    # print(str(key))

    # print(gpg.list_keys())
    # secret = gpg.export_keys([keygrip], secret=True, armor=False)
    # write_secret_to_disk(secret, "output.pdf")
    export_gpg_b64(keygrip)


# Export Subcommand
@stp.command(
    "export", short_help="Helper functions for writing secret keys.",
)
@click.option("--private-key-path", type=click.Path())
@click.option("--output-path", type=click.Path())
def export(private_key_path=None, output_path=None):
    """
    Generate a pdf of the secrets.
    """

    with open(private_key_path, "rb") as f:
        pem_data = f.read()

    print(pem_data)

    # pem = load_pem_private_key(pem_data, None, default_backend())
    # print(pem)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(pem_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # img.show()
    write_secret_to_disk(img, output_path)


# Parse Subcommand
@stp.command(
    "parse", short_help="Helper functions to parse secret keys into PEM format.",
)
@click.option("--input-file-path", type=click.Path())
def export(input_file_path=None):
    """
    Generate a secret key from the pdf.
    """

    codes = decode(Image.open(input_file_path))

    for code in codes:
        print(code.data.decode("utf-8"))

