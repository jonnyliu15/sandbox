import sys


class Config:
    MODE: str = "DEV"

    def __init__(self):
        pass

    def configure(self, configs: list[str]):
        self.MODE = configs[configs.index("--mode") + 1]


config = Config


def run(argv: list[str]):
    print("Starting Database with ")


if __name__ == "__main__":
    run(sys.argv)
