import subprocess
import base64
import os
import io
import errno
import jinja2
import pdfkit

from PIL import Image


def write_secret_to_disk(secret, output_file):

    # imgByteArr = io.BytesIO()
    # secret.save(imgByteArr, format=secret.format)
    # imgByteArr = imgByteArr.getvalue()

    # with open(output_file, "wb") as f:
    #     f.write(imgByteArr)
    #     f.close()

    templateLoader = jinja2.PackageLoader("secrets_to_paper", "templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("secret_output.html")

    options = {"quiet": ""}

    pdfkit.from_string(template.render(data=secret), output_file, options=options)

    return None


def export_gpg_b64(key_id):
    """
    Export a gpg key using the paperkey subcommand
    """

    secret = subprocess.run(["gpg", "--export-secret-key", key_id], capture_output=True)

    paperkey_raw = subprocess.run(
        ["paperkey", "--output-type", "raw"], input=secret.stdout, capture_output=True
    )

    paperkey = subprocess.run(
        ["paperkey", "--output-type", "base16"],
        input=secret.stdout,
        capture_output=True,
    )

    print(secret.stdout)
    print(paperkey_raw.stdout)
    print(paperkey.stdout)
