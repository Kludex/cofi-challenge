<h1 align="center">
    <strong>Cofi Purchase Challenge</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/cofi-challenge" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/cofi-challenge" alt="Latest Commit">
    </a>
    <img src="https://img.shields.io/github/workflow/status/Kludex/cofi-challenge/Test">
    <img src="https://img.shields.io/codecov/c/github/Kludex/cofi-challenge">
    <img src="https://img.shields.io/github/license/Kludex/cofi-challenge">
</p>


## Installation

You must have [Poetry](https://python-poetry.org/) installed. Then, just run:

``` bash
poetry install
```

## Usage

You'll be able to use the `cofi_store` package as you wish, but there's also a CLI available.

``` bash
$ cofi --help
Usage: cofi [OPTIONS] CONFIG_PATH

  Checkout purchase CLI.

Arguments:
  CONFIG_PATH  [required]

Options:
  --debug / --no-debug  [default: False]
  --help                Show this message and exit.
```

Feel free to add the configuration file path and play with it.

P.S.: In case you didn't notice, there's a configuration file in the `resources/rules.json`.

## Decisions

Those decisions were made when developing:

* If `scan()` gets a wrong product, it will just ignore.
* If configuration file has multiple discounts for the same code, only the last one will apply.

## License

This project is licensed under the terms of the MIT license.
