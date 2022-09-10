import os


def main():
    os.system("git pull --ff-only")
    os.system("poetry install")


if __name__ == "__main__":
    main()
