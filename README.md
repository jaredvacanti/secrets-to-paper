# secrets-to-paper

![Publish to PyPI](https://github.com/jaredvacanti/secrets-to-paper/workflows/Publish%20to%20PyPI/badge.svg)

A command-line tool to convert secret keys to printable PDFs and to parse those
PDFs back to usable secret keys.

Note: Python 3.8+ is required to use this package. Python 3.8 introduced
a new computation for
[modular inverses](https://docs.python.org/3/library/functions.html#pow).

> Changed in version 3.8: For int operands, the three-argument form of pow now
> allows the second argument to be negative, permitting computation of modular
> inverses.

## Dependencies

[Paperkey](http://www.jabberwocky.com/software/paperkey/) is a command line tool
to export GnuPG keys on paper. It reduces the size of the exported key, by
removing the public key parts from the private key. Paperkey also includes
CRC-24 checksums in the key to allow the user to check whether their private key
has been restored correctly.

- paperkey (for GPG keys)
- zbar/libzbar0

#### Ubuntu/Linux


```
sudo apt-get install zbar paperkey
```

#### MacOS X

```
brew install zbar paperkey
```

### Usage

```
Usage: stp [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  export      Helper functions for writing secret keys.
  export-gpg  Helper function to generate archive of GPG keys.
  gen-ecc     Helper function to generate ECC private key from A, B, and D.
  gen-rsa     Helper function to generate RSA private key from P and Q.
  parse       Helper functions to parse secret keys into PEM format.
```


## Development

#### Initializing a virtual environment:

```
# requires >= python3.8
pyenv shell 3.8.3

# init & activate virtualenvironment
python -m venv .venv
source .venv/bin/activate

# install poetry in venv, and use to install local package
pip install --upgrade pip
pip install poetry
poetry install
```

This makes an executable `stp` available in your `$PATH` after poetry
installations. During development, it's often more convenient to run

```
poetry run stp ...
```

instead of re-installing before invocations.

## Testing

You can generate a private and public key for testing purposes using `openssl`.

```
poetry run tox
```
