''' Based on script by frankbags@https://gist.github.com/frankbags/c85d37d9faff7bce67b6d18ec4e716ff '''
import re  # To perform the search and replace.
from ..Script import Script


class KlipperPostProcessing(Script):

    def getSettingDataString(self):
        return """{
            "name": "Klipper Post Processing",
            "key": "KlipperPostProcessing",
            "metadata": {},
            "version": 2,
            "settings":{}
        }"""

    def execute(self, data):

        minMaxXY = {'MINX': 0, 'MINY': 0, 'MAXX': 0, 'MAXY': 0}
        startGcodeLineData = ''

        totalLayerCount = ''
        currentLayer = ''
        gcodeTotalPrintTime = ''
        gcodeRemainPrintTime = ''
        gcodePercentProgress = ''

        for layerNumber, layerData in enumerate(data):

            # search for print area boundary
            for k, v in minMaxXY.items():
                result = re.search(str(k)+":(\d*\.?\d*)", layerData)
                if result is not None:
                    minMaxXY[k] = result.group(1)
            # search for set print area macro
            areaStartGcode = re.search(
                ".*%(MINX|MAXX|MINY|MAXY)%.*", layerData)
            # replace print area template
            if areaStartGcode is not None:
                if not startGcodeLineData:
                    startGcodeLineData = layerData
                for k, v in minMaxXY.items():
                    pattern3 = re.compile('%' + k + '%')
                    startGcodeLineData = re.sub(
                        pattern3, v, startGcodeLineData)
                data[layerNumber] = startGcodeLineData

            # get total layer count
            if not totalLayerCount:
                result = re.search(r";LAYER_COUNT:(\d*)", layerData)
                if result is not None:
                    totalLayerCount = result.group(1)
            # get current layer count
            if totalLayerCount:
                result = re.search(r";LAYER:(\d*)", layerData)
                if result is not None:
                    currentLayer = result.group(1)

            # get total print time
            if not gcodeTotalPrintTime:
                result = re.search(r";TIME:(\d*)", layerData)
                if result is not None:
                    gcodeTotalPrintTime = float(result.group(1))
            # get current print time and calc progress percent
            if gcodeTotalPrintTime:
                result = re.search(r";TIME_ELAPSED:(\d*\.?\d*)", layerData)
                if result is not None:
                    timeElapsed = float(result.group(1))
                    gcodePercentProgress = int(
                        timeElapsed / gcodeTotalPrintTime * 100)
                    gcodeRemainPrintTime = str(int((gcodeTotalPrintTime - timeElapsed)/3600)) + ":" + str(
                        int((gcodeTotalPrintTime - timeElapsed) // 60 % 60))

            # insert progress code
            if currentLayer and gcodeRemainPrintTime and gcodePercentProgress:
                data[layerNumber] = "DISPLAY_GCODE_PROGRESS TOTAL_LAYER=" + str(totalLayerCount) + " CURRENT_LAYER=" + str(
                    currentLayer) + " PROGRESS=" + str(gcodePercentProgress) + " REMAIN=" + str(gcodeRemainPrintTime) + "\n" + layerData

        return data


# start g-code format
# START_PRINT EXTRUDER_TEMP={material_print_temperature_layer_0} BED_TEMP={material_bed_temperature_layer_0} AREA_START=%MINX%,%MINY% AREA_END=%MAXX%,%MAXY%

# layer progress format
# SET_GCODE_PROGRESS TOTAL_LAYER=37 CURRENT_LAYER=0 PROGRESS=4 REMAIN=0:5
