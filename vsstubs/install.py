def install(dir: str = None, filename: str = "vapoursynth.pyi"):
    import os
    from . import generate

    pyi_content = generate.stub()

    if dir is not None:
        if not os.path.exists(dir):
            print(f'Unavailable path "{dir}".')
            return
        outdir = dir
    else:
        outdir = os.path.dirname(os.path.realpath(__file__))
        outdir = os.path.abspath(os.path.join(outdir, os.pardir))

    outfile = os.path.join(outdir, filename)
    with open(outfile, "w+") as f:
        f.write(pyi_content)

    print(f"Installed the stub file at {outfile}")
