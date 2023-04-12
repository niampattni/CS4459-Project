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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchatRPC.proto\"\x07\n\x05\x45mpty\";\n\x0fMessageResponse\x12\x0c\n\x04\x66rom\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x03 \x01(\t\"5\n\x0fRegisterRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"%\n\rLogoutRequest\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\"Q\n\x12\x43hannelPostRequest\x12\x14\n\x0c\x63hannel_name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x03 \x01(\t\"P\n\x14\x44irectMessageRequest\x12\x11\n\trecipient\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x03 \x01(\t\":\n\x0cWatchRequest\x12\x14\n\x0c\x63hannel_name\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t\"<\n\x0eUnwatchRequest\x12\x14\n\x0c\x63hannel_name\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t\":\n\x0c\x42lockRequest\x12\x14\n\x0c\x62locked_user\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t\"<\n\x0eUnblockRequest\x12\x14\n\x0c\x62locked_user\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t\"(\n\x08Response\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x08\x32\xa3\x03\n\x0b\x43hatService\x12+\n\x0cRegisterUser\x12\x10.RegisterRequest\x1a\t.Response\x12!\n\x05Login\x12\r.LoginRequest\x1a\t.Response\x12#\n\x06Logout\x12\x0e.LogoutRequest\x1a\t.Response\x12-\n\x0b\x43hannelPost\x12\x13.ChannelPostRequest\x1a\t.Response\x12\x31\n\rDirectMessage\x12\x15.DirectMessageRequest\x1a\t.Response\x12!\n\x05Watch\x12\r.WatchRequest\x1a\t.Response\x12%\n\x07Unwatch\x12\x0f.UnwatchRequest\x1a\t.Response\x12!\n\x05\x42lock\x12\r.BlockRequest\x1a\t.Response\x12%\n\x07Unblock\x12\x0f.UnblockRequest\x1a\t.Response\x12)\n\rMessageStream\x12\x06.Empty\x1a\x10.MessageResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chatRPC_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=17
  _EMPTY._serialized_end=24
  _MESSAGERESPONSE._serialized_start=26
  _MESSAGERESPONSE._serialized_end=85
  _REGISTERREQUEST._serialized_start=87
  _REGISTERREQUEST._serialized_end=140
  _LOGINREQUEST._serialized_start=142
  _LOGINREQUEST._serialized_end=192
  _LOGOUTREQUEST._serialized_start=194
  _LOGOUTREQUEST._serialized_end=231
  _CHANNELPOSTREQUEST._serialized_start=233
  _CHANNELPOSTREQUEST._serialized_end=314
  _DIRECTMESSAGEREQUEST._serialized_start=316
  _DIRECTMESSAGEREQUEST._serialized_end=396
  _WATCHREQUEST._serialized_start=398
  _WATCHREQUEST._serialized_end=456
  _UNWATCHREQUEST._serialized_start=458
  _UNWATCHREQUEST._serialized_end=518
  _BLOCKREQUEST._serialized_start=520
  _BLOCKREQUEST._serialized_end=578
  _UNBLOCKREQUEST._serialized_start=580
  _UNBLOCKREQUEST._serialized_end=640
  _RESPONSE._serialized_start=642
  _RESPONSE._serialized_end=682
  _CHATSERVICE._serialized_start=685
  _CHATSERVICE._serialized_end=1104
# @@protoc_insertion_point(module_scope)
