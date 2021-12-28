from typing import Iterator, List
import vapoursynth


class Injectable:
    cnode = vapoursynth.core
    vnode = vapoursynth.core.std.BlankClip()
    anode = vapoursynth.core.std.BlankAudio()

    def core(plugin: str, function: str):
        return function in dir(getattr(Injectable.cnode, plugin))

    def video(plugin: str, function: str):
        return function in dir(getattr(Injectable.vnode, plugin))

    def audio(plugin: str, function: str):
        return function in dir(getattr(Injectable.anode, plugin))


class FunctionMeta:
    plugin: str
    name: str
    signature: str
    return_signature: str

    def __init__(self, plugin, name, signature, return_signature) -> None:
        self.plugin = plugin
        self.name = name
        self.signature = signature
        self.return_signature = return_signature

    def set_signatures(self, signature: str, return_signature: str):
        return FunctionMeta(self.plugin, self.name, signature, return_signature)


class PluginMeta:
    namespace: str
    name: str
    functions_core: List[FunctionMeta]
    functions_video: List[FunctionMeta]
    functions_audio: List[FunctionMeta]

    def __init__(self, namespace: str, name: str, functions: List[List[FunctionMeta]]):
        self.namespace = namespace
        self.name = name
        self.functions_core = functions[0]
        self.functions_video = functions[1]
        self.functions_audio = functions[2]


def signature_vs2py(signature: str) -> List[str]:
    """Type information from https://github.com/vapoursynth/vapoursynth/blob/master/src/cython/vapoursynth.pyx#L449"""
    arg_list = signature.strip(";").split(";")

    for i, arg in enumerate(arg_list):
        name_type_opt = arg.split(":")
        if len(name_type_opt) == 1 and name_type_opt[0] == "":
            continue
        elif len(name_type_opt) == 1 and name_type_opt[0] == "any":
            name = "**kwargs"
            type = "Any"
        else:
            name = name_type_opt[0]
            type = name_type_opt[1]
            array = type.endswith("[]")
            type = type[:-2] if array else type
            opt = (len(name_type_opt) >= 3) and (name_type_opt[2] == "opt")

            type = type.replace("vnode", "VideoNode").replace("vframe", "VideoFrame")
            type = type.replace("anode", "AudioNode").replace("aframe", "AudioFrame")
            type = type.replace("func", "Callable")
            type = type.replace("data", "Union[str, bytes, bytearray]")
            type = f"Union[{type},Sequence[{type}]]" if array else type
            # type = f"Optional[{ptype}]=..." if popt else ptype
            type = f"{type}=..." if opt else type

        arg_list[i] = ":".join([name, type])

    return arg_list


def function_vs2py(function: FunctionMeta) -> List[FunctionMeta]:
    plugin = function.plugin
    name = function.name
    signature = function.signature
    return_signature = function.return_signature
    core = Injectable.core(plugin, name)
    video = Injectable.video(plugin, name)
    audio = Injectable.audio(plugin, name)

    input_list = signature_vs2py(signature)
    output_list = signature_vs2py(return_signature)

    for i, output in enumerate(output_list):
        if output == "":
            output_list[i] = "None"
        else:
            output_list[i] = output.split(":")[-1]
    if len(output_list) == 1 and output_list[0] == "None":
        return_signature = "None"
    elif len(output_list) == 1:
        return_signature = output_list[0]
    else:
        return_signature = ",".join(output_list)
        return_signature = f"Union[{return_signature}]"

    return (
        None if not core else function.set_signatures(",".join(input_list), return_signature),
        None if not video else function.set_signatures(",".join(input_list[1::]), return_signature),
        None if not audio else function.set_signatures(",".join(input_list[1::]), return_signature),
    )


def functions_vs2py(functions: List[FunctionMeta]) -> List[List[FunctionMeta]]:
    functions_core = functions.copy()
    functions_video = functions.copy()
    functions_audio = functions.copy()
    for i, function in enumerate(functions):
        functions_core[i], functions_video[i], functions_audio[i] = function_vs2py(function)
    return functions_core, functions_video, functions_audio


def plugins_vs2py(plugins: Iterator) -> List[PluginMeta]:
    plugins_meta = []

    for plugin in plugins:
        functions_meta: List[FunctionMeta] = []
        for function in plugin.functions():
            functions_meta.append(
                FunctionMeta(
                    plugin.namespace,
                    function.name,
                    function.signature,
                    function.return_signature,
                )
            )
        plugins_meta.append(PluginMeta(plugin.namespace, plugin.name, functions_vs2py(functions_meta)))

    return plugins_meta
