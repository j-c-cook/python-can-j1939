from collections import OrderedDict
from math import log2
from typing import Union

null_addr = 0xfe
global_addr = 0xff

_fields: OrderedDict = OrderedDict([
    ('source_address', 0xff),
    ('pdu_specific', 0xff),
    ('pdu_format', 0xff),
    ('data_page', 0x1),
    ('extended_data_page', 0x1),
    ('priority', 0x7)
])


class PDUDict(dict):

    field_names = list(_fields.keys())

    def __init__(self, pdu_dict: dict = None):
        super().__init__()
        for field_name in PDUDict.field_names:
            if pdu_dict is None:
                super().__setitem__(field_name, 0x0)
            else:
                super().__setitem__(field_name, pdu_dict[field_name])

        self.has_proper_field_names()

    def has_proper_field_names(self):
        assert [address for address in self] == PDUDict.field_names, \
            "The keys are strictly limited to the field_names"


class _Field(object):

    def __init__(self):
        pass

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

        self.mask, self.shift = self._get_shift_and_mask(self.public_name)

    def __get__(self, instance, owner):
        return (instance.frame_id >> self.shift) & self.mask

    def __set__(self, instance, value):
        instance.frame_id &= ~(self.mask << self.shift)
        instance.frame_id |= (value & self.mask) << self.shift

    @staticmethod
    def _get_shift_and_mask(name):
        shift = 0
        for key in _fields:
            if key == name:
                break
            _mask = _fields[key]
            b = log2(_mask + 1)
            shift += int(b)

        mask = _fields[name]

        return mask, shift


class _BasePDU(object):

    priority = _Field()
    extended_data_page = _Field()
    data_page = _Field()
    pdu_format = _Field()
    pdu_specific = _Field()
    source_address = _Field()

    def __init__(self, frame_id):
        self.frame_id = frame_id

    def __repr__(self):
        return f'frame id: {hex(self.frame_id)} ' \
               f'PDU format: {self.format} ' \
               f'PGN: {hex(self.pgn)}'

    @property
    def format(self):
        if 0 <= self.pdu_format <= 239:
            return 1
        elif 239 < self.pdu_format <= 255:
            return 2
        else:
            raise ValueError("The PDU format field acceptable range is 0-255.")

    @property
    def pgn(self):
        _pgn = (self.data_page << 16) | (self.pdu_format << 8)
        if self.format == 2:
            _pgn |= self.pdu_specific
        return _pgn


class PDU(_BasePDU):
    def __init__(self, frame_id_or_pdu_dict: Union[int, dict, PDUDict] = None):
        if type(frame_id_or_pdu_dict) not in \
                [int, dict, PDUDict, type(None)]:
            raise ValueError("The field frame_id_or_pdu_dict must be of type"
                             "integer or PDUDict.")

        if isinstance(frame_id_or_pdu_dict, int):
            super().__init__(frame_id_or_pdu_dict)
        elif isinstance(frame_id_or_pdu_dict, type(None)):
            super().__init__(0)
        else:
            super().__init__(0)

            if type(frame_id_or_pdu_dict) == dict:
                frame_id_or_pdu_dict: PDUDict = PDUDict(frame_id_or_pdu_dict)

            frame_id_or_pdu_dict.has_proper_field_names()
            for field in frame_id_or_pdu_dict:
                self.__setattr__(field, frame_id_or_pdu_dict[field])
