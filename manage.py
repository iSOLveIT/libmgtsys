from pathlib import Path
import subprocess
import click

from run import app
from helpers.database import autoload_models


base_path = Path('.').parent.absolute().parent


@click.command()
@click.argument("args", nargs=-1)
def process(args):
    if args[0] == "rundebug":
        app.run(port=4000)
    elif args[0] == "db":
        try:
            autoload_models()
            if args[1] == "migrate":
                subprocess.run(["flask", "db", "migrate"])
            elif args[1] == "upgrade":
                subprocess.run(["flask", "db", "upgrade"])
            elif args[1] == "init":
                subprocess.run(["flask", "db", "init"])
        except IndexError as e:
            print("db requires more options")
            raise e
    else:
        print("Command not recognised")

    # This will be printed on exit
    print("See you soon!!!")


if __name__ == "__main__":
    process()
