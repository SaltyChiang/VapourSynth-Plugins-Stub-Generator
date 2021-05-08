from typing import List
from . import convert
from .convert import PluginMeta


def plugins_str(plugins: List[PluginMeta], video: bool, indent: int = 4) -> str:
    lines = []
    if not video:
        for plugin in plugins:
            lines.append(f"class {plugin.namespace}(Plugin):")
            lines.append(f'    """{plugin.name}"""')
            for func in plugin.functions_core.keys():
                lines.append(f"    def {func}({plugin.functions_core[func]})->VideoNode:...")
        lines = [" " * indent + line for line in lines]
    else:
        for plugin in plugins:
            if len(plugin.functions_video) != 0:
                lines.append(f"class {plugin.namespace}(Plugin):")
                lines.append(f'    """{plugin.name}"""')
                for func in plugin.functions_video.keys():
                    lines.append(f'    def {func}({plugin.functions_video[func]})->"VideoNode":...')
        lines = [" " * indent + line for line in lines]
    return "\n".join(lines)


def stub() -> str:
    import os
    from vapoursynth import core

    plugins = core.get_plugins()
    plugins_meta = convert.plugins_vs2py(plugins)

    moduledir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{moduledir}/vapoursynth.pyi.in", "r") as f:
        pyi_content = f.read()

    pyi_content = pyi_content.replace(r"# inject Core plugins", plugins_str(plugins_meta, False, 4))
    pyi_content = pyi_content.replace(r"# inject VideoNode plugins", plugins_str(plugins_meta, True, 4))

    return pyi_content
