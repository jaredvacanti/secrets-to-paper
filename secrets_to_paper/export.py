import subprocess
import base64
import os
import errno


def write_secret_to_disk(secret):
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


def write_chunks_png(chunks, outfile_path):
    """
    Writes the data chunks to png files.
    """

    make_output_dir(outfile_path)
    for i, chunk in enumerate(chunks):
        # Set version to none, and use fit=True when making qrcode so the version,
        # which determines the amount of data the qrcode can store, is selected automatically.
        qrc = qrcode.QRCode(version=None)
        qrc.add_data(chunk)
        qrc.make(fit=True)
        image = qrc.make_image()
        image.save("%s%d.png" % (outfile_path, i + 1), "PNG")
    return len(chunks)


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


def make_output_dir(out_filename):
    """
    Makes the directory to output the file to if it doesn't exist.
    """

    # check if output is to cwd, or is a path
    dirname = os.path.dirname(out_filename)
    if dirname != "" and not os.path.exists(dirname):
        try:
            os.makedirs(os.path.dirname(out_filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


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
