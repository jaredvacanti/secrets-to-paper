import click
from secrets_to_paper.export import write_secret_to_disk
from secrets_to_paper.parse import pdf_to_secret
from secrets_to_paper.generate import generate_key
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + "Option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '"
                        + str(self.name)
                        + "' is mutually exclusive with "
                        + str(mutex_opt)
                        + "."
                    )
                else:
                    self.prompt = None
        return super(Mutex, self).handle_parse_result(ctx, opts, args)


# Primary Click Group
@click.group()
@click.option("--debug/--no-debug", default=False)
def stp(debug):
    click.echo("Debug mode is %s" % ("on" if debug else "off"))


# Generate Subcommand
@stp.command(
    "generate", short_help="Helper function to generate private key from P and Q.",
)
@click.option(
    "--public-key-path", type=click.Path(), cls=Mutex, not_required_if=["public-key"]
)
@click.option("--public-key", cls=Mutex, not_required_if=["public-key-path"])
@click.option("--p-path", cls=Mutex, not_required_if=["p"])
@click.option("--p", cls=Mutex, not_required_if=["p-path"], help="The prime p.")
@click.option("--q-path", cls=Mutex, not_required_if=["q"])
@click.option("--q", cls=Mutex, not_required_if=["q-path"], help="The prime q.")
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
        generate_key(public_key_path, p, q, n, e)

    else:
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
