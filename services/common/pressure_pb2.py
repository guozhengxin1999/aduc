# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pressure.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0epressure.proto\x12\x08pressure\"+\n\x05Input\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0cpressureData\x18\x02 \x03(\x02\"N\n\x06Output\x12\x14\n\x0cpressureData\x18\x01 \x03(\x02\x12\x1b\n\x13hasDetectedPressure\x18\x02 \x01(\x08\x12\x11\n\thasThreat\x18\x03 \x01(\x08\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pressure_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INPUT._serialized_start=28
  _INPUT._serialized_end=71
  _OUTPUT._serialized_start=73
  _OUTPUT._serialized_end=151
# @@protoc_insertion_point(module_scope)
