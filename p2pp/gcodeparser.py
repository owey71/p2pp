__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018-2020, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPLv3'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'

import math

import p2pp.gui as gui
import p2pp.variables as v


def gcode_remove_params(gcode, params):
    removed = False
    result = ''
    rempar = ''
    p = gcode.split(' ')
    for s in p:
        if s == '':
            continue
        if not s[0] in params:
            result += s + ' '
        else:
            rempar = rempar + s + ' '
            removed = True

    result.strip(' ')
    rempar.strip(' ')
    if len(result) < 4:
        return ';--- P2PP Removed [Removed Parameters] - ' + gcode

    if removed:
        return result + ";--- P2PP Removed [Removed Parameters] - " + rempar
    else:
        return result


def get_gcode_parameter(gcode, parameter, default=None):
    fields = gcode.split()
    for parm in fields:
        if parm[0] == parameter:
            return float(parm[1:])
    return default


def split_csv_strings(s):
    newvalues = []
    keyval = s.split("=")
    if len(keyval) > 1:
        keyword = keyval[0]
        value = ("=".join(keyval[1:])).strip(' ')
        values = value.split(";")
        tmp = None
        idx = 0
        while idx < len(values):
            if tmp is None:
                tmp = values[idx]
            else:
                tmp += values[idx]
            if len(tmp) >= 2:
                if tmp[0] == '"' and tmp[-1] == '"':
                    tmp = tmp[1:-1]
                    res = ""
                    tmp = tmp.replace(" ", "_")
                    for i in list(tmp):
                        if i in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-":
                            res = res + i
                    newvalues.append(res)

                    tmp = ""
            idx += 1
    return newvalues


def filament_volume_to_length(x):
    return x / (v.filament_diameter[v.current_tool] / 2 * v.filament_diameter[v.current_tool] / 2 * math.pi)


def parse_slic3r_config():
    for idx in range(len(v.input_gcode) - 1, -1, -1):

        gcode_line = v.input_gcode[idx]

        if gcode_line.startswith("; filament_settings_id"):
            v.filament_ids = split_csv_strings(gcode_line)

        if ("generated by PrusaSlicer") in gcode_line:
            try:
                s1 = gcode_line.split("+")
                s2 = s1[0].split(" ")
                v.ps_version = s2[-1]
                gui.create_logitem("File was created with PS version:{}".format(v.ps_version))
                if v.ps_version < "2.2":
                    gui.log_warning("This version of P2PP is optimized to work with PS2.2!")
            except:
                pass
            continue

        if gcode_line.startswith("; wipe_tower_no_sparse_layers"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                try:
                    v.wipe_remove_sparse_layers = (int(gcode_line[parameter_start + 1:].strip()) == 1)
                except:
                    pass
            continue

        if gcode_line.startswith(";  variable_layer_height = 1"):
            v.variable_layers = True
            continue


        if gcode_line.startswith("; wipe_tower_x"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_posx = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; min_skirt_length"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.skirtsize = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; skirts"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.skirts = float(gcode_line[parameter_start + 1:].strip())
            continue


        if gcode_line.startswith("; wipe_tower_width"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_width = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; wipe_tower_y"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.wipetower_posy = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; extrusion_width"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.extrusion_width = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; infill_speed"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.infill_speed = float(gcode_line[parameter_start + 1:].strip()) * 60
            continue

        if gcode_line.startswith("; layer_height"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.layer_height = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; first_layer_height"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                v.first_layer_height = float(gcode_line[parameter_start + 1:].strip())
            continue

        if gcode_line.startswith("; support_material_synchronize_layers"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                tmp = float(gcode_line[parameter_start + 1:].strip())
                if tmp == 0:
                    v.synced_support = False
                else:
                    v.synced_support = True
            continue

        if gcode_line.startswith("; support_material "):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                tmp = float(gcode_line[parameter_start + 1:].strip())
                if tmp == 0:
                    v.support_material = False
                else:
                    v.support_material = True
            continue

        # TVDE: needs to be expanded to be able to support more than 4 colors
        if gcode_line.startswith("; extruder_colour") or gcode_line.startswith("; filament_colour"):
            filament_colour = ''
            parameter_start = gcode_line.find("=")
            gcode_line = gcode_line[parameter_start + 1:].strip()
            parameter_start = gcode_line.find("#")
            if parameter_start != -1:
                filament_colour = gcode_line.split(";")
            if len(filament_colour) >= 4:
                for i in range(len(filament_colour)):
                    if filament_colour[i] == "":
                        filament_colour[i] = v.filament_color_code[i]
                    else:
                        v.filament_color_code[i] = filament_colour[i][1:]
            continue


        if gcode_line.startswith("; filament_diameter"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                filament_diameters = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(filament_diameters) >= 4:
                    for i in range(4):
                        v.filament_diameter[i] = float(filament_diameters[i])
            continue

        # TVDE: needs to be expanded to be able to support more than 4 colors
        # only check that is needed is that if nore than 4 colors exist, all must be of same type
        if gcode_line.startswith("; filament_type"):
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                filament_string = gcode_line[parameter_start + 1:].strip(" ").split(";")
                v.m4c_numberoffilaments = len(filament_string)
                if v.m4c_numberoffilaments == 4:
                    v.filament_type = filament_string
                    v.used_filament_types = list(set(filament_string))
                elif v.m4c_numberoffilaments >= 4:
                    v.used_filament_types = list(set(filament_string))
                    if len(v.used_filament_types) > 1:
                        gui.log_warning("Prints with more than 4 colors should be of one filament type only!")
                        gui.log_warning("This file will not print correctly")
                    v.filament_type = filament_string[:4]

            if v.m4c_numberoffilaments > 4:
                gui.log_warning(
                    "Number of inputs defined in print: {}.  Swaps may be required!!!".format(v.m4c_numberoffilaments))

            continue

        # TVDE: needs to be expanded to be able to support more than 4 colors
        # if more than 4, just retain the first four (check is done at other level, but for not all settings should be the same)

        if gcode_line.startswith("; retract_lift = "):
            if v.filament_list:
                continue
            lift_error = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                retracts = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(retracts) >= 4:
                    for i in range(4):
                        v.retract_lift[i] = float(retracts[i])
                        if v.retract_lift[i] == 0:
                            lift_error = True
                if lift_error:
                    gui.log_warning(
                        "[Printer Settings]->[Extruders 1 -> {}]->[Retraction]->[Lift Z] should not be set to zero.".format(
                            len(retracts)))
                    gui.log_warning(
                        "Generated file might not print correctly")
            continue

        # TVDE: needs to be expanded to be able to support more than 4 colors
        # if more than 4, just retain the first four (check is done at other level, but for not all settings should be the same)
        if gcode_line.startswith("; retract_length = "):
            retract_error = False
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                retracts = gcode_line[parameter_start + 1:].strip(" ").split(",")
                if len(retracts) >= 4:
                    for i in range(4):
                        v.retract_length[i] = float(retracts[i])
                        if v.retract_length[i] == 0.0:
                            retract_error = True
                if retract_error:
                    gui.log_warning(
                        "[Printer Settings]->[Extruders 1 -> {} 4]->[Retraction Length] should not be set to zero.".format(
                            len(retracts)))
            continue

        if gcode_line.startswith("; gcode_flavor"):
            if "reprap" in gcode_line:
                v.isReprap_Mode = True
            continue

        if "use_firmware_retraction" in gcode_line:
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                gcode_line = gcode_line[parameter_start + 1:].replace(";", "")
                if "1" in gcode_line:
                    v.use_firmware_retraction = True
                else:
                    v.use_firmware_retraction = False
            continue

        if "use_relative_e_distances" in gcode_line:
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                gcode_line = gcode_line[parameter_start + 1:].replace(";", "")
                if "1" in gcode_line:
                    v.gcode_has_relative_e = True
                else:
                    v.gcode_has_relative_e = False
            continue

        # TVDE: needs to be expanded to be able to support more than 4 colors
        # this should be expanded to nxn filaments where n = the number of filaments used.
        # needs to be a perfect square, calculate from there.
        if gcode_line.startswith("; wiping_volumes_matrix"):
            wiping_info = []
            parameter_start = gcode_line.find("=")
            if parameter_start != -1:
                wiping_info = gcode_line[parameter_start + 1:].strip(" ").split(",")
                _warning = True
                for i in range(len(wiping_info)):
                    if int(wiping_info[i]) != 140 and int(wiping_info[i]) != 0:
                        _warning = False

                    wiping_info[i] = filament_volume_to_length(float(wiping_info[i]))
            v.max_wipe = max(wiping_info)
            v.wiping_info = wiping_info
            if _warning:
                gui.log_warning("All purge lenghts 70/70 OR 140.  Purge lenghts may not have been set correctly.")
            continue

