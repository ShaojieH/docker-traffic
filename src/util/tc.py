import socket
import struct


def get_src_by_filter(output: str):
    start_pos = output.find("match ")
    if start_pos == -1:
        return ""
    start_pos = start_pos + + len("match ")
    end_pos = start_pos + 8
    hex_src_addr = output[start_pos: end_pos]
    return get_ip_by_hex(hex_src_addr)


def get_limit_by_class(output: str):
    start_pos = output.find("parent 1: rate ")
    if start_pos == -1:
        return ""
    start_pos = start_pos + len("parent 1: rate ")
    end_pos = output.find("(bounded,isolated) prio 5") - 1
    limit = output[start_pos: end_pos]
    return limit


def get_ip_by_hex(hex_addr):
    addr_long = int(hex_addr, 16)
    return socket.inet_ntoa(struct.pack(">L", addr_long))


def main():
    print(get_limit_by_class("class cbq 1:1 parent 1: rate 5Mbit (bounded,isolated) prio 5"))


if __name__ == '__main__':
    main()
