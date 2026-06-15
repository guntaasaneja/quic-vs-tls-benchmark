import socket, ssl, time

HOST = "127.0.0.1"     # or LAN IP
PORT = 4433

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print("[CLIENT] Connected to server")
        print(f"{'Size (KB)':>10} | {'Time (s)':>10} | {'Throughput (Mbps)':>18}")
        print("-" * 44)

        size = 1024
        MAX_SIZE = 1024 * 1024 * 1024  # 1 GB

        while size <= MAX_SIZE:
            data = b"A" * size
            start = time.perf_counter()
            start = time.perf_counter()
            ssock.sendall(data)

            received = 0
            while received < size:
                chunk = ssock.recv(65536)
                if not chunk:
                    break
                received += len(chunk)

            elapsed = time.perf_counter() - start
            throughput = (size * 8) / (elapsed * 1e6)
            print(f"{size/1024:10.0f} | {elapsed:10.7f} | {throughput:18.3f}")
            size *= 2
