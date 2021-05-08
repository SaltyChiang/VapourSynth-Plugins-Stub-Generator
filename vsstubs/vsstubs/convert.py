from typing import Dict, List, Union


class FunctionMeta(Dict[str, Union[str, None]]):
    pass


class PluginMeta:
    namespace: str
    name: str
    functions_core: FunctionMeta
    functions_video: FunctionMeta

    def __init__(self, namespace: str, name: str, functions: List[FunctionMeta]):
        self.namespace = namespace
        self.name = name
        self.functions_core = functions[0]
        self.functions_video = functions[1]


def function_params_vs2py(params: str) -> List[str]:
    """ Type information from https://github.com/vapoursynth/vapoursynth/blob/master/src/cython/vapoursynth.pyx#L385 """
    params = params.strip(";")
    if params == "":
        return params, None
    param_list = params.split(";")

    video = param_list[0].split(":")[1] in ["clip", "clip[]"]

    for param_i in range(len(param_list)):
        name_type_opt = param_list[param_i].split(":")
        pname = name_type_opt[0]
        ptype = name_type_opt[1]
        parray = ptype.endswith("[]")
        popt = (len(name_type_opt) >= 3) and (name_type_opt[2] == "opt")

        ptype = ptype[:-2] if parray else ptype
        ptype = ptype.replace("clip", "VideoNode").replace("frame", "VideoFrame")
        ptype = ptype.replace("func", "Callable").replace("data", "Union[str, bytes, bytearray]")
        ptype = f"Union[{ptype},Sequence[{ptype}]]" if parray else ptype
        # ptype = f"Optional[{ptype}]=..." if popt else ptype
        ptype = f"{ptype}=..." if popt else ptype
        param_list[param_i] = ":".join([pname, ptype])

    if video:
        return ",".join(param_list), ",".join(param_list[1::]).replace("VideoNode", '"VideoNode"')
    else:
        return ",".join(param_list), None


def functions_vs2py(functions: FunctionMeta) -> List[FunctionMeta]:
    functions_core = functions.copy()
    functions_video = functions.copy()
    for name in functions.keys():
        params = functions[name]
        functions_core[name], functions_video[name] = function_params_vs2py(params)
    return functions_core, functions_video


def plugins_vs2py(plugins: Dict[str, Dict[str, Union[str, Dict[str, str]]]]) -> List[PluginMeta]:
    plugins_meta = []

    for plugin in plugins.values():
        plugin_meta = PluginMeta(plugin["namespace"], plugin["name"], functions_vs2py(plugin["functions"]))
        plugin_meta.functions_video = {key: val for key, val in plugin_meta.functions_video.items() if val is not None}
        plugins_meta.append(plugin_meta)

    return plugins_meta
