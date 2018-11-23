bbr1

State       Recv-Q Send-Q                                         Local Address:Port                                                        Peer Address:Port
ESTAB       0      0                                                192.168.2.1:43712                                                        192.168.1.1:5201
         bbr1 wscale:8,8 rto:250 rtt:45.214/17.785 ato:40 mss:1448 cwnd:13 bytes_acked:124 bytes_received:4 segs_out:9 segs_in:8 data_segs_out:3 data_segs_in:4 bbr:(bw:285.8
         Kbps,mrtt:40.471,pacing_gain:2.88672,cwnd_gain:2.88672) send 3.3Mbps lastsnd:38760 lastrcv:38580 lastack:38720 pacing_rate 8.5Mbps rcv_space:29200 minrtt:40.471
         
bbr 


ESTAB       0      1342296                                           192.168.2.1:43718                                                        192.168.1.1:5201
         bbr wscale:8,8 rto:250 rtt:48.482/1.647 mss:1448 cwnd:144 ssthresh:42 bytes_acked:162248438 segs_out:112139 segs_in:54915 data_segs_out:112137 bbr:(bw:19.2Mbps,mrtt:40.647,pacing_gain:0.75,cwnd_gain:2) send 34.4Mbps lastrcv:59310 pacing_rate 14.4Mbps unacked:86 rcv_space:29200 notsent:1217768 minrtt:40.524


bbr1 @ 10mbps

ESTAB      0      692144 192.168.2.1:43726              192.168.1.1:5201
         bbr1 wscale:8,8 rto:330 rtt:125.966/0.041 mss:1448 cwnd:104 bytes_acked:5861542 segs_out:4155 segs_in:2122 data_segs_out:4153 bbr:(bw:9.6Mbps,mrtt:40.506,pacing_gain:0.34375,cwnd_gain:2.88672) send 9.6Mbps lastrcv:5090 pacing_rate 3.4Mbps unacked:104 rcv_space:29200 notsent:541552 minrtt:40.506



bbr @ 10

ESTAB      0      726896 192.168.2.1:43730              192.168.1.1:5201
         bbr wscale:8,8 rto:250 rtt:48.731/2.477 mss:1448 cwnd:76 ssthresh:42 bytes_acked:7066278 segs_out:4930 segs_in:2600 data_segs_out:4928 bbr:(bw:9.6Mbps,mrtt:40.482,pacing_gain:0.75,cwnd_gain:2) send 18.1Mbps lastsnd:10 lastrcv:6100 lastack:10 pacing_rate 7.2Mbps unacked:47 rcv_space:29200 notsent:658840 minrtt:40.482

