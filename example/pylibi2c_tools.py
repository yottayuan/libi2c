# -*- coding: utf-8 -*-
import six
import sys
import ctypes
import argparse
import pylibi2c


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bus', help='i2c bus, such as 1', type=int, required=True)
    parser.add_argument('-d', '--dev_addr', help='i2c device address', type=str, required=True)
    parser.add_argument('-i', '--iaddr', help='i2c internal address', type=str, default="0x0")
    parser.add_argument('-l', '--iaddr_bytes', help='i2c internal address bytes', type=int, default=1)
    parser.add_argument('-w', '--write', help='defualt is read, with -w read', type=bool, default=False)
    parser.add_argument('-s', '--size', help='read / write size', type=int, default=1)
    parser.add_argument('--data', help='write data start', type=int, default=0x0)
    parser.add_argument('--delay', help='i2c r/w delay, unit is msec', type=int, default=5)
    parser.add_argument('--ioctl', help='using ioctl r/w i2c', type=bool, default=False)
    args = vars(parser.parse_args())

    # Args parser
    bus = args.get('bus')
    size = args.get('size')
    data = args.get('data')
    ioctl = args.get('ioctl')
    write = args.get('write')
    delay = args.get('delay')
    iaddr = int(args.get('iaddr'), 16)
    iaddr_bytes = args.get('iaddr_bytes')
    dev_addr = int(args.get('dev_addr'), 16)

    # Open i2c bus
    bus = pylibi2c.open('/dev/i2c-{}'.format(bus))
    if bus == -1:
        print("Open i2c bus:{0:d} error!".format(bus))
        sys.exit(-1)

    # Create read / write buffer
    buf = ctypes.create_string_buffer(size)

    # Set device info
    device = {"bus": bus, "addr": dev_addr, "delay": delay, "iaddr_bytes": iaddr_bytes}

    # Ioctl r /w
    if ioctl:
        read_handle = pylibi2c.ioctl_read
        write_handle = pylibi2c.ioctl_write
    else:
        read_handle = pylibi2c.read
        write_handle = pylibi2c.write

    # Fill write data
    if write:
        for i in range(size):
            buf[i] = six.int2byte(data & 0xff)
            data += 1

        if write_handle(device, iaddr, buf, size) != size:
            print("Write error!")
            sys.exit(-1)
    else:
        if read_handle(device, iaddr, buf, size) != size:
            print("Read error")
            sys.exit(-1)

    # Print read / write data
    print("Write data:" if write else "Read data:")

    for i in range(0, size):
        if (i % 16 == 0):
            print('')
        six.print_("{0:02x} ".format(ord(buf[i])), end='')
    else:
        print('')

