import myhex


class Commands:
    def init(self):
        self.DATA = None

    def SimplePoll(self):
        self.LNG = 0
        self.HEAD = 254
        self.DATA = None
        return None

    def RequestStatus(self):
        self.LNG = 0
        self.HEAD = 248
        self.DATA = None
        return None

    def RequestManufacturerId(self):
        self.LNG = 0
        self.HEAD = 246
        self.DATA = None
        return None

    def RequestEquipmentCategoryId(self):
        self.LNG = 0
        self.HEAD = 245
        self.DATA = None
        return None

    def RequestProductCode(self):
        self.LNG = 0
        self.HEAD = 244
        self.DATA = None
        return None

    def RequestDatabaseVersion(self):
        self.LNG = 0
        self.HEAD = 243
        self.DATA = None
        return None

    def RequestSerialNumber(self):
        self.LNG = 0
        self.HEAD = 242
        self.DATA = None
        return None

    def RequestSoftwareRevision(self):
        self.LNG = 0
        self.HEAD = 241
        self.DATA = None
        return None

    def EnableCoins(self):
        self.LNG = 2
        self.HEAD = 231
        self.DATA = [0xff, 0xff]
        return None

    def DisableCoins(self):
        self.LNG = 2
        self.HEAD = 231
        self.DATA = [0x00, 0x00]
        return None

    def RequestInhibitStatus(self):
        self.LNG = 0
        self.HEAD = 230
        self.DATA = None
        return None

    def POLL(self):
        self.LNG = 0
        self.HEAD = 229
        self.DATA = None
        return None

    def NormalOperation(self):
        self.LNG = 1
        self.HEAD = 228
        self.DATA = [0x01]
        return None

    def MasterActive(self):
        self.LNG = 1
        self.HEAD = 228
        self.DATA = [0x00]
        return None

    def RequestSorterOverrideStatus(self):
        self.LNG = 0
        self.HEAD = 221
        self.DATA = None
        return None

    def RequestOptionFlags(self):
        self.LNG = 0
        self.HEAD = 213
        self.DATA = None
        return None

    def RequestSorterPaths(self):
        self.LNG = 1
        self.HEAD = 209
        return None

    def RequestDefaultSorterPath(self):
        self.LNG = 0
        self.HEAD = 188
        self.DATA = None
        return None

    def RequestCoinId(self):
        self.LNG = 1
        self.HEAD = 184
        return None

    def ResetDevice(self):
        self.LNG = 0
        self.HEAD = 1
        self.DATA = None
        return None
