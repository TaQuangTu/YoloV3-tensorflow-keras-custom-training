import os

NAMES_TO_LABELS = {'person': 0, 'people': 1, 'cyclist': 2, 'person?': 3}

def getAllFiles(directory):
    fileList = []
    for path in os.listdir(directory):
        absolutePath = os.path.join(directory, path)
        if os.path.isfile(absolutePath):
            fileList.append(absolutePath)
        else:
            subFileList = getAllFiles(directory + "/" + path)
            fileList += subFileList
    return fileList

def getFileLines(filePath):
    lines = []
    file = open(filePath, "r")
    return file.readlines()

def createNewAnnotationFiles():
    annoDir = '/content/sample_data/dataset/annotations'
    imageDir = '/content/sample_data/dataset/images'
    newAnnofile = open('4_CLASS_test.txt', 'w+')
    fileList = getAllFiles(annoDir)
    for filePath in fileList:
        if filePath.__contains__("set06"):
            continue
        if filePath.__contains__("set07"):
            continue
        if filePath.__contains__("set08"):
            continue
        if filePath.__contains__("set05"):
            continue
        if filePath.__contains__("set09"):
            continue
        if filePath.__contains__("set10"):
            continue
        if filePath.__contains__("set11"):
            continue
        lines = getFileLines(filePath)[1:]  # exclude the first row
        bboxes = []
        for line in lines:
            items = line.split(sep=' ', maxsplit=20)
            className = items[0]
            classLabel = NAMES_TO_LABELS[className]
            xMin = int(items[1])
            yMin = int(items[2])
            width = int(items[3])
            height = int(items[4])
            xMax = xMin + width
            yMax = yMin + height
            bbox = str(xMin) + "," + str(yMin) + "," + str(xMax) + "," + str(yMax) + "," + str(classLabel)
            bboxes.append(bbox)
        bboxesStr = ""
        for bbox in bboxes:
            bboxesStr += bbox + " "
       # newRowLowLight = imageDir + filePath[len(annoDir):-10] +"lwir/"+filePath[-10:-3] + "jpg " + bboxesStr + "\n"
        newRowVisible = imageDir + filePath[len(annoDir):-10] +"visible/"+filePath[-10:-3] + "jpg " + bboxesStr + "\n"
       # newAnnofile.write(newRowLowLight)
        newAnnofile.write(newRowVisible)

if __name__ == "__main__":
    createNewAnnotationFiles()
