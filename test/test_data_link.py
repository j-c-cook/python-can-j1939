import unittest

import pytest
from j1939 import PDU, PDUDict
from typing import Dict


def address_claim_id_pdu_dict() -> Dict:
    # null address claim id
    values: dict = {
        'priority': 0x6,
        'extended_data_page': 0x0,
        'data_page': 0x0,
        'pdu_format': 0xee,
        'pdu_specific': 0xff,
        'source_address': 0xfe
    }
    return values


def address_claim_id_pdu_field() -> PDUDict:
    _pdu_dict: PDUDict = address_claim_id_pdu_dict()
    return PDUDict(_pdu_dict)


def address_claim_id_pdu_by_dict() -> PDU:
    _pdu_dict: PDUDict = address_claim_id_pdu_field()
    return PDU(_pdu_dict)


def address_claim_id_pdu_by_frame_id() -> PDU:
    _frame_id: int = 0x18eefffe
    return PDU(_frame_id)


class TestDataLink(unittest.TestCase):

    def setUp(self) -> None:
        return

    def test_1(self):
        pdu: PDUDict = address_claim_id_pdu_field()

        assert pdu['priority'] == 0x6
        assert pdu['extended_data_page'] == 0x0
        assert pdu['data_page'] == 0x0
        assert pdu['pdu_format'] == 0xee
        assert pdu['pdu_specific'] == 0xff
        assert pdu['source_address'] == 0xfe

        pdu['new_field'] = 0x0

        with pytest.raises(Exception):
            pdu.has_proper_field_names()

    def test_2(self):
        pdu: PDU = address_claim_id_pdu_by_dict()

        assert pdu.priority == 0x6
        assert pdu.extended_data_page == 0x0
        assert pdu.data_page == 0x0
        assert pdu.pdu_format == 0xee
        assert pdu.pdu_specific == 0xff
        assert pdu.source_address == 0xfe

    def test_3(self):
        pdu: PDU = address_claim_id_pdu_by_frame_id()

        assert pdu.priority == 0x6
        assert pdu.extended_data_page == 0x0
        assert pdu.data_page == 0x0
        assert pdu.pdu_format == 0xee
        assert pdu.pdu_specific == 0xff
        assert pdu.source_address == 0xfe
