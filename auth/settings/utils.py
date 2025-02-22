import pathlib

import dotenv

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent


def load_dotenv():
    dotenv.load_dotenv(dotenv.find_dotenv(filename=str(ROOT_DIR / "deploy" / "dev" / ".env.auth.dev")))
