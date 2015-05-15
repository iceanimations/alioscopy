import os
from string import Template


__all__ = ['makeMainExpression', 'makeStereoExpression']

curdir = os.path.dirname(__file__)

# reading mainExpression from file
mainExpressionString = ''
mainExpressionFileName = os.path.join(curdir, 'mainExpression.mel')
with open(mainExpressionFileName) as mainExpressionFile:
    mainExpressionString = mainExpressionFile.read()
mainExpressionTemplate = Template(mainExpressionString)

def makeMainExpression(p, cameraScale, focalLength, loctz, locsx, locsy):
    variables = {
            's_p': str(p),
            's_cameraScale': str(cameraScale),
            's_mainCamShapeFocalLength': str(focalLength),
            's_loc2TranslateZ': str(loctz),
            's_loc2ScaleZ': str(locsx),
            's_loc2ScaleY': str(locsy),
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
