def install(dir: str, filename: str):
    import os
    from . import generate

    pyi_content = generate.stub()

    if dir is not None:
        outdir = os.path.realpath(dir)
        if not os.path.exists(outdir):
            print(f'Unavailable path "{outdir}".')
            return
        elif not os.access(dir, os.W_OK):
            print(f'Access to "{outdir}" is denied.')
            return

    outfile = os.path.join(outdir, filename)
    with open(outfile, "w+") as f:
        f.write(pyi_content)

    print(f"Installed the stub file at {outfile}")
