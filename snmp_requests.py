from pysnmp.hlapi import *


def snmp_get(community, host, oid):
    result = None

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, 161), timeout=2.0, retries=0),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        return None
    elif errorStatus:
        return None
    else:
        for varBind in varBinds:
            varB = (' = '.join([x.prettyPrint() for x in varBind]))
            result = varB.split()[2]
    return result
