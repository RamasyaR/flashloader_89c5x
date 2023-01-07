from pydantic import BaseModel

from flashloader.constants import ProgVoltages, SupportedMCU


class InfoMessage(BaseModel):
    mcu: SupportedMCU
    prog_voltage_type: ProgVoltages
    non_blank_bytes: int
    byte_cursor: int


class PGMMessage(BaseModel):
    mcu_postfix: int
    non_blank_bytes: int
    byte_cursor: int
