import cctalk_msgf
import cctalk_port
import cctalk_cmds
import cctalk_pars
import myhex
import time
import threading
import sys
import json
import configparser
import os
import redis

class CCTalkCoinAcceptor(cctalk_msgf.Message, cctalk_port.Device, cctalk_cmds.Commands, cctalk_pars.CCTalkReply, threading.Thread):

    active = threading.Event()
    pool_active = threading.Event()
    line = threading.Lock()

    debug_pool = True

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        super().__init__(*args, **kwargs)
        # CCNET config serial port

    def write(self):
        if not self.serial.is_open:
            self.serial.open()
        self.serial.write(self.body)
        return self

    def read(self):
        self.first = self.serial.read(len(self.body))
        if self.first == bytes(self.body):
            self.first = self.serial.read(4)
        self.last = self.serial.read(self.first[1]+1)
        self.rhead = self.first[3]
        self.RDATA = self.last[:-1]
        self.reply = self.first+self.last
        self.reply_hex = myhex.getHEX(self.reply)
        crc = 0
        for rbyte in self.reply:
            crc += rbyte
        self.error_crc = (crc % 256) != 0
        return self

    def parse(self):
        self.cctalk_parse(self.HEAD, self.first[3], self.RDATA)

    def send(self, cmd, debug=False):
        if self.line.acquire():
            do_event = cmd()
            self.generate()
            if debug:
                print('-> {}'.format(myhex.getHEX(self.body)))
            self.write()

            self.read()
            if debug:
                print('<- {}'.format(myhex.getHEX(self.reply)))
                print(str(self.RDATA))

            self.proceed().parse()
            if do_event:
                do_event(self.reply)
            self.line.release()

    def run(self):

        self.active.wait()
        self.pool_active.wait()

        print('pool started..')

        while self.active.is_set():
            if self.pool_active.is_set():
                time.sleep(0.2)
                self.send(self.POLL, self.debug_pool)

        print('pool ended..')

    def readConfig(self, configName):
        config = configparser.ConfigParser()
        config.read(configName)

        self.serial.port = config['DEFAULT']['port']
        self.serial.baudrate = int(config['DEFAULT']['baudrate'])
        self.serial.timeout = int(config['DEFAULT']['timeout'])
        self.serial.writeTimeout = int(config['DEFAULT']['writeTimeout'])
