from binaryninja import Architecture, BinaryViewType, Endianness
from Moxie import *

Moxie.register()
BinaryViewType['ELF'].register_arch(0xdf, Endianness.BigEndian, Architecture["moxie"])

