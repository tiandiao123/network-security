import asyncio
import time
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, BUFFER
from playground.network.packet.fieldtypes import NamedPacketType, ComplexFieldType, PacketFields, Uint, StringFieldType, PacketFieldType, ListFieldType
from HTMLParsePacket import HTMLParsePacket
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol

class HTMLParsePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab1b.Cuiqing_Li.MyPacket"
	DEFINITION_VERSION = "1.0"

	FIELDS = [
	("file_name",STRING),
	("num_file",Uint),
	("content",STRING),
	("data",BUFFER)
	]


class ServerProtocol(asyncio.Protocol):
	def __init__(self):
		self.transport = None
		self._deserializer = None

	def connection_made(self,transport):
		client_name = transport.get_extra_info('peername')
		self.transport = transport
		self._deserializer = PacketType.Deserializer()

	def data_received(self, data):
		#print("log first")
		self._deserializer.update(data)
		print("server side: data has been received!")
		for pat in self._deserializer.nextPackets():
			print(pat)

		print("send feed back to client to say: data has been processed")
		self.transport.write("Hi client: data has been processed, good to go!".encode())

	def connection_lost(self,exc):
		self.transport = None


class ClientProtocol(asyncio.Protocol):
	def __init__(self,packet,loop):
		self.packet = packet
		self.loop = loop


	def connection_made(self,transport):
		pybytes = self.packet.__serialize__()
		#print(type(pybytes))
		#print(pybytes)
		transport.write(pybytes)


	def data_received(self, data):
		print("Got feedback from server side: {} ".format(data.decode()))

	def connection_lost(self,exc):
		self.transport = None
		self.loop.stop()




def BasicUnitTest():
	asyncio.set_event_loop(TestLoopEx())
	client = ClientProtocol()
	server = ServerProtocol()