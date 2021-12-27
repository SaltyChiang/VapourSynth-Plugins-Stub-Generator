def main():
    import os
    import sys
    import sysconfig
    import site

    try:
        import vapoursynth
    except ImportError as e:
        print("It seems you have not installed VapourSynth yet.")
        exit(e)
    from .install import install

    def print_help():
        print(
            """
Useage: python3 -m vsstubs [operation] [mode]

operation could be "help", "install" or "update".
If not specified, "update" will be selected.

- "help"    will show this help message.

- "install" has three modes: "default", "byside" and "here".
            "mode" option could be empty and then "default"
            will be selected.

  - "default"   will install the stub file as a package called
                "vapoursynth-stub", which could be used by many
                language servers.
  - "byside"    will install the stub file where your vapoursynth
                is installed.
  - "here"      will generate the stub file at where you run the
                command, which should only be used for testing.

- "update"  will find your installed stub file and make that up to date.
            """
        )

    argc = len(sys.argv)
    if argc == 1:
        mode = "update"
    elif argc >= 2:
        if sys.argv[1] == "install":
            if argc >= 3:
                mode = sys.argv[2]
            else:
                mode = "default"
        elif sys.argv[1] == "update":
            mode = "update"
        elif sys.argv[1] == "help":
            mode = "help"
        else:
            print(f'Unknown operation "{sys.argv[1]}"')
            mode = "help"
    else:
        mode = "help"

    if site.ENABLE_USER_SITE:
        pkgdir = site.USER_SITE
    else:
        pkgdir = sysconfig.get_path("purelib")
    stubsdir = os.path.join(pkgdir, "vapoursynth-stubs")

    vsdir = os.path.dirname(os.path.realpath(vapoursynth.__file__))

    workdir = os.getcwd()

    filedir = os.path.dirname(os.path.realpath(__file__))
    filedir = os.path.abspath(os.path.join(filedir, os.pardir))

    if mode == "update":
        if os.path.exists(os.path.join(stubsdir, "__init__.pyi")):
            mode = "default"
        elif os.path.exists(os.path.join(vsdir, "vapoursynth.pyi")):
            mode = "byside"
        elif os.path.exists(os.path.join(workdir, "vapoursynth.pyi")):
            mode = "test"
        else:
            print("It seems you have not installed the stub file yet.")
            mode = "help"

    if mode == "default":
        if not os.path.exists(stubsdir):
            os.makedirs(stubsdir)
        install(stubsdir, "__init__.pyi")
    elif mode == "byside":
        install(vsdir, "vapoursynth.pyi")
    elif mode == "test":
        install(workdir, "vapoursynth.pyi")
    elif mode == "help":
        print_help()
    else:
        print(f'Unknown mode "{mode}".')
        print_help()
