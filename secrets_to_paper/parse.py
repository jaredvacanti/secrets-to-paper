import subprocess
import base64


def pdf_to_secret(pdf_file):
    return None


def import_from_b64(pubkey_path, private_bytes):
    """
    Imports the private GPG key to the gpg key ring.
    """

    paperkey = subprocess.Popen(
        args=["paperkey", "--pubring", pubkey_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    (paperkey_stdout, _) = paperkey.communicate(private_bytes)
    gpg = subprocess.Popen(
        args=["gpg", "--import"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return gpg.communicate(paperkey_stdout)


def read_chunks_png(in_filenames):
    """
    Reads base64 encoded private key data from many PNG QR codes.
    """

    base64str = b""
    for in_filename in in_filenames:
        chunk = subprocess.check_output(["zbarimg", "--raw", in_filename])
        base64str += chunk
    return base64str


def read_chunks_b64(in_filenames):
    """
    Reads base64 encoded private key data from many files.
    """

    base64str = b""
    for in_filename in in_filenames:
        with open(in_filename, "rb") as in_file:
            chunk = in_file.read()
            base64str += chunk
    return base64str
