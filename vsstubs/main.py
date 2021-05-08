def main():
    import os
    import sys
    import vapoursynth
    from . import install

    argc = len(sys.argv)
    if argc >= 2:
        if sys.argv[1] == "install":
            if argc >= 3:
                mode = sys.argv[2]
            else:
                mode = "default"
        else:
            mode = "none"
    else:
        mode = "none"

    if mode == "default":
        install.install()
    elif mode == "vapoursynth":
        vsdir = os.path.dirname(os.path.realpath(vapoursynth.__file__))
        install.install(vsdir)
    elif mode == "vscode":
        if sys.platform == "win32":
            extdir = os.path.join(os.getenv("USERPROFILE"), ".vscode", "extensions")
        elif sys.platform == "linux":
            extdir = os.path.join(os.getenv("HOME"), ".vscode", "extensions")
        else:
            print(f'Unsupported platform "{sys.platform}"')
            return
        pyextlist = [dirname for dirname in os.listdir(extdir) if dirname.startswith("ms-python.python")]
        if len(pyextlist) == 0:
            print("No python extension installed.")
            return
        jedidir = os.path.join(extdir, pyextlist[-1], "pythonFiles", "lib", "python", "jedi", "third_party", "typeshed", "third_party", "3")
        jedilspdir = os.path.join(extdir, pyextlist[-1], "pythonFiles", "lib", "jedilsp", "jedi", "third_party", "typeshed", "third_party", "3")
        install.install(jedidir)
        install.install(jedilspdir)
    elif mode == "none":
        pass
    else:
        print(f'Unknown mode "{mode}".')
