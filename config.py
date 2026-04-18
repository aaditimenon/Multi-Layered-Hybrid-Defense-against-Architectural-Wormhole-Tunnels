# Configuration for Wormhole Attack Simulation

# WORMHOLE EXIT (Server receiving captured credentials)
EXIT_CONFIG = {
    "listen_host": "0.0.0.0",  # Listen on all interfaces
    "ports": [8080, 8888, 9000, 9999],
    "public_ip": "YOUR_PUBLIC_IP_HERE",  # Set to your actual public IP
}

# WORMHOLE ENTRANCE (DNS spoofing)
ENTRANCE_CONFIG = {
    "target_domain": "www.example.com",
    "wormhole_exit": "YOUR_PUBLIC_IP_HERE",  # Where victims get redirected
}

# DEFENDER (Detection tool)
DEFENDER_CONFIG = {
    "trusted_domains": {
        "www.example.com": "93.184.216.34",
    }
}
