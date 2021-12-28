from typing import List
from . import convert
from .convert import PluginMeta


def plugins_str(plugins: List[PluginMeta], indent: int = 4) -> str:
    ret_core = []
    ret_video = []
    ret_audio = []
    for plugin in plugins:
        lines_core = []
        lines_video = []
        lines_audio = []
        lines_core.append(f"class {plugin.namespace}(Plugin):")
        lines_core.append(f'    """{plugin.name}"""')
        lines_video.append(f"class {plugin.namespace}(Plugin):")
        lines_video.append(f'    """{plugin.name}"""')
        lines_audio.append(f"class {plugin.namespace}(Plugin):")
        lines_audio.append(f'    """{plugin.name}"""')
        for func in filter(None, plugin.functions_core):
            lines_core.append(r"    @staticmethod")
            lines_core.append(f"    def {func.name}({func.signature})->{func.return_signature}:...")
        for func in filter(None, plugin.functions_video):
            lines_video.append(r"    @staticmethod")
            lines_video.append(f"    def {func.name}({func.signature})->{func.return_signature}:...")
        for func in filter(None, plugin.functions_audio):
            lines_audio.append(r"    @staticmethod")
            lines_audio.append(f"    def {func.name}({func.signature})->{func.return_signature}:...")
        if len(lines_core) > 2:
            ret_core += lines_core
        if len(lines_video) > 2:
            ret_video += lines_video
        if len(lines_audio) > 2:
            ret_audio += lines_audio

    ret_core = [" " * indent + line for line in ret_core]
    ret_video = [" " * indent + line for line in ret_video]
    ret_audio = [" " * indent + line for line in ret_audio]

    return "\n".join(ret_core), "\n".join(ret_video), "\n".join(ret_audio)


def stub() -> str:
    import os
    from vapoursynth import core

    plugins_meta = convert.plugins_vs2py(core.plugins())

    moduledir = os.path.dirname(os.path.realpath(__file__))
    with open(f"{moduledir}/vapoursynth.pyi.in", "r") as f:
        pyi_content = f.read()

    plugins_core, plugins_video, plugins_audio = plugins_str(plugins_meta, 4)
    pyi_content = pyi_content.replace(r"# inject Core plugins", plugins_core)
    pyi_content = pyi_content.replace(r"# inject VideoNode plugins", plugins_video)
    pyi_content = pyi_content.replace(r"# inject AudioNode plugins", plugins_audio)

    return pyi_content
