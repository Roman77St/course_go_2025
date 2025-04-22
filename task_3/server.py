import socket

def get_page(page: str) -> bytes:
    with open(page, encoding='utf8') as p:
        response = p.read()
    return response.encode()

def get_request(data: bytes) -> dict :
    raw_data = data.decode().strip().split('\r\n')
    request = {}
    method, uri, protocol = raw_data[0].split()
    request['method'] = method
    request['uri'] = uri
    request['protocol'] = protocol
    for line in raw_data[1:]:
        split_line = line.split(':', maxsplit=1)
        if len(split_line) > 1:
            request[split_line[0]] = split_line[1]
        else:
            request['body'] = split_line[0]
    return request

def handle(request: dict) -> bytes:
    if request['method'] == 'GET':
        if request['uri'] == '/':
            return get_page('index.html')
        elif request['uri'] == '/login':
            return get_page('login.html')
    if request['method'] == "POST":
        if request['uri'] == '/login':
            post_data = request['body']
            print(post_data)
            return get_page('post.html')
    return get_page('404.html')

HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print('Listening on 3000 ...')
    sock.listen()
    while True:
        conn, addr = sock.accept()
        print(f'Connected by {addr}')
        data = b''
        while True:
            data  = conn.recv(1024)
            if not data:
                break
            request = get_request(data)
            page = handle(request)
            conn.sendall(page)
            conn.shutdown(1)
        conn.close()
