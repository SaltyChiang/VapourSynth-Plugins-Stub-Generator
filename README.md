# VapourSynth-Plugins-Stub-Generator
An unofficial stub generator for vapoursynth and its plugins, which is helpful to autocomplete code in VSCode.

At first, you need to have a [python](https://www.python.org/) with [vapoursynth](https://www.vapoursynth.com/) installed. You can check it with
```bash
python -c 'from vapoursynth import core
print(core.version())'
```

Then run the command:
```bash
python vs_plugins_helper.py
```

A file called `vapoursynth.pyi` should be created, and move it to where your python could find it (i.e. your python search path), for example:
```bash
mv vapoursynth.pyi /path/to/python/Lib/site-packages/
```

You can check python search path by:
```bash
python -c 'import sys
print(sys.path)'
```

Now open your [VSCode](https://code.visualstudio.com/) and enable [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python), set `python.languageServer` to `Pylance` and then you should see the autocompletion for vapoursynth functions works.

This works by using python stub file, so your language server should have ability to use `.pyi` files. [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) in VSCode works perfectly for me, and I'm wondering how to make Jedi work with it.
