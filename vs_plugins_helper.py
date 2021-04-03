import os
import sys
import re
from vapoursynth import core

plugins = core.get_plugins()

vs_path = "."
init_in_path = "vs_plugins_helper.in"

if len(sys.argv) > 1 and sys.argv[1] is not None:
    vs_path = sys.argv[1]
    if not os.path.exists(vs_path):
        print("Path \"%s\" invalid." % (vs_path))
        sys.exit()

vs_path = "%s/vapoursynth" % (vs_path)
if os.path.exists(vs_path):
    print(
        "There exists a folder called \"vapoursynth\" in the path, do you want to cover it? (y/N)"
    )
    cover = input().lower()
    if cover != "y" and cover != "yes":
        print("Stop generating.")
        sys.exit()
else:
    os.mkdir(vs_path)


def convert2pyi(params: str):
    if params == "":
        return params, None
    list_type_regex = re.compile(r"^(?P<type>\S+)\[\]$")
    param_list = params.split(";")
    vn = False
    if param_list[0].split(":")[1] in ["clip", "clip[]"]:
        vn = True
    for param_i in range(len(param_list)):
        param_name_type = param_list[param_i].split(":")
        list_type_match = list_type_regex.match(param_name_type[1])
        if list_type_match is not None:
            list_type = list_type_match.groupdict()["type"]
            param_name_type[1] = "list[%s]" % (list_type)
        param_list[param_i] = ":".join(param_name_type[0:2])
    if vn:
        return ",".join(param_list), ",".join(param_list[1::])
    else:
        return ",".join(param_list), None


for plugin_identifier in plugins:
    plugin_dict = plugins[plugin_identifier]
    plugin_namespace = plugin_dict["namespace"]
    plugin_file = open("%s/%s.pyi" % (vs_path, plugin_namespace), "w+")
    plugin_vn_file = open("%s/%s_vn.pyi" % (vs_path, plugin_namespace), "w+")
    plugin_file_head = (
        "from . import VideoNode as clip\nfunc = function\ndata = str\n\n"
    )
    plugin_file.write(plugin_file_head)
    plugin_vn_file.write(plugin_file_head)

    functions = plugin_dict["functions"]
    for function_name in functions:
        function_params, function_vn_params = convert2pyi(
            functions[function_name].strip(" ;")
        )
        function_str = "def %s(%s) -> clip: ...\n" % (function_name, function_params)
        plugin_file.write(function_str)
        if function_vn_params is not None:
            function_vn_str = "def %s(%s) -> clip: ...\n" % (
                function_name,
                function_vn_params,
            )
            plugin_vn_file.write(function_vn_str)
    plugin_file.close()
    plugin_vn_file.close()

init_in_file = open("%s" % (init_in_path), "r")
init_file = open("%s/__init__.pyi" % (vs_path), "w+")
init_lines = init_in_file.readlines()
init_in_file.close()

init_lines.append("\n")
init_lines.append("class Core(_Core):\n")
for plugin_identifier in plugins:
    plugin_dict = plugins[plugin_identifier]
    plugin_namespace = plugin_dict["namespace"]
    init_lines.append("    from . import %s\n" % (plugin_namespace))

init_lines.append("\n")
init_lines.append("class VideoNode(_VideoNode):\n")
for plugin_identifier in plugins:
    plugin_dict = plugins[plugin_identifier]
    plugin_namespace = plugin_dict["namespace"]
    init_lines.append(
        "    from . import %s_vn as %s\n" % (plugin_namespace, plugin_namespace)
    )

init_file.writelines(init_lines)
