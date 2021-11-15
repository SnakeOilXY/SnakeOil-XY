

def countObjects():
    printList = list()
    objectTypeTable = {}
    # build up dictionary of different classes and keep a count
    for obj in FreeCAD.ActiveDocument.Objects:
        if objectTypeTable.has_key(obj.TypeId):
            objectTypeTable[obj.TypeId] = objectTypeTable[obj.TypeId]+1
        else:
            objectTypeTable[obj.TypeId] = 1
        wb = obj.TypeId[0:obj.TypeId.find("::")]
        shape = obj.TypeId[obj.TypeId.find("::")+2:]
        # print wb + "---" + shape
        placementString = ""
        if obj.TypeId == "Sketcher::SketchObject":
            printList.append(formatPrintLine("Sketch", "", str(obj.Label)))
            if showSketcherSegmentsFlag:
                for i in obj.Geometry:
                    printList.append(formatPrintLine("", " -segment", str(i)))
        elif wb == "Part":
            if showPlacementFlag:
                placementString = str(obj.Placement)
            if shape in ("Cylinder", "Cut", "Box", "Fuse", "Loft", "Feature", "FeaturePython", "Part2DObjectPython"):
                printList.append(formatPrintLine(
                    wb, shape, str(obj.Label), str(obj.Name)))
            else:  # print shapes not in list above
                printList.append(formatPrintLine(
                    str(obj.TypeId), "", str(obj.Label), str(obj.Name)))
        elif wb == "PartDesign":
            if showPlacementFlag:
                placementString = str(obj.Placement)
            if shape in ("Pad", "Feature", "Fillet", "Part2DObjectPython"):
                printList.append(formatPrintLine(
                    wb, shape, str(obj.Label), str(obj.Name)))
            else:  # print shapes not in list above
                printList.append(formatPrintLine(
                    str(obj.TypeId), "", str(obj.Label), str(obj.Name)))
        elif obj.TypeId == "App::DocumentObjectGroup":
            printList.append(formatPrintLine("Group", "", str(obj.Label)))
        elif obj.TypeId == "Image::ImagePlane":
            printList.append(formatPrintLine(
                wb, shape, str(obj.Label), str(obj.Name)))
        else:  # print workbench shapes not in lists above
            printList.append(formatPrintLine(
                str(obj.TypeId), str(obj.Label), str(obj.Name)))
        if showPlacementFlag and len(placementString) != 0:
            printList.append(formatPrintLineMax(
                "", " -placement", placementString))

    printList.append("")
    printList.append(summarySeparator)
    from collections import OrderedDict
    sortedByTags = OrderedDict(
        sorted(objectTypeTable.items(), key=lambda x: x[1], reverse=True))
    for k, v in sortedByTags.items():
        printList.append(formatPrintLineSum(k, v))
    printList.append("")
    objectClassCount = 0
    objectTotalCount = 0
    for i in objectTypeTable:
        objectTotalCount = objectTotalCount + objectTypeTable[i]
    objectCLassCount = len(objectTypeTable)
    printList.append(formatPrintLineSum(
        "Object Class Total is ", str(objectCLassCount)))
    printList.append(formatPrintLineSum(
        "Object Total is ", str(objectTotalCount)))
    printList.append(summarySeparator)
    return printList


def formatPrintLineSum(a, b):
    return printLineFormatter(2, a, str(b), "", "")


def formatPrintLineMax(a, b, c):
    return printLineFormatter(1, a, b, "", "")


def formatPrintLine(a, b, c, *args):
    d = ""
    if len(args) == 1:
        d = args[0]
    return printLineFormatter(0, a, b, c, d)


def printLineFormatter(flag, a, b, c, d):
    # flag = 0	standard print, spread values over 4 columns
    # flag = 1	printing verbose things like Sketch details or Placements, combine columns 3 & 4
    # flag = 2	printing the summary lines, combine columns 1 & 2
    suffix = ""
    if csvFlag:
        pfs2 = printFormatString2csv
        pfs3 = printFormatString3csv
        pfs4 = printFormatString4csv
    else:
        pfs2 = printFormatString2
        pfs3 = printFormatString3
        pfs4 = printFormatString4
    if flag == 0:
        aa = a[:f1]
        bb = b[:f2]
        cc = c[:f3]
        dd = d[:f4]
        return pfs4.format(aa, bb, cc, dd)
    elif flag == 1:
        aa = a[:f1]
        bb = b[:f2]
        cc = c[:f3+f4]
        dd = d[:f4]
        return pfs3.format(aa, bb, cc)
    else:
        aa = a[:f1+f2]
        bb = b[:f3+f4]
        return pfs2.format(aa, bb)


# Constant definitions
# set some field widths
screenWidth = QtGui.QDesktopWidget().screenGeometry().width()
global f1, f2, f3, f4
# f1 = 15; f2 = 25; f3 = 45; f4 = 25 # 110 columns in 1000 pixels
f1 = 15*screenWidth/1000
f2 = 25*screenWidth/1000
f3 = 45*screenWidth/1000
f4 = 25*screenWidth/1000
# and some print format strings
global printFormatString2, printFormatString3, printFormatString4
global printFormatString2csv, printFormatString3csv, printFormatString4csv
printFormatString2 = "{0:<"+str(f1+f2)+"} {1:<"+str(f3)+"}"
printFormatString2csv = "{0}, {1}"
printFormatString3 = "{0:<"+str(f1)+"} {1:<"+str(f2)+"} {2:<"+str(f3+f4)+"}"
printFormatString3csv = "{0}, {1}, {2}"
printFormatString4 = "{0:<"+str(f1)+"} {1:<" + \
    str(f2)+"} {2:<"+str(f3)+"} {3:<"+str(f4)+"}"
printFormatString4csv = "{0}, {1}, {2}, {3}"
# some button labels that are checked in the code
global choice1, choice2, choice3, csvFlag
choice1 = "Report View"
choice2 = "CSV File"
choice3 = "Window"
csvFlag = False
summarySeparator = "======================================================="
summarySeparatorCsv = "-------------------------------------------------------"
# code ***********************************************************************************
if FreeCAD.ActiveDocument != None:
    # ask if to window or to Report View...
    form = configureMacro()
    form.exec_()
    showSketcherSegmentsFlag = False
    if form.cbss.isChecked():
        showSketcherSegmentsFlag = True
    showPlacementFlag = False
    if form.cbp.isChecked():
        showPlacementFlag = True
    if form.result == choice2:
        csvFlag = True
        showSketcherSegmentsFlag = False
        showPlacementFlag = False
        summarySeparator = summarySeparatorCsv
    printList = countObjects()
    if form.result == choice1:  # report to Report View
        mainWindow = FreeCADGui.getMainWindow()
        dockWidgets = mainWindow.findChildren(QtGui.QDockWidget)
        reportViewFlag = False
        for dw in dockWidgets:
            if dw.objectName() == "Report view":
                reportViewFlag = True
        if reportViewFlag:
            print printFormatString4.format(	"", "", "(User Supplied)", "")
            print printFormatString4.format(	"Type", "Shape", "Label", "Name")
            print ""
            for line in printList:
                print line + "\n"
        else:
            QtGui.QMessageBox.information(
                None, "", "Please use 'Menu->View->Views->Report view' to open the 'Report view'")
    if form.result == choice2:  # report to CSV file
        filePath = QtGui.QFileDialog.getSaveFileName(
            parent=None, caption="Save CSV file as", dir=expanduser("~"), filter="*.csv")
        file = open(filePath[0], "w")
        for line in printList:
            file.write(line + "\n")
        file.close()
    if form.result == choice3:  # report to window
        # ----------------------------------------------------------------------
        longPrintLine = ""
        for line in printList:
            longPrintLine = longPrintLine + line + "\n"
        form = DisplayText(longPrintLine)
