import sys


def main():
    sys.path.insert(1, "./vsstubs/")
    from vsstubs.install import install as vsstubs_install
    from vsstubs.main import main as vsstubs_main

    argc = len(sys.argv)
    if argc == 1:
        vsstubs_install("./")
    else:
        vsstubs_main()


if __name__ == "__main__":
    main()
