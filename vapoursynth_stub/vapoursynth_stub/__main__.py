if __name__ == "__main__":
    import sys
    from . import install

    if sys.argv[1] == "install":
        install.install()
