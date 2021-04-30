# vapoursynth-stub
An unofficial stub generator for vapoursynth and its plugins, which is helpful to autocomplete code in VSCode.

## Install and generate stub file

At first, you need to have a [python](https://www.python.org/) with [vapoursynth](https://www.vapoursynth.com/) installed. You can check it with
```bash
python -c 'from vapoursynth import core
print(core.version())'
```

It is easy to install or uninstall the package with pip:
```bash
python -m pip install .
python -m pip uninstall vapoursynth-stub
```

You can use the command below to generate the stub file:
```bash
python -m vapoursynth_stub install
```

or use `vsstub` in `Scripts` folder to do the same thing:
```bash
/path/to/python/Scripts/vsstub install
```

A file called `vapoursynth.pyi` should be created in one of you PYTHONPATH.

## Generate stub file for VSCode
There are several installation modes, you can use `vscode` mode to generate stub file for VSCode with Jedi and JediLSP.
```bash
vsstub install vscode
```

The `default` or `vapoursynth` mode shoule work with Pylance or Microsoft Python Language Server.
```bash
vsstub install vapoursynth
```
