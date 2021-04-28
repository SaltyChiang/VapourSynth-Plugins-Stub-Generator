import sys

sys.path.insert(1, "./vapoursynth_stub")


def main():
    from vapoursynth_stub import install

    install.install("./")


if __name__ == "__main__":
    main()
