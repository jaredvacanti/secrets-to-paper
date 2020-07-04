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


def export_as_b64(key_id, num_files):
    """
    The export command. With it you can export your gpg secret key to a base64 encoded string
    across n chunks.
    """

    secret = subprocess.Popen(
        ["gpg", "--export-secret-key", key_id], stdout=subprocess.PIPE
    )
    paperkey = subprocess.check_output(
        ["paperkey", "--output-type", "raw"], stdin=secret.stdout
    )
    base64str = base64.b64encode(paperkey)
    chunks = chunk_up(base64str, num_files)
    return chunks


def write_chunks_b64(chunks, outfile_path):
    """
    Writes the data chunks to text files as base64 encoded strings.
    """

    out_filename = outfile_path.split(".")
    outfile_ext = "txt"
    if len(out_filename) > 1:
        (out_filename, outfile_ext) = out_filename
    else:
        out_filename = out_filename[0]

    make_output_dir(out_filename)
    for i, chunk in enumerate(chunks):
        with open("%s%d.%s" % (out_filename, i + 1, outfile_ext), "wb") as txt_file:
            txt_file.write(chunk)
    return len(chunks)


def chunk_up(base64str, num_chunks):
    """
    Breaks a base64 encoded string into n equal size parts
    (the final chunk might be smaller than the others).
    """

    chunk_size = int(len(base64str) / num_chunks)
    chunks = []
    for i in range(num_chunks - 1):
        low = i * chunk_size
        upper = (i + 1) * chunk_size
        chunks.append(base64str[low:upper])
    chunks.append(base64str[(num_chunks - 1) * chunk_size :])
    return chunks
