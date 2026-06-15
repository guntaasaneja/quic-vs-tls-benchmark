import ssl
import http.client
import time
import argparse
from urllib.parse import urlparse

def measure_tls(url: str):
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 443
    path = parsed.path or "/"

    # TLS context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # skip self-signed verification

    # Handshake + TCP connect
    start_handshake = time.time()
    conn = http.client.HTTPSConnection(host, port, context=context)
    conn.connect()  # TCP + TLS handshake
    end_handshake = time.time()
    handshake_time = end_handshake - start_handshake

    # Measure RTT for GET request
    start_rtt = time.time()
    conn.request("GET", path)
    resp = conn.getresponse()
    data = resp.read()
    end_rtt = time.time()
    rtt = end_rtt - start_rtt

    # Throughput
    size_bytes = len(data)
    elapsed = end_rtt - start_handshake
    throughput_mbps = (size_bytes * 8) / elapsed / 1_000_000

    print(f"TLS Performance for {url}")
    print(f"Handshake: {handshake_time:.4f}s")
    print(f"Request RTT: {rtt:.4f}s")
    print(f"Elapsed total: {elapsed:.4f}s")
    print(f"Throughput: {throughput_mbps:.3f} Mbps")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TLS Benchmark")
    parser.add_argument("url", type=str, help="HTTPS URL to test")
    args = parser.parse_args()
    measure_tls(args.url)
