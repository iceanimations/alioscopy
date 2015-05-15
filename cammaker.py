''' cammaker.py

Makes a maya cam rig using the rules from alioscopy (C)
'''
import pymel.core as pc
import math


import utilities
reload(utilities)

from utilities import clamp, fovToFocalLength, lockAndHide

from . import expressions
reload(expressions)

__all__ = ['makeCams']


# constants
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

if __name__ == '__main__':
    makeCams
