''' cammaker.py

Makes a maya cam rig using the rules from alioscopy (C)
'''
import pymel.core as pc
import math


from . import utilities
reload(utilities)
from .utilities import clamp, fovToFocalLength, lockAndHide

from . import expressions
reload(expressions)

__all__ = ['makeCams']


if 'constants':
    alioscopy_MIN = 0.05
    alioscopy_MAX = 1.0

    origImageZ = 400
    origNearZ = 6
    origFOV = math.radians(13.35)
    validNumberOfCameras = [5, 8, 16]
    origStereoEyeSeparation = 6.5

# attribute lists
displayAttrs = [
    'displayFilmGate',
    'displayResolution',
    'displayGateMask',
    'displaySafeAction',
    'displaySafeTitle',
    'displayFilmPivot',
    'displayFilmOrigin',
    'displayCameraFrustum',
    'displayCameraNearClip',
    'displayCameraFarClip',
]

lockingAttrs = [
    'ovr',
    'ffo',
    'o',
    'psc',
    'filmTranslateH',
    'filmTranslateV',
    'horizontalRollPivot',
    'verticalRollPivot',
    'frv',
    'ptsc',
    'horizontalFilmOffset',
    'verticalFilmOffset',
    'cameraScale',
]

# main function
def makeCams(nCams=8, alioscopyParameter=1.0, cameraScale=1.0):
    ''' Creates a set of cameras using the alioscopy_parameter'''
    p = clamp(alioscopy_MIN, alioscopy_MAX, alioscopyParameter)
    nCams = nCams if nCams in validNumberOfCameras else validNumberOfCameras[1]

    # effect of scale
    fov = origFOV
    imageZ = origImageZ*cameraScale
    nearZ = origNearZ
    stereoEyeSeparation = origStereoEyeSeparation*cameraScale

    # effect of alioscopyParameter
    fov = 2 * math.atan( math.tan( fov/2.0 ) / p )
    imageZ *= p
    stereoEyeSeparation *= p

    # adding custom attrs to mainCam
    mainCam, mainCamShape = pc.camera()
    mainCam.rename('alioscopyCamRig')
    mainCam.addAttr('alioscopyParameter', shortName='p',
            niceName='Alioscopy Parameter', defaultValue=1.0, keyable=True,
            hasMinValue=True, minValue=alioscopy_MIN, hasMaxValue=True,
            maxValue=alioscopy_MAX, attributeType='double')
    pAttr=mainCam.attr('alioscopyParameter')
    pAttr.set(p)
    pAttr.set(keyable=True)
    mainCam.addAttr('cameraScale', shortName='cs',
            niceName='Camera Scale', defaultValue=1.0, keyable=True,
            attributeType='double', hasMinValue=True, minValue=0.001,
            hasSoftMaxValue=True, softMaxValue=2)
    scaleAttr = mainCam.attr('cameraScale')
    scaleAttr.set(cameraScale)
    scaleAttr.set(keyable=True)
    mainCam.addAttr('showStereoCams', shortName='ssc',
            niceName='Show Stereo Cams',
            attributeType='bool', defaultValue=True)
    showStereoAttr = mainCam.attr('showStereoCams')
    showStereoAttr.set(keyable=True)
    mainCam.addAttr('showAnnotations', shortName='sha', 
            niceName='Show Annotations', attributeType='bool',
            defaultValue=True)
    annotationsAttr = mainCam.attr('showAnnotations')
    annotationsAttr.set(keyable=True)

    # make annotations
    grp = pc.createNode('transform', n='annotationsGrp', p=mainCam)
    loc1 = pc.spaceLocator()
    loc2 = pc.spaceLocator()
    dimShape = pc.createNode('distanceDimShape')
    dim = dimShape.firstParent()
    loc1.worldPosition[0] >> dim.startPoint
    loc2.worldPosition[0] >> dim.endPoint
    loc1.v.set(False)
    pc.parent(loc1, loc2, dim, grp)
    annotationsAttr >> grp.v

    # focal length expression
    mainCamShape.fl.set(fovToFocalLength(fov))
    mainExpr = expressions.makeMainExpression(pAttr, scaleAttr,
            mainCamShape.fl, loc2.tz, loc2.getShape().localScaleX,
            loc2.getShape().localScaleY)
    pc.expression(s=mainExpr)

    lockAndHide(loc1)
    lockAndHide(loc2)
    lockAndHide(dim)
    lockAndHide(grp)
    lockAndHide(mainCam, False, False, True)
    for attr in displayAttrs:
        mainCamShape.attr(attr).set(True)
    for attr in lockingAttrs:
        mainCamShape.attr(attr).setLocked(True)

    for camIndex in range(nCams):
        stereoOffset = stereoEyeSeparation * (camIndex - nCams/2.0 + 0.5)
        shift = -stereoOffset * nearZ / imageZ

        cam, camShape = pc.camera()
        mainCamShape.fl >> camShape.fl
        showStereoAttr >> cam.v
        cam.translateX.set(stereoOffset)
        pc.parent(cam, mainCam, relative=True)
        cam.horizontalFilmOffset.set(shift)
        cam.rename('alioscopyCam%02d' % (camIndex+1))

        stereoExpr = expressions.makeStereoExpression(nCams, pAttr, scaleAttr,
                camIndex, cam.tx, camShape.horizontalFilmOffset)
        pc.expression(s=stereoExpr)

        lockAndHide(cam)
        for attr in displayAttrs:
            camShape.attr(attr).set(True)
        for attr in lockingAttrs:
            camShape.attr(attr).setLocked(True)

    pc.select(mainCam)
    return mainCam

if __name__ == '__main__':
    makeCams
