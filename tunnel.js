#!/usr/bin/env node

/**
 * ngrok Tunnel Configuration
 * Exposes local server to public internet
 */

const ngrok = require("ngrok");

const port = process.argv[2] || 9000;

async function startTunnel() {
  console.log(`
╔════════════════════════════════════════════════════════════════════╗
║                    NGROK TUNNEL STARTUP                           ║
║         Exposing Wormhole Exit Server to Public Internet           ║
╚════════════════════════════════════════════════════════════════════╝
`);

  try {
    console.log(`[*] Connecting to ngrok...`);
    console.log(`[*] Local port: 127.0.0.1:${port}\n`);

    // Start ngrok tunnel
    const url = await ngrok.connect({
      addr: port,
      proto: "http",
    });

    console.log("\n" + "=".repeat(70));
    console.log("SUCCESS: NGROK TUNNEL ACTIVE");
    console.log("=".repeat(70));
    console.log(`[+++] PUBLIC URL: ${url}`);
    console.log(`[+++] Public Access: ${url}/`);
    console.log("=".repeat(70) + "\n");

    // Save URL to file
    const fs = require("fs");
    fs.writeFileSync("tunnel_url.txt", `${url}\n`);
    console.log(`[+] Tunnel URL saved to: tunnel_url.txt\n`);

    console.log("[*] Connection Information:");
    console.log(`    - POST data captured by Python server`);
    console.log(`    - Index.html served from wormhole_exit.py`);
    console.log(`    - Traffic tunneled through: ${url}\n`);

    console.log("[*] Press Ctrl+C to stop tunnel\n");
  } catch (error) {
    console.error("\n[!!!] NGROK ERROR");
    console.error("=".repeat(70));
    console.error(`Error: ${error.message}`);

    if (error.message.includes("ECONNREFUSED")) {
      console.error("\n[!] Connection refused - Python server not running");
      console.error("[!] Start Python server: python wormhole_exit.py\n");
    } else if (error.message.includes("authtoken")) {
      console.error("\n[!] ngrok authtoken not configured");
      console.error("[!] Setup: ngrok config add-authtoken YOUR_TOKEN");
      console.error("[!] Get token from: https://dashboard.ngrok.com\n");
    }

    console.error("=".repeat(70) + "\n");
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on("SIGINT", async () => {
  console.log("\n[*] Shutting down tunnel...");
  await ngrok.kill();
  process.exit(0);
});

// Start tunnel
startTunnel();
