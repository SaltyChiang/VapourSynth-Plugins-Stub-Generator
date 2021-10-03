from typing import Dict, Generator, List, Union


class FunctionMeta(Dict[str, Union[str, None]]):
    pass


class PluginMeta:
    namespace: str
    name: str
    functions_core: FunctionMeta
    functions_video: FunctionMeta
    functions_audio: FunctionMeta

    def __init__(self, namespace: str, name: str, functions: List[FunctionMeta]):
        self.namespace = namespace
        self.name = name
        self.functions_core = functions[0]
        self.functions_video = functions[1]
        self.functions_audio = functions[2]


def function_params_vs2py(params: str) -> List[str]:
    """ Type information from https://github.com/vapoursynth/vapoursynth/blob/master/src/cython/vapoursynth.pyx#L449 """
    params = params.strip(";")
    if params == "":
        return params, None, None
    param_list = params.split(";")

    video = param_list[0].split(":")[1] in ["vnode", "vnode[]"]
    audio = param_list[0].split(":")[1] in ["anode", "anode[]"]

    for param_i in range(len(param_list)):
        name_type_opt = param_list[param_i].split(":")
        if len(name_type_opt) == 1 and name_type_opt[0] == "any":
            pname = "**kwargs"
            ptype = "Any"
        else:
            pname = name_type_opt[0]
            ptype = name_type_opt[1]
            parray = ptype.endswith("[]")
            popt = (len(name_type_opt) >= 3) and (name_type_opt[2] == "opt")

            ptype = ptype[:-2] if parray else ptype
            ptype = ptype.replace("vnode", "VideoNode").replace("vframe", "VideoFrame")
            ptype = ptype.replace("anode", "AudioNode").replace("aframe", "AudioFrame")
            ptype = ptype.replace("func", "Callable").replace("data", "Union[str, bytes, bytearray]")
            ptype = f"Union[{ptype},Sequence[{ptype}]]" if parray else ptype
            # ptype = f"Optional[{ptype}]=..." if popt else ptype
            ptype = f"{ptype}=..." if popt else ptype
        param_list[param_i] = ":".join([pname, ptype])

    if video:
        return ",".join(param_list), ",".join(param_list[1::]).replace("VideoNode", '"VideoNode"'), None
    elif audio:
        return ",".join(param_list), None, ",".join(param_list[1::]).replace("AudioNode", '"AudioNode"')
    else:
        return ",".join(param_list), None, None


def functions_vs2py(functions: FunctionMeta) -> List[FunctionMeta]:
    functions_core = functions.copy()
    functions_video = functions.copy()
    functions_audio = functions.copy()
    for name in functions.keys():
        params = functions[name]
        functions_core[name], functions_video[name], functions_audio[name] = function_params_vs2py(params)
    return functions_core, functions_video, functions_audio


def plugins_vs2py(plugins: Generator) -> List[PluginMeta]:
    plugins_meta = []

    for plugin in plugins:
        functions_dict: Dict[str, str] = {}
        for function in plugin.functions():
            functions_dict[function.name] = function.signature
        plugin_meta = PluginMeta(plugin.namespace, plugin.name, functions_vs2py(functions_dict))
        plugins_meta.append(plugin_meta)

    return plugins_meta
