import myhex
import json


class CCTalkReply:

    def cctalk_parse(self, head, rhead, data):
        if len(data) == 0:
            if rhead == 0:
                print('ACK')
            if rhead == 5:
                print('NAK')
            if rhead == 6:
                print('BUSY')
            return self

        if head == 242:
            self.serial_number = data[0] + data[1] * 256 + data[2] * 65536
            print('Serial Number: {}'.format(self.serial_number))
            return self

        if head == 184:
            coin_id = self.DATA[0]
            coin_info = self.RDATA.decode()
            if coin_info[0] != '.':
                coin_nominal = int(coin_info[2:-1])
                self.coins[coin_id] = coin_nominal
                print('coin id {} is {} KZT '.format(coin_id, coin_nominal))
            return self

        if head == 229:
            if len(data) == 11:

                self.event_counter = data[0]

                self.coin1A = data[1]
                self.coin1B = data[2]

                self.coin2A = data[3]
                self.coin2B = data[4]

                self.coin3A = data[5]
                self.coin3B = data[6]

                self.coin4A = data[7]
                self.coin4B = data[8]

                self.coin5A = data[9]
                self.coin5B = data[10]

            return self


"""

coin1 
        naminals.put("KZ005A", 5);
        naminals.put("KZ005B", 5);
coin2
        naminals.put("KZ010A", 10);
        naminals.put("KZ010B", 10);
coin3 
        naminals.put("KZ020A", 20);
        naminals.put("KZ020B", 20);
coin4 
        naminals.put("KZ050A", 50);
        naminals.put("KZ050B", 50);
coin5 
        naminals.put("KZ100A", 100);
        naminals.put("KZ100B", 100);

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

15.1.1 Expansion Headers 
 
Headers 100, 101, 102 and 103 are used to indicate another 
set of headers within the message data.

Although this lengthens the expansion messages by 1 byte, 
it immediately gives access to 1024 extra commands. 

Money Controls will use this approach for its future range of products. 
 
As an example, suppose we add a new command ‘Request ASCII serial number’ 
which returns a serial number in ASCII rather than binary. 

We will define this new command as EH 100:255 ( expansion header 100, sub-header 255 ). 
 
Host sends… 

[ 2 ] - destination address 
[ 1 ] - 1 data byte = 1 x sub-header 
[ 1 ] - source address 
[ 100 ] - expansion header 100 
[ 255 ] - sub-header 255 ( e.g. Request ASCII serial number ) 
[ 153 ] - checksum, 

2 + 1 + 1 + 100 + 255 + 153 = 512 = 0 
 
Host receives… 

[ 1 ] - destination address 
[ 8 ] - 8 data bytes 
[ 2 ] - source address 
[ 0 ] - reply header 
[ 49 ] - ‘1’ 
[ 50 ] - ‘2’ 
[ 51 ] - ‘3’ 
[ 52 ] - ‘4’ 
[ 53 ] - ‘5’ 
[ 54 ] - ‘6’ 
[ 55 ] - ‘7’ 
[ 56 ] - ‘8’ 
[ 81 ] - checksum, 

1 + 8 + 2 +… = 512 = 0

"""
