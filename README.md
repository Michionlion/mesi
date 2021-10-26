# Mesi

[![Lint and Test](https://github.com/Michionlion/mesi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Michionlion/mesi/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Michionlion/mesi/branch/main/graph/badge.svg?token=RdzwvXDrxp)](https://codecov.io/gh/Michionlion/mesi)
[![PyPI](https://img.shields.io/pypi/v/mesi)](https://pypi.org/project/mesi)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mesi)](https://pypi.org/project/mesi/#files)
[![License](https://img.shields.io/github/license/Michionlion/mesi.svg)](https://github.com/Michionlion/mesi/blob/master/LICENSE)

---

Mesi is a tool to measure the similarity in a many-to-many fashion of long-form
documents like Python source code or technical writing. The output can be useful
in determining which of a collection of files are the most similar to each
other.

## Installation

Python 3.9+ and [pipx](https://pypa.github.io/pipx/) are recommended, although
Python 3.6+ and/or [pip](https://pip.pypa.io/en/stable/) will also work.

```bash
pipx install mesi
```

If you'd like to test out Mesi before installing it, use the remote execution
feature of `pipx`, which will temporarily download Mesi and run it in an
isolated virtual environment.

```bash
pipx run mesi --help
```

## Usage

For a directory structure that looks like:

```text
projects
├── project-one
│   ├── pyproject.toml
│   ├── deliverables
│   │   └── python_program.py
│   └── README.md
├── project-two
│   ├── pyproject.toml
│   ├── deliverables
│   │   └── python_program.py
│   └── README.md
│
```

where similarity should be measured between each project's
`deliverables/python_program.py` file, run the command:

```bash
mesi projects/*/deliverables/python_program.py
```

A lower distance in the produced table equates to a higher degree of similarity.

See the help menu (`mesi --help`) for additional options and configuration.

### Algorithms

There are many algorithms to choose from when comparing string similarity! Mesi
implements all the
[algorithms](https://github.com/life4/textdistance#algorithms) provided by
[TextDistance](https://github.com/life4/textdistance). In general `levenshtein`
is never a bad choice, which is why it is the default.

### Table Formats

Mesi uses [tabulate](https://github.com/astanin/python-tabulate) for table
formatting. The table format can be configured with the `--table-format` option
to one of the formats
[listed](https://github.com/astanin/python-tabulate#table-format) in tabulate's
documentation.

### Dependencies

Mesi uses two primary dependencies for text similarity calculation:
[polyleven](https://github.com/fujimotos/polyleven), and
[TextDistance](https://github.com/life4/textdistance). Polyleven is the default,
as its singular implementation of [Levenshtein
distance](https://en.wikipedia.org/wiki/Levenshtein_distance) can be faster in
most situations. However, if a different edit distance algorithm is requested,
TextDistance's implementations will be used.

## Bugs/Requests

Please use the [GitHub issue
tracker](https://github.com/Michionlion/mesi/issues) to submit bugs or request
new features, options, or algorithms.

## License

Distributed under the terms of the [GPL v3](LICENSE) license, mesi is free and
open source software.
