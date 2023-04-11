# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chatRPC.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatRPC.proto\x12\x04main\"5\n\x0fRegisterRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"M\n\x12\x43hannelPostRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0c\x63hannel_name\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"J\n\x14\x44irectMessageRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x11\n\trecipient\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"6\n\x0cWatchRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0c\x63hannel_name\x18\x02 \x01(\t\"8\n\x0eUnwatchRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0c\x63hannel_name\x18\x02 \x01(\t\"6\n\x0c\x42lockRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0c\x62locked_user\x18\x02 \x01(\t\"8\n\x0eUnblockRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0c\x62locked_user\x18\x02 \x01(\t\"(\n\x08Response\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x08\x32\xa3\x03\n\x0b\x43hatService\x12\x35\n\x0cRegisterUser\x12\x15.main.RegisterRequest\x1a\x0e.main.Response\x12\x37\n\x0b\x43hannelPost\x12\x18.main.ChannelPostRequest\x1a\x0e.main.Response\x12;\n\rDirectMessage\x12\x1a.main.DirectMessageRequest\x1a\x0e.main.Response\x12+\n\x05Login\x12\x12.main.LoginRequest\x1a\x0e.main.Response\x12+\n\x05Watch\x12\x12.main.WatchRequest\x1a\x0e.main.Response\x12/\n\x07Unwatch\x12\x14.main.UnblockRequest\x1a\x0e.main.Response\x12+\n\x05\x42lock\x12\x12.main.BlockRequest\x1a\x0e.main.Response\x12/\n\x07Unblock\x12\x14.main.UnblockRequest\x1a\x0e.main.Responseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatRPC_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTERREQUEST._serialized_start=23
  _REGISTERREQUEST._serialized_end=76
  _CHANNELPOSTREQUEST._serialized_start=78
  _CHANNELPOSTREQUEST._serialized_end=155
  _DIRECTMESSAGEREQUEST._serialized_start=157
  _DIRECTMESSAGEREQUEST._serialized_end=231
  _LOGINREQUEST._serialized_start=233
  _LOGINREQUEST._serialized_end=283
  _WATCHREQUEST._serialized_start=285
  _WATCHREQUEST._serialized_end=339
  _UNWATCHREQUEST._serialized_start=341
  _UNWATCHREQUEST._serialized_end=397
  _BLOCKREQUEST._serialized_start=399
  _BLOCKREQUEST._serialized_end=453
  _UNBLOCKREQUEST._serialized_start=455
  _UNBLOCKREQUEST._serialized_end=511
  _RESPONSE._serialized_start=513
  _RESPONSE._serialized_end=553
  _CHATSERVICE._serialized_start=556
  _CHATSERVICE._serialized_end=975
# @@protoc_insertion_point(module_scope)
