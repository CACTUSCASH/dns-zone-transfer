# DNS Zone Transfer

A simple Python tool to test for DNS zone transfer vulnerabilities. It attempts an AXFR zone transfer on each name server of a domain by invoking standard command-line tools.

## Features

- Retrieves all authoritative name servers for a domain using `nslookup`.
- Attempts a DNS zone transfer (AXFR) using `dig` against each name server.
- Prints the zone records if a transfer succeeds.
- Uses only standard tools available on most Unix systems (`nslookup`, `dig`).

## Usage

First ensure you have `nslookup` and `dig` installed on your system. Then run:

```bash
python dns_zone_transfer.py example.com
```

The script will list each name server and whether the zone transfer was successful.

## Disclaimer

This tool is provided for educational and authorized security testing purposes only. Attempting zone transfers on domains without permission may be illegal and unethical. Always obtain proper authorization before testing.
