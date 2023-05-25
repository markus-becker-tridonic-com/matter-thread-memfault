import requests
import socket

LOCAL_IP = "localhost"
LOCAL_PORT = 20001
BUFFER_SIZE = 508 + 28

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((LOCAL_IP, LOCAL_PORT))

print(f"Listening on {LOCAL_IP}:{LOCAL_PORT}")

def post_chunk(project_key, chunk, device_serial):
    CHUNK_BASE_URL = "https://chunks.memfault.com"
    CHUNK_API_HEADERS = {
        "Memfault-Project-Key": project_key,
        "Content-Type": "application/octet-stream",
    }
    url = "{}/api/v0/chunks/{}".format(CHUNK_BASE_URL, device_serial)
    response = requests.post(url, data=chunk, headers=CHUNK_API_HEADERS)
    if response.status_code == 202:
        print("Success")
    else:
        print(response.status_code)
        print(response.text)

while(True):
    message, address = UDPServerSocket.recvfrom(BUFFER_SIZE)
    version_bytes, project_key_bytes, device_serial_bytes, chunk_bytes = message.split(b"\x00", 3)
    version = version_bytes.decode('utf-8')
    project_key = project_key_bytes.decode('utf-8')
    device_serial = device_serial_bytes.decode('utf-8')
    print("{}: version {}, project key {}, device_serial {}, chunk {}".format(address, version, project_key, device_serial, chunk_bytes))
    post_chunk(project_key, chunk_bytes, device_serial)


