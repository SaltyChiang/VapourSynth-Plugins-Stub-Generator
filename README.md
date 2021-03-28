# VapourSynth-Plugins-Stub-Generator
An unofficial stub generator for vapoursynth and its plugins, which is helpful to autocomplete code in VSCode.

At first, you need to have a python with vapoursynth installed. Use this python to run the `.py` file and you will get a folder called `vapoursynth` at where you locate the file.

Put the `vapoursynth` folder where your python could find, i.e., at one of `sys.path` item, open your VSCode and enable Python extension and then you should see the autocompletion for vapoursynth functions works.

This works by using python stub file, so your language server should have ability to use `.pyi` files. Pylance in VSCode works perfectly for me, and Jedi works but not so good.
