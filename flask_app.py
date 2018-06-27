from flask import Flask, request, render_template, flash
import cgi

def check_data():
    form = cgi.FieldStorage()
    imei = form["imei"]
    momsn = form["momsn"]
    transmit_time = form["transmit_time"]
    iridium_latitude = form["iridium_latitude"]
    iridium_longitude = form["iridium_longitude"]
    iridium_cep = form["iridium_cep"]
    data = form["data"]
    #data = data.decode("hex")
    print("Content-Type:text/html\n\n")
    print("OK")
    return data

class Parser(object):

    def __init__(self, data):
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
        self.GPSPos = float.fromhex(data[38:54])
        self.GPSQuality = int(data[54:56], 16)
        self.UnstructLen = int(data[56:58], 16)
        if ((self.MsgLen-2) - 58) > 0:
            self.Unstructured = int(data[58: self.MsgLen-2], 16)
        self.Crc = int(data[self.MsgLen-1], 16)

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    data = check_data()
    return render_template("index.html", test=True, data=data)

@app.route("/", methods=["POST"])
def submit():
    #try:
    payload = request.form['payload']
    return flash(payload)
    #return "\n".join(m1.a)
    #return "<br>".join(m1.a)
    #except:
    #    return index()

app.secret_key = "secret"
