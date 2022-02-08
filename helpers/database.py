import importlib
from pathlib import Path


base_path = Path('.').parent.absolute().parent


def autoload_models():
    """
    Auto imports models from modules/ in desired file. Used so that
    flask_migrate does not miss models when migrating

    Returns
    -------
    None
    """
    print("Auto importing models")

    modules_path = Path.joinpath(base_path, 'project/modules')
    for folder in modules_path.iterdir():
        if folder.name.startswith("books") or folder.name.startswith("users"):
            print(folder)
            try:
                to_load = "modules.{}.models".format(folder.name)
                importlib.import_module(to_load)
                print("[x]", "imported", to_load)
            except Exception as e:
                print("[ ]", e)
    pass
