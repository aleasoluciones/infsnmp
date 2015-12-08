# -*- coding: utf-8 -*-

import unittest

from hamcrest import *

from pysnmp.proto import rfc1902

from infsnmp import types, clients, exceptions

def snmp_string(value):
    return types.PySnmpValue(types.PySnmpTypes().octect_string(value))

def snmp_integer(value):
    return types.PySnmpValue(types.PySnmpTypes().integer(value))


def snmp_octect_string(value):
    return types.PySnmpValue(types.PySnmpTypes().octect_string(value))


class SnmpClientTest(unittest.TestCase):

    def setUp(self):
        self.snmp_client = clients.PySnmpClient()
        self.community = 'public'
        self.host = '127.0.0.1'
        self.port = 1161

    def test_get_several_oids(self):
        oid1 = '1.3.6.1.2.1.1.4.0'
        oid2 = '1.3.6.1.2.1.1.6.0'

        result = self.snmp_client.get(
            self.host, self.community, [oid1, oid2], port=self.port)

        assert_that(
            result, equal_to([(oid1, snmp_string("infsnmptests <infsnmptests@example.org>")),
                              (oid2, snmp_string("infsnmptests"))]))

    def test_walk(self):
        oid = '1.3.6.1.2.1.1.9.1.3'
        oid1 = '1.3.6.1.2.1.1.9.1.3.4'

        result = self.snmp_client.walk(
            self.host, self.community, oid, port=self.port)

        assert_that(result, has_length(10))
        assert_that(result, has_item((oid1, snmp_string("The MIB module for SNMPv2 entities"))))

    def test_bulk_walk(self):
        oid = '1.3.6.1.2.1.1.9.1.3'
        oid1 = '1.3.6.1.2.1.1.9.1.3.4'

        result = self.snmp_client.bulk_walk(
            self.host, self.community, oid, port=self.port)

        assert_that(result, has_length(10))
        assert_that(result, has_item((oid1, snmp_string("The MIB module for SNMPv2 entities"))))

    def test_get_with_timeout(self):
        self.assertRaises(exceptions.SNMPExceptionError, self.snmp_client.get,
                          '127.0.0.1', 'incorrect-community', ['1.1'], port=self.port, timeout=1)

    def test_get_unknown_oid(self):
        unknown_oid = '1.2'

        result = self.snmp_client.get(
            self.host, self.community, [unknown_oid], port=self.port)

        value = result[0][1]
        assert_that(value.exists(), is_(False))

    def test_walk_unknown_oid(self):
        unknown_oid = '1.2'

        result = self.snmp_client.walk(
            self.host, self.community, unknown_oid, port=self.port)

        assert_that(result, has_length(0))

    def test_set(self):
        oid_1 = '1.3.6.1.2.1.1.5.0'
        value_1 = snmp_octect_string('irrelevant_value1').value()
        snmp_set_values = ((oid_1, value_1), )
        community = 'rwcommunity'

        self.snmp_client.set(
            self.host, community, snmp_set_values, port=self.port, timeout=1)

        result = self.snmp_client.get(
            self.host, community, [oid_1], port=self.port, timeout=1)

        assert_that(
            result, equal_to([(oid_1, snmp_string("irrelevant_value1"))]))

    def test_set_with_timeout(self):
        oid_1 = '1.3.6.1.2.1.1.5.0'
        value_1 = rfc1902.OctetString('hola')

        self.assertRaises(exceptions.SNMPExceptionError, self.snmp_client.set,
                          '127.0.0.1', 'incorrect-community', ((oid_1, value_1),), port=self.port)
