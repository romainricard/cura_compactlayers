# Cura PostProcessingPlugin
# Author:   Amanda de Castilho
# Date:     August 28, 2018
# Modified: November 16, 2018 by Joshua Pope-Lewis
# Modified: May 25, 2020 by Romain Ricard

# Description:  This plugin shows compact custom messages about your print on the Status bar.

from ..Script import Script
from UM.Application import Application

class CompactLayersCount(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Display compact layer and filename on LCD for Ender 3",
            "key": "Ender3DisplayFilenameAndLayerOnLCD",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "maxlayer":
                {
                    "label": "Display max layer?:",
                    "description": "Display how many layers are in the entire print on status bar?",
                    "type": "bool",
                    "default_value": true
                },
                "prefix":
                {
                    "label": "Remove prefix:",
                    "description": "Files are exported by default with 'CE3PRO_' (or 'CE3_') prefix. If you want to remove this prefix, type it in.",
                    "type": "str",
                    "default_value": "CE3PRO_"
                }
            }
        }"""
    
    def execute(self, data):
        max_layer = 0
        name = Application.getInstance().getPrintInformation().jobName


        prefix = self.getSettingValueByKey("prefix")
        if prefix:
            if name.startswith(prefix):
                name = name[len(prefix):]
        lcd_text = "M117 "

        i = 1
        for layer in data:
            display_text = lcd_text + str(i)
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";LAYER_COUNT:"):
                    max_layer = line
                    max_layer = max_layer.split(":")[1]
                if line.startswith(";LAYER:"):
                    if self.getSettingValueByKey("maxlayer"):
                        display_text = display_text + "/" + max_layer
                    display_text = display_text + " " + name
                    line_index = lines.index(line)
                    lines.insert(line_index + 1, display_text)
                    i += 1
            final_lines = "\n".join(lines)
            data[layer_index] = final_lines
            
        return data
