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


def params2pyi(params: str) -> List[str]:
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
        ptype = f"Optional[{ptype}]" if popt else ptype
        param_list[param_i] = ":".join([pname, ptype])

    if video:
        return ",".join(param_list), ",".join(param_list[1::]).replace("VideoNode", '"VideoNode"')
    else:
        return ",".join(param_list), None


def functions2pyi(functions: FunctionMeta) -> List[FunctionMeta]:
    functions_core = functions.copy()
    functions_video = functions.copy()
    for name in functions.keys():
        params = functions[name]
        functions_core[name], functions_video[name] = params2pyi(params)
    return functions_core, functions_video


def plugins2str(plugins: List[PluginMeta], video: bool, indent: int = 4) -> str:
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


def generate_pyi(out_file: str, in_file: str):
    from vapoursynth import core

    plugins = core.get_plugins()
    plugins_meta = []

    for plugin in plugins.values():
        plugin_meta = PluginMeta(plugin["namespace"], plugin["name"], functions2pyi(plugin["functions"]))
        plugin_meta.functions_video = {key: val for key, val in plugin_meta.functions_video.items() if val is not None}
        plugins_meta.append(plugin_meta)

    with open(f"{in_file}", "r") as f:
        pyi_content = f.read()

    pyi_content = pyi_content.replace(r"# inject Core plugins", plugins2str(plugins_meta, False, 4))
    pyi_content = pyi_content.replace(r"# inject VideoNode plugins", plugins2str(plugins_meta, True, 4))

    with open(f"{out_file}", "w+") as f:
        f.write(pyi_content)


def main():
    import os
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-path", type=str, default=".", help=r"Set output folder path.")
    args = parser.parse_args()

    in_path = "vs_plugins_helper.in"
    out_path = args.output_path

    if not os.path.exists(out_path):
        print(f'Path "{out_path}" invalid.')
        sys.exit()

    out_path = f"{out_path}/vapoursynth.pyi"

    if os.path.exists(out_path):
        print('There exists "vapoursynth.pyi" in the path, do you want to cover it? (y/N)')
        cover = input().lower()
        if cover != "y" and cover != "yes":
            print("Stop generating.")
            sys.exit()

    generate_pyi(out_path, in_path)


if __name__ == "__main__":
    main()
