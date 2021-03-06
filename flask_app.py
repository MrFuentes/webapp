from flask import Flask, request, render_template, flash
import cgi, time, datetime
#todo:
#get server running

app = Flask(__name__)

def hex_to_float(hex):
    little_endian = str(hex[6:] + hex[4:6] + hex[2:4] + hex[0:2])
    binary = [bin(int(x, 16))[2:].zfill(4) for x in little_endian]
    binary_str = ''.join(binary)
    sign = binary_str[0]
    exponent = 2 ** (int(binary_str[1:9], 2) - 127)
    mantissa = binary_str[9:]
    i = -1
    pos = []
    for x in mantissa:
        if x == "1":
            pos.append(i)
        i -= 1
    sum = 1
    for x in pos:
        sum += 2 ** x
    if sign == 1:
        return(-1 * exponent * sum)
    else:
        return(exponent * sum)

a = [None]

class crc8:
    def __init__(self):
        self.crcTable = ( 0x00, 0x07, 0x0E, 0x09, 0x1C, 0x1B, 0x12, 0x15, 0x38, 0x3F, 0x36, 0x31, 0x24,
        0x23, 0x2A, 0x2D, 0x70, 0x77, 0x7E, 0x79, 0x6C, 0x6B, 0x62, 0x65, 0x48, 0x4F, 0x46, 0x41, 0x54,
        0x53, 0x5A, 0x5D, 0xE0, 0xE7, 0xEE, 0xE9, 0xFC, 0xFB, 0xF2, 0xF5, 0xD8, 0xDF, 0xD6, 0xD1, 0xC4,
        0xC3, 0xCA, 0xCD, 0x90, 0x97, 0x9E, 0x99, 0x8C, 0x8B, 0x82, 0x85, 0xA8, 0xAF, 0xA6, 0xA1, 0xB4,
        0xB3, 0xBA, 0xBD, 0xC7, 0xC0, 0xC9, 0xCE, 0xDB, 0xDC, 0xD5, 0xD2, 0xFF, 0xF8, 0xF1, 0xF6, 0xE3,
        0xE4, 0xED, 0xEA, 0xB7, 0xB0, 0xB9, 0xBE, 0xAB, 0xAC, 0xA5, 0xA2, 0x8F, 0x88, 0x81, 0x86, 0x93,
        0x94, 0x9D, 0x9A, 0x27, 0x20, 0x29, 0x2E, 0x3B, 0x3C, 0x35, 0x32, 0x1F, 0x18, 0x11, 0x16, 0x03,
        0x04, 0x0D, 0x0A, 0x57, 0x50, 0x59, 0x5E, 0x4B, 0x4C, 0x45, 0x42, 0x6F, 0x68, 0x61, 0x66, 0x73,
        0x74, 0x7D, 0x7A, 0x89, 0x8E, 0x87, 0x80, 0x95, 0x92, 0x9B, 0x9C, 0xB1, 0xB6, 0xBF, 0xB8, 0xAD,
        0xAA, 0xA3, 0xA4, 0xF9, 0xFE, 0xF7, 0xF0, 0xE5, 0xE2, 0xEB, 0xEC, 0xC1, 0xC6, 0xCF, 0xC8, 0xDD,
        0xDA, 0xD3, 0xD4, 0x69, 0x6E, 0x67, 0x60, 0x75, 0x72, 0x7B, 0x7C, 0x51, 0x56, 0x5F, 0x58, 0x4D,
        0x4A, 0x43, 0x44, 0x19, 0x1E, 0x17, 0x10, 0x05, 0x02, 0x0B, 0x0C, 0x21, 0x26, 0x2F, 0x28, 0x3D,
        0x3A, 0x33, 0x34, 0x4E, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5C, 0x5B, 0x76, 0x71, 0x78, 0x7F, 0x6A,
        0x6D, 0x64, 0x63, 0x3E, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2C, 0x2B, 0x06, 0x01, 0x08, 0x0F, 0x1A,
        0x1D, 0x14, 0x13, 0xAE, 0xA9, 0xA0, 0xA7, 0xB2, 0xB5, 0xBC, 0xBB, 0x96, 0x91, 0x98, 0x9F, 0x8A,
        0x8D, 0x84, 0x83, 0xDE, 0xD9, 0xD0, 0xD7, 0xC2, 0xC5, 0xCC, 0xCB, 0xE6, 0xE1, 0xE8, 0xEF, 0xFA,
        0xFD, 0xF4, 0xF3)

    def crc(self, msg):
        runningCRC = 0x42
        for c in data:
            c = int(c, 16)
            z = runningCRC ^ c
            runningCRC = self.crcTable[z]
        return hex(runningCRC)[2:]

def check_data():
    global a
    imei = request.form["imei"]
    momsn = request.form["momsn"]
    transmit_time = request.form["transmit_time"]
    iridium_latitude = request.form["iridium_latitude"]
    iridium_longitude = request.form["iridium_longitude"]
    iridium_cep = request.form["iridium_cep"]
    data = request.form["data"]
    a.append(data)
    print("ok")
    return data

class ParseFromHex(object):

    def __init__(self, data):
        lat = data[38:46]
        long = data[46:54]

        self.MsgLen = int(data[0:4], 16)
        self.MsgID = int(data[4:10], 16)
        Year = int(data[10:12], 16)
        Month = int(data[12:14], 16)
        Day = int(data[14:16], 16)
        Hour = int(data[16:18], 16)
        Min = int(data[18:20], 16)
        Sec = int(data[20:22], 16)
        self.TimeStamp = "{:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d}".format(Year, Month, Day, Hour, Min, Sec)
        self.MsgType = int(data[22:24], 16)
        self.DeviceReg = bytearray.fromhex(data[24:40]).decode()
        self.GPSLatitude = hex_to_float(data[40:48])
        self.GPSLongitude = hex_to_float(data[48:56])
        self.GPSQuality = int(data[56:58], 16)
        self.UnstructLen = int(data[58:60], 16)
        if ((self.MsgLen-2) - 56) > 0:
            self.Unstructured = int(data[56: self.MsgLen-2], 16)
        else:
            self.Unstructured = None
        crc_8 = crc8()
        crc_input = data
        msg = [crc_input[i:i+n] for i in range(0, len(crc_input), n)]
        self.crc = crc_8.crc(msg)
        if self.crc == 0:
            self.crc_test = True
        else:
            self.crc_test = False

class ParseToHex(object):

    def __init__(self, msgtype, Unstructured=None):
        self.MsgType = msgtype
        if Unstructured != None:
            Unstructured = Unstructured.encode("utf-8")
            self.Unstructured = Unstructured.hex()
            self.UnstructLen = len(self.Unstructured)
        else:
            self.Unstructured= None
            self.UnstructLen = 0
        self.MsgID = str(datetime.datetime.fromtimestamp(time.time()).strftime('%S%M%H%d%m%Y'))
        TimeStamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))
        year = hex(int(TimeStamp[2:4]))[2:].rjust(2, "0")
        month = hex(int(TimeStamp[4:6]))[2:].rjust(2, "0")
        day = hex(int(TimeStamp[6:8]))[2:].rjust(2, "0")
        hour = hex(int(TimeStamp[8:10]))[2:].rjust(2, "0")
        minute = hex(int(TimeStamp[10:12]))[2:].rjust(2, "0")
        second = hex(int(TimeStamp[12:]))[2:].rjust(2, "0")
        self.TimeStamp = year + month + day + hour + minute + second
        self.msglen = len(self.MsgType) + len(self.MsgID) + len(self.UnstructLen) + self.UnstructLen + len(self.MsgID) + len(self.TimeStamp) + 2
        crc_8 = crc8()
        if self.Unstructured == None:
            crc_input = self.msglen + self.MsgID  + self.TimeStamp + self.MsgType + self.UnstructLen
        else:
            crc_input = self.msglen + self.MsgID  + self.TimeStamp + self.MsgType + self.UnstructLen + self.Unstructured
        n = 2
        msg = [crc_input[i:i+n] for i in range(0, len(crc_input), n)]
        self.crc = crc_8.crc(msg)
        self.Msg = crc_input + self.crc

@app.route('/', methods=["GET", "POST"])
def index():
    check_data()
    global a
    data = ParseFromHex(a[-1])
    return render_template("index.html", test=data.crc_test, raw_data=a[-1], data=data)

@app.route("/", methods=["GET", "POST"])
def submit():
    MsgType = request.form['msgtype']
    payload = request.form['payload']
    data = ParseToHex(msgType, payload)
    return render_template("index.html", data=data)

app.secret_key = "secret"

if __name__ == "__main__":
    app.run()
