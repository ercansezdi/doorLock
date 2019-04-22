__version__ = "2.2.1"

try:
    from .rfid import RFID
    from .util import RFIDUtil
except RuntimeError:
    pass
