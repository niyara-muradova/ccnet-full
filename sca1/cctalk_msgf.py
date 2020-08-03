import myhex

"""
7.1 Standard Message Packets, Simple checksum 
 
For a payload of N data bytes… 
 
[ Destination Address ] 
[ No. of Data Bytes ] 
[ Source Address ] 
[ Header ] 
[ Data 1 ] 
... 
[ Data N ] 
[ Checksum ] 

For a simple command or request with no data bytes… 
 
[ Destination Address ] 
[ 0 ] 
[ Source Address ] 
[ Header ] 
[ Checksum ]

The acknowledge message is produced by setting the header to zero and having no data bytes… 
 
[ Destination Address ] 
[ 0 ] 
[ Source Address ] 
[ 0 ] 
[ Checksum ]
 
"""


class Message:
    # 2 Message Format
    DEST = 0x02
    LNG = 0x00
    SOUR = 0x01
    HEAD = None
    DATA = None
    RDATA = None
    CRC = 0x00

    host_address = 1
    device_address = 2

    coins = [0]*17
    accepted = []

    """
        для монетоприемников по умолчанию задан адрес 2, 
        для бункеров - адрес 3, 
        для счетчиков - 40 
    """

    # CRC16
    POLYNOMIAL = 0x8408

    def getCRC16(self, _body):
        _CRC = 0x00
        for _data in _body:
            _CRC ^= _data
            for _ in range(0, 8):
                if (_CRC & 0x0001):
                    _CRC >>= 1
                    _CRC ^= self.POLYNOMIAL
                else:
                    _CRC >>= 1
        return [myhex.LOW(_CRC), myhex.HIGH(_CRC)]

    def getCRC(self, _body):
        _CRC = 0x00
        for _data in _body:
            _CRC += _data
        return 256 - _CRC % 256

    def proceed(self):
        return self

    def generate(self):

        self.body = [self.DEST, self.LNG, self.SOUR, self.HEAD]

        if self.DATA != None:
            self.body += self.DATA

        self.body += [self.getCRC(self.body)]

        return self

    def ACK(self):
        self.DEST = self.host_address
        self.LNG = 0
        self.SOUR = self.device_address
        self.HEAD = 0
        self.DATA = None
        self.generate()
        return self

    def NAK(self):
        self.DEST = self.host_address
        self.LNG = 0
        self.SOUR = self.device_address
        self.HEAD = 5
        self.DATA = None
        self.generate()
        return self

    def BUSY(self):
        self.DEST = self.host_address
        self.LNG = 0
        self.SOUR = self.device_address
        self.HEAD = 6
        self.DATA = None
        self.generate()
        return self

    def CLEAR(self):
        self.coin1A = 0
        self.coin1B = 0

        self.coin2A = 0
        self.coin2B = 0

        self.coin3A = 0
        self.coin3B = 0

        self.coin4A = 0
        self.coin4B = 0

        self.coin5A = 0
        self.coin5B = 0


"""
a = Message()
a.DEST = 1
a.LNG = 3
a.SOUR = 2
a.HEAD = 0
a.DATA = [78, 97, 188]
a.generate()
print(a.body)
#[1, 3, 2, 0, 78, 97, 188, 143]


7.12 Anatomy of an Example Message Sequence 
 
Let’s suppose the host machine wishes to find the serial number 
of an attached slave device. 

It therefore sends the ‘Request serial number’ command. 
 
Host sends… 

[ 2 ] - this is to slave address 2 
[ 0 ] - there are no additional data bytes to send 
[ 1 ] - this is from host address 1 
[ 242 ] - header is 242 ( Request serial number ) 
[ 11 ] - checksum, 

2 + 0 + 1 + 242 + 11 = 256 = 0 ( modulo 256 ) 

Host receives… 

[ 1 ] - this is to host address 1 
[ 3 ] - there are 3 data bytes in the reply 
[ 2 ] - this is from slave address 2 
[ 0 ] - header is 0, i.e. it’s a reply ! 
[ 78 ] - data byte 1 = 78 
[ 97 ] - data  byte 2 = 97 
[ 188 ] - data byte 3 = 188 
[ 143 ] - checksum, 

1 + 3 + 2 + 0 + 78 + 97 + 188 + 143 = 512 = 0 ( modulo 256 ) 

Interpreting the return data, 

serial number = 78 + 256 * 97 + 65536 * 188 = 12,345,678 in decimal.


21. Discussion of Transitory versus Steady-state Events 
 
The primary mechanism used to transfer information from a peripheral to the host machine is through event polling. 
 
For coin acceptors this is… Header 229, Read buffered credit or error codes 
 
For bill validators this is… Header 159, Read buffered bill events 
 
For hoppers this is… Header 166, Request hopper status 

"""
