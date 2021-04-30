def install(dir: str = None):
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

    with open(f"{outdir}/vapoursynth.pyi", "w+") as f:
        f.write(pyi_content)
