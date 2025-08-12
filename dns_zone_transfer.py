#!/usr/bin/env python3
"""
DNS Zone Transfer Tool

This script attempts to perform a DNS zone transfer (AXFR) for a given domain using each name server obtained via nslookup.
It uses the 'nslookup' and 'dig' command-line utilities via subprocess. If a zone transfer succeeds, the returned records
are printed. Otherwise, a failure message is shown.

Usage:
    python dns_zone_transfer.py example.com

Note: This script is for educational and testing purposes only. Always ensure you have permission to attempt zone transfers.
"""

import argparse
import subprocess
import re
import sys

def get_name_servers(domain):
    try:
        result = subprocess.run(['nslookup', '-type=ns', domain], capture_output=True, text=True, check=True)
    except Exception as e:
        print(f'Error running nslookup: {e}')
        return []
    servers = re.findall(r'nameserver = ([\w.-]+)', result.stdout)
    return [s.strip('.') for s in servers]

def attempt_zone_transfer(domain, server):
    try:
        result = subprocess.run(['dig', f'@{server}', domain, 'axfr', '+time=5', '+tries=1'], capture_output=True, text=True)
        output = result.stdout
        if 'Transfer failed' in output or 'failed' in output.lower() or 'timed out' in output.lower():
            return None
        return output
    except FileNotFoundError:
        print("dig command not found. Please install 'dnsutils' or bind-utils.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Attempt DNS zone transfer for a domain')
    parser.add_argument('domain', help='Domain to test for zone transfer')
    args = parser.parse_args()
    ns_servers = get_name_servers(args.domain)
    if not ns_servers:
        print(f'No name servers found for {args.domain}')
        return
    for ns in ns_servers:
        print(f'[*] Trying zone transfer from {ns}...')
        records = attempt_zone_transfer(args.domain, ns)
        if records:
            print(f'[+] Zone transfer successful from {ns}:\n')
            print(records)
        else:
            print(f'[-] Zone transfer failed or refused by {ns}\n')

if __name__ == '__main__':
    main()
