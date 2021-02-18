from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from cofi_store.checkout import CheckoutIssuer


class CheckoutMethods(str, Enum):
    SCAN = "scan"
    TOTAL = "total"
    RESTART = "restart"


app = typer.Typer(add_completion=False)


@app.command(help="Checkout purchase CLI.")
def checkout(config_path: Path, debug: Optional[bool] = False):
    methods = [e.value for e in CheckoutMethods]
    issuer = CheckoutIssuer(config_path)
    checkout = issuer.use_checkout()
    code_list = list(issuer.products.keys())
    session = PromptSession(
        completer=WordCompleter(methods + code_list),
        auto_suggest=AutoSuggestFromHistory(),
    )
    while True:
        line = session.prompt()
        words = line.strip().split()
        try:
            command = words[0]
            if command.startswith(tuple(methods)):
                if command == CheckoutMethods.RESTART:
                    checkout = issuer.use_checkout()
                elif command == CheckoutMethods.SCAN:
                    code = words[1]
                    checkout.scan(code)
                else:
                    typer.echo(checkout.total())
            if debug:
                typer.echo(checkout.subtotal)
        except IndexError:
            ...


if __name__ == "__main__":
    app()
