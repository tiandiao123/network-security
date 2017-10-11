from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
from ..PEEPPacket import PEEPPacket
import time
class PEEPTransport(StackingTransport):

    MAXBYTE = 10

    def __init__(self, transport, protocol=None):
        super().__init__(transport)
        self.protocol = protocol

    def write(self, data):
        if self.protocol:
            print("PEEPTransport: Write got {} bytes of data to package".format(len(data)))
            # Currently no chunking
            i = 0
            index = 0
            while (i < len(data)):
                sentData = None
                if (i + self.MAXBYTE < len(data)):
                    sentData = data[i: i + self.MAXBYTE]
                else:
                    sentData = data[i:]
                i += self.MAXBYTE
                pkt = PEEPPacket.makeDataPacket(self.protocol.raisedSeqNum(len(sentData)), sentData)
                index += 1
                if index <= self.protocol.WINDOW_SIZE:
                    print("sending {!r} packet, sequence number: {!r}".format(index, pkt.SequenceNumber))
                    self.protocol.sentDataCache[pkt.SequenceNumber] = (pkt, time.time())
                    super().write(pkt.__serialize__())
                else: 
                    print("caching {!r} packet, sequence number: {!r}".format(index, pkt.SequenceNumber))
                    self.protocol.readyDataCache.append((pkt.SequenceNumber, pkt))
            print("PEEPTransport: data transmitting finished, number of packets sent: {!r}".format(index))
        
        else:
            print("PEEPTransport: Undefined protocol, writing anyway...")
            print("PEEPTransport: Write got {} bytes of data to pass to lower layer".format(len(data)))
            super().write(data)
            