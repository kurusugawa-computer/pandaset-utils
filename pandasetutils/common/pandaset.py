from enum import Enum


class CameraType(Enum):
    """
    カメラの種類。値はディレクトリ名に合わせています。
    """

    FRONT_CAMERA = "front_camera"
    BACK_CAMERA = "back_camera"
    FRONT_LEFT_CAMERA = "front_left_camera"
    FRONT_RIGHT_CAMERA = "front_right_camera"
    BACK_LEFT_CAMERA = "back_left_camera"
    BACK_RIGHT_CAMERA = "back_right_camera"
