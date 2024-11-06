import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.163.103:5555")

# JSONでリクエストを送信
socket.send_json({"filename": "sample_image.png"})
message = socket.recv_json()
print(message)
