# VapourSynth-Plugins-Stub-Generator
An unofficial stub generator for vapoursynth and its plugins, which is helpful to autocomplete code in VSCode.

## Generating stub file

At first, you need to have a [python](https://www.python.org/) with [vapoursynth](https://www.vapoursynth.com/) installed. You can check it with
```bash
python -c 'from vapoursynth import core
print(core.version())'
```

Then run the command:
```bash
python vs_plugins_helper.py
```

A file called `vapoursynth.pyi` should be created. Move it to where your language server or library like Jedi can recognize.

## Generating stub file for VSCode

For VSCode users, there are some simpler way to generate the stub file.

For Pylance or Microsoft Python Language Server users, run the command to install the stub file:
```bash
python vs_plugins_helper.py install beside
```

For Jedi or JediLSP users, run the command to install the stub file:
```bash
python vs_plugins_helper.py install vscode
```

## Setting up VSCode

Files in `.vscode` folder might be helpful to set up VSCode.

1. Install [VSCode](https://code.visualstudio.com/), then install [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) in VSCode extension market.

2. Paste the settings.json to the *user settings folder*<sup>1</sup> or *work area settings folder*<sup>2</sup>. This will enable the python code highlighting and autocompletion.

3. Paste the tasks.json to the *user settings folder*<sup>1</sup> or *work area settings folder*<sup>2</sup>, and paste the keybindings.json to your vscode *user settings folder*<sup>1</sup>. This will enable shift+f5/f6 hotkeys as f5/f6 in vsedit.

4. **Remember to change `"path\\to\\your\\VapourSynth\\python.exe"` in settings.json and tasks.json to your own python interpreter.**

<sup>1</sup>: Usually refer to `%APPDATA%\Code\User\` on Windows and `$HOME/.config/Code/User/` on Linux

<sup>2</sup>: Usually refer to `/path/to/your/workdir/.vscode/`

