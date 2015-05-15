import os
from string import Template
curdir = os.path.dirname(__file__)

# reading mainExpression from file
mainExpressionString = ''
mainExpressionFileName = os.path.join(curdir, 'mainExpression.mel')
with open(mainExpressionFileName) as mainExpressionFile:
    mainExpressionString = mainExpressionFile.read()
mainExpressionTemplate = Template(mainExpressionString)

def makeMainExpression(p, cameraScale, focalLength):
    variables = {
            's_p': str(p),
            's_cameraScale': str(cameraScale),
            's_mainCamShapeFocalLength': str(focalLength),
            }
    return mainExpressionTemplate.safe_substitute(variables)


# reading stereoExpression from file
stereoExpressionString = ''
stereoExpressionFileName = os.path.join(curdir, 'stereoExpression.mel')
with open(stereoExpressionFileName) as stereoExpressionFile:
    stereoExpressionString = stereoExpressionFile.read()
stereoExpressionTemplate = Template(stereoExpressionString)

def makeStereoExpression(nCams, p, cameraScale, camIndex, camTranslateX,
        filmOffset):
    variables = {
            's_nCams': str(nCams),
            's_p': str(p),
            's_cameraScale': str(cameraScale),
            's_camIndex': str(camIndex),
            's_camTranslateX': str(camTranslateX),
            's_camShapeHorizontalFilmOffset': str(filmOffset)
            }
    return stereoExpressionTemplate.safe_substitute(variables)
