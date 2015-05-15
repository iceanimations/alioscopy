''' cammaker.py

Makes a maya cam rig using the rules from alioscopy (C)
'''
import pymel.core as pc
import math

from . import expressions
reload(expressions)

__all__ = ['makeCams']

alioscopy_MIN = 0.05
alioscopy_MAX = 1.0

origImageZ = 400
origNearZ = 6
origFOV = math.radians(13.35)
validNumberOfCameras = [5, 8, 16]
origStereoEyeSeparation = 6.5




# utility functions
def clamp(min, max, value):
    return sorted((min, value, max))[1]

def fovToFocalLength(fov, filmBackWidth=36.0):
    ''' filmBackWidth is in mm '''
    return filmBackWidth / ( 2 * math.tan(fov/2.0) )

def focalLengthToFov(focalLength, filmBackWidth=36.0):
    ''' filmBackWidth is in mm '''
    return 2 * math.atan( filmBackWidth / (2.0 * focalLength) )

def lockAndHide(node, tr=True, ro=True, scale=True):
    node.scaleX.set(l=True)
    node.scaleY.set(l=True)
    node.scaleZ.set(l=True)
    node.scaleX.setKeyable(False)
    node.scaleY.setKeyable(False)
    node.scaleZ.setKeyable(False)


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
]

# main function
def makeCams(nCams=8, alioscopyParameter=1.0, cameraScale=1.0):
    ''' Creates a set of cameras using the alioscopy_parameter'''
    p = clamp(alioscopy_MIN, alioscopy_MAX, alioscopyParameter)
    nCams = nCams if nCams in validNumberOfCameras else validNumberOfCameras[1]

    # effect of scale
    fov = origFOV
    imageZ = origImageZ*cameraScale
    nearZ = origNearZ*cameraScale
    stereoEyeSeparation = origStereoEyeSeparation*cameraScale

    # effect of alioscopyParameter
    fov = 2 * math.atan( math.tan( fov/2.0 ) / p )
    imageZ *= p
    stereoEyeSeparation *= p

    mainCam, mainCamShape = pc.camera()
    mainCam.rename('alioscopyCamRig')

    lockAndHide(mainCam, False, False, True)
    # TODO add mainCam.alioscopyParameter
    # TODO add mainCam.cameraScale parameter and connect
    # TODO show stereo Cams

    for attr in displayAttrs:
        mainCamShape.attr(attr).set(True)

    for attr in lockingAttrs:
        mainCamShape.attr(attr).setLocked(True)

    # TODO lock focal length by expression
    mainCamShape.fl.set(fovToFocalLength(fov))
    mainCamShape.fl.set(l=True)

    for camIndex in range(nCams):
        stereoOffset = stereoEyeSeparation * (camIndex - nCams/2.0 + 0.5)
        shift = -stereoOffset * nearZ / imageZ

        cam, camShape = pc.camera()
        mainCamShape.fl >> camShape.fl
        cam.translateX.set(stereoOffset)
        lockAndHide(cam)
        pc.parent(cam, mainCam, relative=True)
        cam.horizontalFilmOffset.set(shift)
        cam.rename('alioscopyCam%02d' % (camIndex+1))

        for attr in displayAttrs:
            camShape.attr(attr).set(True)

        for attr in lockingAttrs:
            camShape.attr(attr).setLocked(True)

def testFocalLengthToFov():
    assert focalLengthToFov(35) == 0.9500215125301936

def testFovToFocalLength():
    assert fovToFocalLength(0.9500215125301936) == 35
