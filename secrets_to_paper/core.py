import click
import secrets_to_paper.export as export
import secrets_to_paper.parse as parse
from secrets_to_paper.generate import generate_key
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image


# Primary Click Group
@click.group()
@click.option("--debug/--no-debug", default=False)
def stp(debug):
    click.echo("Debug mode is %s" % ("on" if debug else "off"))


# Generate Subcommand
@stp.command(
    "generate", short_help="Helper function to generate private key from P and Q.",
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
def generate(public_key_path, p, q, n, e):
    """
    Generate a secret key from public key and secret numbers.
    """

    generate_key(public_key_path, p, q, n, e)


# Export Subcommand
@stp.command(
    "export", short_help="Helper functions for writing secret keys.",
)
@click.argument("private-key-path", type=click.Path())
def export(private_key_path):
    """
    Generate a pdf of the secrets.
    """

    img = qrcode.make("Some data here")
    print(img)
    # decode(Image.open("pyzbar/tests/code128.png"))
