from enum import Enum

from parse import *

bandwhich_format_connection = 'connection: <{time}> <{device}>:{device_port} => {dst}:{dst_port} ({protocol}) up/down Bps: {up}/{down} process: "{process}"'
bandwhich_format_remote_address = 'remote_address: <{time}> {address} up/down Bps: {up}/{down} connections: {connections}'


class Traffic_log_type(Enum):
    INVALID = 0
    BANDWHICH_CONNECTION = 1
    BANDWHICH_REMOTE_ADDRESS = 2


def match_bandwhich_output(line):
    if line.startswith('connection'):
        return Traffic_log_type.BANDWHICH_CONNECTION, parse(bandwhich_format_connection, line)
    elif line.startswith('remote_address'):
        return Traffic_log_type.BANDWHICH_REMOTE_ADDRESS, parse(bandwhich_format_remote_address, line)
    else:
        return Traffic_log_type.INVALID, line
