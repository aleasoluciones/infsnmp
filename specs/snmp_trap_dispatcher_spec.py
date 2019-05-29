from mamba import describe, context, it
from expects import expect, equal
from doublex import Spy

from infsnmp.traps import PySnmpTrapDispatcher
from pysnmp.proto import api


PROTO_MODULE = api.protoModules[api.protoVersion2c]


with describe('PySnmpTrapDispatcher Spec'):
    with context('FEATURE: is snmp trap OID'):
        with context('having a trap oid'):
            with it('returs true'):
                an_str_oid = '1.3.6.1.6.3.1.1.4.1.0'
                request_pdu = _build_request_pdu(an_str_oid)
                an_oid = _get_oid_from_request_pdu(request_pdu)

                trap_hander = Spy()
                address = Spy()
                port = Spy()
                clock = Spy()
                pysnmp_trap_dispatcher = PySnmpTrapDispatcher(trap_hander, address, port, clock)

                is_snmp_trap_oid = pysnmp_trap_dispatcher.is_snmp_trap_oid(an_oid)

                expect(is_snmp_trap_oid).to(equal(True))

        with context('having a NON trap oid'):
            with it('returs false'):
                an_str_oid = '1.2.3.4.5.6.7'
                request_pdu = _build_request_pdu(an_str_oid)
                an_oid = _get_oid_from_request_pdu(request_pdu)

                trap_hander = Spy()
                address = Spy()
                port = Spy()
                clock = Spy()
                pysnmp_trap_dispatcher = PySnmpTrapDispatcher(trap_hander, address, port, clock)

                is_snmp_trap_oid = pysnmp_trap_dispatcher.is_snmp_trap_oid(an_oid)

                expect(is_snmp_trap_oid).to(equal(False))

def _build_request_pdu(str_oid):
    request_pdu = PROTO_MODULE.GetRequestPDU()
    PROTO_MODULE.apiPDU.setDefaults(request_pdu)
    PROTO_MODULE.apiPDU.setVarBinds(
        request_pdu, ((str_oid, PROTO_MODULE.Null('')),
                        )
    )
    return request_pdu

def _get_oid_from_request_pdu(request_pdu):
    for oid, val in PROTO_MODULE.apiPDU.getVarBindList(request_pdu):
        return oid
