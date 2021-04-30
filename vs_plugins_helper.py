import sys

sys.path.insert(1, "./vapoursynth_stub")


def main():
    from vapoursynth_stub import main
    from vapoursynth_stub import install

    argc = len(sys.argv)
    if argc == 1:
        install.install("./")
    else:
        main.main()


if __name__ == "__main__":
    main()
