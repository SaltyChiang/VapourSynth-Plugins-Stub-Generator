# vapoursynth-stub
An unofficial stub generator for vapoursynth and its plugins, which is helpful to autocomplete code in VSCode.

## Install and generate stub file

At first, you need to have a [python](https://www.python.org/) with [vapoursynth](https://www.vapoursynth.com/) installed. You can check it with
```bash
python -c 'from vapoursynth import core
print(core.version())'
```

Then run the command:
```bash
python -m pip install .
python -m vapoursynth_stub install
```

Or use `update-vsstub` in `Scripts` folder to update stub:
```bash
/path/to/python/Scripts/update-vsstub
```

A file called `vapoursynth.pyi` should be created in one of you PYTHONPATH.

You can check python search path by:
```bash
python -c 'import sys
print(sys.path)'
```

## Known limit

This works by using python stub file, so your language server should have ability to use `.pyi` files. Pylance in VSCode works perfectly for me, and I'm wondering how to make Jedi work with it.
