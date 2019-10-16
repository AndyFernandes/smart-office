import socket
from flask import Flask, request, jsonify
import collections
from threading import Timer
import json
from flask_cors import CORS
import copy 
app = Flask(__name__)
CORS(app)

devices = [{
        "tipo": "Ar-condicionado",
        "ip": "adosihdaiosddios",
        "id": "1",
        "porta": 3000,
        "acoes": {
            "status": "Ligado",
            "temperatura": 30,
        }
    },{
        "tipo": "TV",
        "ip": "adosihdaiosddios",
        "id": "2",
        "porta": 3000,
        "acoes": {
            "status": "Ligado",
            "canal": 30,
            "volume": 20
        }
    },{
        "tipo": "Lâmpada",
        "ip": "adosihdaiosddios",
        "id": "3",
        "porta": 3000,
        "acoes": {
            "status": "Ligado",
        }
    },{
        "tipo": "Lâmpada",
        "ip": "adosihdaiosddios",
        "id": "5",
        "porta": 3000,
        "acoes": {
            "status": "Desligado"
        }
    }]

@app.route('/getDevices', methods=['GET'])
def get_devices():
    resultado = []
    for device in devices:
        dev = device
        resultado.append(dev)
    return jsonify(resultado)


@app.route('/changeStatus/<string:id>/<string:new_status>', methods=["PUT"])
def change_status(id, new_status):
    dev = None
    for device in devices:
        if(device['id'] == id):
            device["acoes"]["status"] = str(new_status)
            dev = copy.copy(device)
            dev['acoes'] = json.dumps(dev['acoes'], separators=(',', ':'))
            # sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
            # sock.sendto(json.dumps(dev).encode(), (device['ip'], device['porta']))
    return json.dumps(dev, separators=(',', ':'))


@app.route('/changeTemp/<string:id>/<string:new_temp>', methods=["PUT"])
def change_temperatura(id, new_temp):
    dev = None
    for device in devices:
        if(device['id'] == id):
            device["acoes"]["temperatura"] = str(new_temp)
            dev = copy.copy(device)
            dev['acoes'] = json.dumps(dev['acoes'], separators=(',', ':'))
            # sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
            # sock.sendto(json.dumps(dev).encode(), (device['ip'], device['porta']))
    return json.dumps(dev, separators=(',', ':'))

@app.route('/changeCanal/<string:id>/<string:new_canal>', methods=["PUT"])
def change_canal(id, new_canal):
    dev = None
    for device in devices:
        if(device['id'] == id):
            device["acoes"]["canal"] = str(new_canal)
            dev = copy.copy(device)
            dev['acoes'] = json.dumps(dev['acoes'], separators=(',', ':'))
            # sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
            # sock.sendto(json.dumps(dev).encode(), (device['ip'], device['porta']))
    return json.dumps(dev, separators=(',', ':'))


@app.route('/changeVolume/<string:id>/<string:new_volume>', methods=["PUT"])
def change_volume(id, new_volume):
    dev = None
    for device in devices:
        if(device['id'] == id):
            device["acoes"]["volume"] = str(new_volume)
            dev = copy.copy(device)
            dev['acoes'] = json.dumps(dev['acoes'], separators=(',', ':'))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(json.dumps(dev).encode(), (device['ip'], device['porta']))
    return json.dumps(dev, separators=(',', ':'))


if __name__ == '__main__':
    def decode_json(msg):
        device = json.loads(msg)
        for dev in devices:
            if (device['ip'] == dev['ip']):
                return
        devices.append(device)

    app.run(host='127.0.0.1', port='2000', debug=True)
    devices = []
    server_ip = socket.gethostbyname(socket.gethostname())
    server_port = 3000
    server_addr = (server_ip, int(server_port))

    broadcast_ip = '255.255.255.255'
    broadcast_port = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    broacast_addr = (broadcast_ip, broadcast_port)

    sock.bind(server_addr)

    msg = 'Aguardando Conexao...'


    def send_broadcast():
        sock.sendto(msg.encode(), broacast_addr)

    sock.sendto(msg.encode(), broacast_addr)

    while True:
        # ------------ RECEIVE TO DEVICE
        t = Timer(10.0, send_broadcast)
        t.start()
        data, client = sock.recvfrom(1024)
        #TODO: Verificação se o tipo de dispositivo é válido
        #TODO: ADicionar na lista de devices
        # ---------- TESTES DO TIPO DE DADO 
        # print (data)
        # print (type(data))
        data_dec = data.decode("utf-8")
        # print (type(x))
        data_dec = data_dec.replace("'", '"')

        data_json = json.loads(data_dec)
        print (data_json)
        print (type(data_json))

        sock.close()

        # ------------ SEND TO DEVICE
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # ip_device = '127.0.0.1'
        # port_device = 5001
        # device_addr = (ip_device, port_device)
        # msg = '{"acoes": {"status": "Ligado","temperatura": 45}}'
        # sock.sendto(msg.encode(), device_addr)

        #decode_json(data.decode())
        #print(len(devices))