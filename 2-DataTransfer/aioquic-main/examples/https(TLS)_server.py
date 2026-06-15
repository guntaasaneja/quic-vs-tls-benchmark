import socket
import ssl

HOST = "0.0.0.0"
PORT = 4433

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"[SERVER] Listening on https://{HOST}:{PORT}")

    while True:
        conn, addr = sock.accept()
        print(f"[SERVER] Connected by {addr}")
        with context.wrap_socket(conn, server_side=True) as ssock:
            try:
                while True:
                    data = ssock.recv(65536)
                    if not data:
                        break
                    ssock.sendall(data)  # Echo back immediately
            except Exception as e:
                print(f"[SERVER] Connection error: {e}")
            finally:
                ssock.close()

