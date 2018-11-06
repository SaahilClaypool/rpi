from pcapfile import savefile
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
from pcapfile.protocols.transport import tcp
import binascii
import re

"""
Usage:
> pip3 install pypcapfile
"""


testcap = open('./Results/100mbps_compete_bbr1_bbr1_pi@tarta1.pcap', 'rb')

capfile = savefile.load_savefile(testcap, verbose=True)

sender_src = re.compile(f"192.168.2..")
sender_dst = re.compile(f"192.168.1..")

for packet in capfile.packets:
    eth_frame: ethernet.Ethernet = ethernet.Ethernet(packet.raw())
    ip_packet: ip.IP = ip.IP(binascii.unhexlify(eth_frame.payload))
    tcp_pkt: tcp.TCP = tcp.TCP(binascii.unhexlify(ip_packet.payload))

    dst = ip_packet.dst.decode("utf-8")
    src = ip_packet.src.decode("utf-8")
    b = len(ip_packet.payload)
    print(tcp_pkt)
    break
    
def parse(packet) -> (ethernet.Ethernet, ip.IP, tcp.TCP):
    eth_frame: ethernet.Ethernet = ethernet.Ethernet(packet.raw())
    ip_packet: ip.IP = ip.IP(binascii.unhexlify(eth_frame.payload))
    tcp_pkt: tcp.TCP = tcp.TCP(binascii.unhexlify(ip_packet.payload))
    return eth_frame, ip_packet, tcp_pkt
    
def throughput_per_packet(packets, src, dst):
    bottom_ack = 0
    bottom_time = 0
    bottom_bytes = 0
    for packet in packets:
        (eth_f, ip_p, tcp_p) = parse(packet)
        pkt_dst = ip_p.dst.decode("utf-8")
        pkt_src = ip_p.src.decode("utf-8")
        if (src.match(pkt_src)): # if the packet is leaving the stream
            bottom_bytes += len(tcp_p.payload)


