# vsstubs
An unofficial stub generator for vapoursynth and its plugins, which is helpful to autocomplete code in VSCode.

## Generate and install the stub file

At first, you need to have a [python](https://www.python.org/) with [vapoursynth](https://www.vapoursynth.com/) installed. You can check it with
```bash
python -c 'from vapoursynth import core
print(core.version())'
```

It is easy to install or uninstall the package with pip:
```bash
python -m pip install .
python -m pip uninstall vsstubs
```

You can use the command below to generate the stub file:
```bash
python -m vsstubs install
```

or use `vsstubs` in `Scripts` folder to do the same thing:
```bash
/path/to/python/Scripts/vsstubs install
```

A file called `vapoursynth.pyi` should be created in one of you PYTHONPATH.

## Install the `vapoursynth-stubs` package

```bash
vsstubs install package
```
