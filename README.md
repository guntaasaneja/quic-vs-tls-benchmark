# QUIC vs TLS Protocol Benchmarking Study

**A comprehensive experimental comparison of QUIC (HTTP/3) and TLS (HTTPS over TCP) for modern network communication**

---

## 📋 Project Overview

This project provides an empirical analysis comparing **QUIC (HTTP/3)** and **TLS (HTTPS over TCP)** protocols across different network conditions. Through controlled experiments with doubling payload sizes (1 KB → 1 GB), this study measures performance differences, explains root causes, and provides practical recommendations for protocol selection.

### Key Research Questions
- How does QUIC perform compared to TLS in local and LAN environments?
- What are the trade-offs between kernel-optimized TCP and user-space QUIC implementations?
- When should developers choose QUIC over TLS and vice versa?

---

## 🧪 Experimental Setup

### Hardware & Environment
- **OS**: macOS / Linux
- **Network Scenarios**: 
  - Same machine (localhost) testing
  - Local Area Network (LAN) testing
- **Wi-Fi Network**: Connected laptops on same LAN

### Software Stack
- **Python 3.13** for test implementation
- **aioquic** library for QUIC (HTTP/3) implementation
- **Python ssl + socket** for TLS (OpenSSL integration)
- **Test Pattern**: Echo server architecture for bidirectional communication

### Measurement Methodology
For each payload size (1 KB, 2 KB, 4 KB, ..., 1 GB):
1. Record start timestamp
2. Send payload from client to server
3. Record end timestamp
4. Compute elapsed time and throughput (Mbps)
5. Repeat 3 trials per size for statistical validity

---

## 🚀 Quick Start

### Prerequisites
```bash
python3 --version  # 3.10+
pip install -r requirements.txt
```

### Running TLS Benchmark (Same PC)
```bash
cd 2-DataTransfer/aioquic-main
python3 examples/https\(TLS\)_server.py --host 127.0.0.1 --port 4433 &
sleep 2
python3 examples/https\(TLS\)_client.py
```

### Running QUIC Benchmark (Same PC)
```bash
cd 2-DataTransfer/aioquic-main
python3 examples/http3\(QUIC\)_server.py \
  --certificate examples/cert.pem \
  --private-key examples/key.pem \
  --host 127.0.0.1 --port 4433 &
sleep 2
python3 examples/http3\(QUIC\)_client.py https://127.0.0.1:4433/ --insecure
```

### Running Over LAN
1. Update server IP in client scripts: `HOST = "192.168.1.X"`
2. Run server on server machine: `python3 examples/https\(TLS\)_server.py --host 0.0.0.0 --port 4433`
3. Run client from another machine with updated IP

---

## 📊 Key Findings

### Same-PC Results
- **TLS is 20-40% faster** in local loopback tests
- **Root Cause**: Kernel TCP optimizations + compiled OpenSSL vs Python user-space QUIC
- **Key Insight**: Loopback networking bypasses many real-world network delays that QUIC is optimized for

### LAN Results
- **QUIC performs better** with optimized implementations
- **Why**: Designed for real-world network conditions (packet loss, variable latency, connection migration)
- **Takeaway**: QUIC shines in production environments with actual network variability

### Why TLS Wins Locally
1. **Kernel-level TCP optimization**: 30+ years of tuning
2. **Hardware acceleration**: OpenSSL uses cryptographic acceleration
3. **Loopback bypass**: OS optimizes localhost path; QUIC still pays user-space overhead

### Why QUIC Wins in Production
1. **Elimination of head-of-line blocking**: Per-stream reliability vs TCP's strict ordering
2. **Integrated TLS 1.3**: Reduced handshake round trips (0-RTT support)
3. **Connection migration**: Survives IP/network changes (critical for mobile)
4. **User-space congestion control**: Rapid algorithm updates (BBR, BBRv2, Copa)
5. **Encrypted metadata**: Prevents middlebox interference
6. **Optimized for mobile/wireless**: Handles loss, latency variance, and network switching

---

## 📁 Project Structure

```
quic-vs-tls-benchmark/
├── README.md                    # This file
├── RESULTS.md                   # Detailed results & metrics
├── .gitignore                   # Git exclusion rules
├── docs/
│   └── analysis.md              # Deep technical analysis
├── results/
│   ├── tls_benchmark.csv        # TLS benchmark data
│   └── quic_benchmark.csv       # QUIC benchmark data
└── 2-DataTransfer/
    ├── aioquic-main/            # QUIC protocol library (aioquic)
    │   ├── examples/
    │   │   ├── https(TLS)_client.py
    │   │   ├── https(TLS)_server.py
    │   │   ├── http3(QUIC)_client.py
    │   │   ├── http3(QUIC)_server.py
    │   │   └── cert.pem          # Self-signed certificate
    │   └── src/
    │       └── aioquic/          # Library source code
    └── New/
        └── (Benchmark results exported to results/ as CSV)
```

---

## 📈 Results Summary

| Scenario | Winner | Performance Gap | Reason |
|----------|--------|-----------------|--------|
| Same PC (localhost) | TLS | 20-40% faster | Kernel optimization, loopback bypass |
| LAN (real network) | QUIC | Variable | Better loss recovery, multiplexing |
| High latency / Lossy | QUIC | Significantly | 0-RTT, per-stream reliability |
| Mobile networks | QUIC | Decisive | Connection migration, pacing |
| Large files (1 GB) | Depends | Implementation-specific | Memory management, buffering |

**Full results with charts available in [RESULTS.md](RESULTS.md)**

---

## 🔍 Technical Insights

### Implementation Layers Tested
- **Transport**: TCP vs UDP
- **Encryption**: TLS 1.3 (both integrated into QUIC and separate for TCP)
- **HTTP**: HTTP/1.1 over HTTPS vs HTTP/3 over QUIC
- **Application**: Echo server for deterministic measurement

### Why Python aioquic?
- Pure Python implementation allows detailed observation
- Works on all platforms
- Demonstrates protocol logic clearly
- Production implementations (Cloudflare, Google) use compiled versions for optimization

### Measurement Challenges Addressed
1. **Timer precision**: Used high-resolution time.time()
2. **Network variability**: Multiple trials (n=3) with averages
3. **OS scheduling**: Localhost tests eliminate network variance
4. **Statistical validity**: Simple but repeatable methodology

---

## 📚 For Recruiters: What This Demonstrates

✅ **Network Protocol Knowledge**
- Understanding of TCP/UDP differences
- TLS/cryptography concepts
- HTTP/2 vs HTTP/3 architecture

✅ **Performance Analysis Skills**
- Benchmarking methodology
- Root cause analysis
- Trade-off evaluation (performance vs. complexity)

✅ **System-Level Understanding**
- Kernel vs user-space implementations
- OS optimization techniques
- Network stack internals

✅ **Research & Documentation**
- Reproducible experiments
- Clear visualization of results
- Practical recommendations

---

## 🛠️ Technologies & Skills Demonstrated

- **Languages**: Python 3
- **Protocols**: QUIC, TLS 1.3, TCP, UDP, HTTP/3, HTTPS
- **Libraries**: aioquic, ssl, socket, asyncio
- **Tools**: Git, Performance benchmarking, Data analysis
- **Concepts**: Transport protocols, Encryption, Network latency, Throughput measurement

---

## 📖 References

- [QUIC RFC 9000](https://tools.ietf.org/html/rfc9000)
- [HTTP/3 RFC 9114](https://tools.ietf.org/html/rfc9114)
- [aioquic GitHub](https://github.com/aiortc/aioquic)
- Full analysis: See [docs/analysis.md](docs/analysis.md)

---

## 📝 How to Reproduce

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Navigate to `2-DataTransfer/aioquic-main`
4. Follow benchmark instructions in README or run scripts
5. Compare results with data in `results/` directory

---

## 📧 Notes

- **Last Updated**: November 2025
- **Python Version**: 3.13
- **Environment**: macOS / Linux
- **Network**: WiFi LAN setup
- For detailed technical analysis, see [docs/analysis.md](docs/analysis.md)

---

**Ready for production-grade QUIC implementations? Check out:**
- Cloudflare's quiche
- Google's QUIC
- nginx QUIC support

