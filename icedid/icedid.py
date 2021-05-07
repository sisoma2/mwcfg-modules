import logging

from malduck.extractor import Extractor
from malduck.pe import MemoryPEData
from malduck.pe import PE
log = logging.getLogger(__name__)

__author__  = "4rchib4ld"
__version__ = "1.0.0"

class IcedID(Extractor):

    """
    IcedID C2 Domain Configuration Extractor
    """

    family     = 'IcedID'
    yara_rules = 'icedid',

    @staticmethod
    def extractPayload(p, count, xorKeyCount):
        # Extracting the payload from the .data section
        MAX_STRING_SIZE = 128
        for section in p.sections:
            if ".data" in str(section.Name):
                data = section.get_data()
                payload = data[4:MAX_STRING_SIZE].split(b"\0")[0]
                return payload  

    @Extractor.extractor
    def obfuscationCode(self, p, addr):
        pe_rep = PE(data=p)
        payload = self.extractPayload(pe_rep)
        decrypted = ""
        for i in range(32):
            try:
                decrypted += chr(payload[i+64] ^ payload[i])
            except IndexError:
                pass
        c2 = decrypted.split("\x00")[0]
        config = {
            'family': self.family,
            'url': c2
        }
        return config