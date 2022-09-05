#
# Autogenerated by Thrift Compiler (0.14.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class EndPoint(object):
    """
    Attributes:
     - ip
     - port

    """


    def __init__(self, ip=None, port=None,):
        self.ip = ip
        self.port = port

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.ip = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.port = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('EndPoint')
        if self.ip is not None:
            oprot.writeFieldBegin('ip', TType.STRING, 1)
            oprot.writeString(self.ip.encode('utf-8') if sys.version_info[0] == 2 else self.ip)
            oprot.writeFieldEnd()
        if self.port is not None:
            oprot.writeFieldBegin('port', TType.I32, 2)
            oprot.writeI32(self.port)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.ip is None:
            raise TProtocolException(message='Required field ip is unset!')
        if self.port is None:
            raise TProtocolException(message='Required field port is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TSStatus(object):
    """
    Attributes:
     - code
     - message
     - subStatus
     - redirectNode

    """


    def __init__(self, code=None, message=None, subStatus=None, redirectNode=None,):
        self.code = code
        self.message = message
        self.subStatus = subStatus
        self.redirectNode = redirectNode

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    self.code = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.message = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.LIST:
                    self.subStatus = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = TSStatus()
                        _elem5.read(iprot)
                        self.subStatus.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRUCT:
                    self.redirectNode = EndPoint()
                    self.redirectNode.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TSStatus')
        if self.code is not None:
            oprot.writeFieldBegin('code', TType.I32, 1)
            oprot.writeI32(self.code)
            oprot.writeFieldEnd()
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 2)
            oprot.writeString(self.message.encode('utf-8') if sys.version_info[0] == 2 else self.message)
            oprot.writeFieldEnd()
        if self.subStatus is not None:
            oprot.writeFieldBegin('subStatus', TType.LIST, 3)
            oprot.writeListBegin(TType.STRUCT, len(self.subStatus))
            for iter6 in self.subStatus:
                iter6.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.redirectNode is not None:
            oprot.writeFieldBegin('redirectNode', TType.STRUCT, 4)
            self.redirectNode.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.code is None:
            raise TProtocolException(message='Required field code is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TSOpenSessionResp(object):
    """
    Attributes:
     - status
     - sessionId
     - configuration

    """


    def __init__(self, status=None, sessionId=None, configuration=None,):
        self.status = status
        self.sessionId = sessionId
        self.configuration = configuration

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.status = TSStatus()
                    self.status.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.sessionId = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.MAP:
                    self.configuration = {}
                    (_ktype8, _vtype9, _size7) = iprot.readMapBegin()
                    for _i11 in range(_size7):
                        _key12 = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                        _val13 = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                        self.configuration[_key12] = _val13
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TSOpenSessionResp')
        if self.status is not None:
            oprot.writeFieldBegin('status', TType.STRUCT, 1)
            self.status.write(oprot)
            oprot.writeFieldEnd()
        if self.sessionId is not None:
            oprot.writeFieldBegin('sessionId', TType.I64, 2)
            oprot.writeI64(self.sessionId)
            oprot.writeFieldEnd()
        if self.configuration is not None:
            oprot.writeFieldBegin('configuration', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.configuration))
            for kiter14, viter15 in self.configuration.items():
                oprot.writeString(kiter14.encode('utf-8') if sys.version_info[0] == 2 else kiter14)
                oprot.writeString(viter15.encode('utf-8') if sys.version_info[0] == 2 else viter15)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.status is None:
            raise TProtocolException(message='Required field status is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TSOpenSessionReq(object):
    """
    Attributes:
     - zoneId
     - username
     - password
     - configuration

    """


    def __init__(self, zoneId=None, username=None, password=None, configuration=None,):
        self.zoneId = zoneId
        self.username = username
        self.password = password
        self.configuration = configuration

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 2:
                if ftype == TType.STRING:
                    self.zoneId = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.username = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.password = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.MAP:
                    self.configuration = {}
                    (_ktype17, _vtype18, _size16) = iprot.readMapBegin()
                    for _i20 in range(_size16):
                        _key21 = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                        _val22 = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                        self.configuration[_key21] = _val22
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TSOpenSessionReq')
        if self.zoneId is not None:
            oprot.writeFieldBegin('zoneId', TType.STRING, 2)
            oprot.writeString(self.zoneId.encode('utf-8') if sys.version_info[0] == 2 else self.zoneId)
            oprot.writeFieldEnd()
        if self.username is not None:
            oprot.writeFieldBegin('username', TType.STRING, 3)
            oprot.writeString(self.username.encode('utf-8') if sys.version_info[0] == 2 else self.username)
            oprot.writeFieldEnd()
        if self.password is not None:
            oprot.writeFieldBegin('password', TType.STRING, 4)
            oprot.writeString(self.password.encode('utf-8') if sys.version_info[0] == 2 else self.password)
            oprot.writeFieldEnd()
        if self.configuration is not None:
            oprot.writeFieldBegin('configuration', TType.MAP, 5)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.configuration))
            for kiter23, viter24 in self.configuration.items():
                oprot.writeString(kiter23.encode('utf-8') if sys.version_info[0] == 2 else kiter23)
                oprot.writeString(viter24.encode('utf-8') if sys.version_info[0] == 2 else viter24)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.zoneId is None:
            raise TProtocolException(message='Required field zoneId is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TSCloseSessionReq(object):
    """
    Attributes:
     - sessionId

    """


    def __init__(self, sessionId=None,):
        self.sessionId = sessionId

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.sessionId = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TSCloseSessionReq')
        if self.sessionId is not None:
            oprot.writeFieldBegin('sessionId', TType.I64, 1)
            oprot.writeI64(self.sessionId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.sessionId is None:
            raise TProtocolException(message='Required field sessionId is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TSWritePointsReq(object):
    """
    Attributes:
     - sessionId
     - database
     - retentionPolicy
     - precision
     - consistency
     - lineProtocol

    """


    def __init__(self, sessionId=None, database=None, retentionPolicy=None, precision=None, consistency=None, lineProtocol=None,):
        self.sessionId = sessionId
        self.database = database
        self.retentionPolicy = retentionPolicy
        self.precision = precision
        self.consistency = consistency
        self.lineProtocol = lineProtocol

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.sessionId = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.database = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.retentionPolicy = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.precision = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.consistency = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.lineProtocol = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TSWritePointsReq')
        if self.sessionId is not None:
            oprot.writeFieldBegin('sessionId', TType.I64, 1)
            oprot.writeI64(self.sessionId)
            oprot.writeFieldEnd()
        if self.database is not None:
            oprot.writeFieldBegin('database', TType.STRING, 2)
            oprot.writeString(self.database.encode('utf-8') if sys.version_info[0] == 2 else self.database)
            oprot.writeFieldEnd()
        if self.retentionPolicy is not None:
            oprot.writeFieldBegin('retentionPolicy', TType.STRING, 3)
            oprot.writeString(self.retentionPolicy.encode('utf-8') if sys.version_info[0] == 2 else self.retentionPolicy)
            oprot.writeFieldEnd()
        if self.precision is not None:
            oprot.writeFieldBegin('precision', TType.STRING, 4)
            oprot.writeString(self.precision.encode('utf-8') if sys.version_info[0] == 2 else self.precision)
            oprot.writeFieldEnd()
        if self.consistency is not None:
            oprot.writeFieldBegin('consistency', TType.STRING, 5)
            oprot.writeString(self.consistency.encode('utf-8') if sys.version_info[0] == 2 else self.consistency)
            oprot.writeFieldEnd()
        if self.lineProtocol is not None:
            oprot.writeFieldBegin('lineProtocol', TType.STRING, 6)
            oprot.writeString(self.lineProtocol.encode('utf-8') if sys.version_info[0] == 2 else self.lineProtocol)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.sessionId is None:
            raise TProtocolException(message='Required field sessionId is unset!')
        if self.database is None:
            raise TProtocolException(message='Required field database is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class TSCreateDatabaseReq(object):
    """
    Attributes:
     - sessionId
     - database

    """


    def __init__(self, sessionId=None, database=None,):
        self.sessionId = sessionId
        self.database = database

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.sessionId = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.database = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TSCreateDatabaseReq')
        if self.sessionId is not None:
            oprot.writeFieldBegin('sessionId', TType.I64, 1)
            oprot.writeI64(self.sessionId)
            oprot.writeFieldEnd()
        if self.database is not None:
            oprot.writeFieldBegin('database', TType.STRING, 2)
            oprot.writeString(self.database.encode('utf-8') if sys.version_info[0] == 2 else self.database)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.sessionId is None:
            raise TProtocolException(message='Required field sessionId is unset!')
        if self.database is None:
            raise TProtocolException(message='Required field database is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(EndPoint)
EndPoint.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'ip', 'UTF8', None, ),  # 1
    (2, TType.I32, 'port', None, None, ),  # 2
)
all_structs.append(TSStatus)
TSStatus.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'code', None, None, ),  # 1
    (2, TType.STRING, 'message', 'UTF8', None, ),  # 2
    (3, TType.LIST, 'subStatus', (TType.STRUCT, [TSStatus, None], False), None, ),  # 3
    (4, TType.STRUCT, 'redirectNode', [EndPoint, None], None, ),  # 4
)
all_structs.append(TSOpenSessionResp)
TSOpenSessionResp.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'status', [TSStatus, None], None, ),  # 1
    (2, TType.I64, 'sessionId', None, None, ),  # 2
    (3, TType.MAP, 'configuration', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 3
)
all_structs.append(TSOpenSessionReq)
TSOpenSessionReq.thrift_spec = (
    None,  # 0
    None,  # 1
    (2, TType.STRING, 'zoneId', 'UTF8', None, ),  # 2
    (3, TType.STRING, 'username', 'UTF8', None, ),  # 3
    (4, TType.STRING, 'password', 'UTF8', None, ),  # 4
    (5, TType.MAP, 'configuration', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 5
)
all_structs.append(TSCloseSessionReq)
TSCloseSessionReq.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'sessionId', None, None, ),  # 1
)
all_structs.append(TSWritePointsReq)
TSWritePointsReq.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'sessionId', None, None, ),  # 1
    (2, TType.STRING, 'database', 'UTF8', None, ),  # 2
    (3, TType.STRING, 'retentionPolicy', 'UTF8', None, ),  # 3
    (4, TType.STRING, 'precision', 'UTF8', None, ),  # 4
    (5, TType.STRING, 'consistency', 'UTF8', None, ),  # 5
    (6, TType.STRING, 'lineProtocol', 'UTF8', None, ),  # 6
)
all_structs.append(TSCreateDatabaseReq)
TSCreateDatabaseReq.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'sessionId', None, None, ),  # 1
    (2, TType.STRING, 'database', 'UTF8', None, ),  # 2
)
fix_spec(all_structs)
del all_structs
