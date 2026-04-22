from . import GaussianBlur
from . import GrayBalanceFromPoint
from . import ExposureMatchFromPoint
from . import ApplyWhiteBalanceGain
from . import ApplyExposureGain

NODE_CLASS_MAPPINGS = {
    **GaussianBlur.NODE_CLASS_MAPPINGS,
    **GrayBalanceFromPoint.NODE_CLASS_MAPPINGS,
    **ExposureMatchFromPoint.NODE_CLASS_MAPPINGS,
    **ApplyWhiteBalanceGain.NODE_CLASS_MAPPINGS,
    **ApplyExposureGain.NODE_CLASS_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **GaussianBlur.NODE_DISPLAY_NAME_MAPPINGS,
    **GrayBalanceFromPoint.NODE_DISPLAY_NAME_MAPPINGS,
    **ExposureMatchFromPoint.NODE_DISPLAY_NAME_MAPPINGS,
    **ApplyWhiteBalanceGain.NODE_DISPLAY_NAME_MAPPINGS,
    **ApplyExposureGain.NODE_DISPLAY_NAME_MAPPINGS,
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
