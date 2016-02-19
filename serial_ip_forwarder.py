#!/usr/bin/env python
#
# (C) 2016 Mark Bristow <mark.bristow@gmail.com>
#
# Forwards Serial Data to an IP address
# Inspired by Chris Liechti <cliechti@gmx.net> script found here: 
# https://github.com/pyserial/pyserial/blob/master/examples/tcp_serial_redirect.py
#
# Software is provided "as-is".  No warranty is implied and functionality is not gaurenteed.
# In fact if it works at all and dosn't wipe your system, consider yourself luckey.
#
# SPDX-License-Identifier:	BSD-3-Clause
#
# BE SURE YOU INSTALL PYSERIAL 'sudo apt-get install python-serial'

import sys
import socket
import serial

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(
		description="Simple Serial data forwarder."
	)
	
	parser.add_argument(
			'HOSTNAME',
			help='remote processing host IP or Hostname')
			
	parser.add_argument(
			'SERIALPORT',
			help="serial port name")

	parser.add_argument(
			'BAUDRATE',
			type=int,
			nargs='?',
			help='set baud rate, default: %(default)s',
			default=9600)

	parser.add_argument(
			'-q', '--quiet',
			action='store_true',
			help='suppress non error messages',
			default=False)

	group = parser.add_argument_group('serial port')

	group.add_argument(
			'-t', '--timeout',
			type=float,
			help='serial port readline timeout',
			default=1.5)
			
	group.add_argument(
			"--parity",
			choices=['N', 'E', 'O', 'S', 'M'],
			type=lambda c: c.upper(),
			help="set parity, one of {N E O S M}, default: N",
			default='N')

	group.add_argument(
			'--rtscts',
			action='store_true',
			help='enable RTS/CTS flow control (default off)',
			default=False)

	group.add_argument(
			'--xonxoff',
			action='store_true',
			help='enable software flow control (default off)',
			default=False)

	group.add_argument(
			'--rts',
			type=int,
			help='set initial RTS line state (possible values: 0, 1)',
			default=None)

	group.add_argument(
			'--dtr',
			type=int,
			help='set initial DTR line state (possible values: 0, 1)',
			default=None)

	group = parser.add_argument_group('network forwarding settings')
	
	group.add_argument(
			'-P', '--remoteport',
			type=int,
			help='remote TCP port',
			default=7777)

	args = parser.parse_args()

	# connect to serial port
	ser = serial.serial_for_url(args.SERIALPORT, do_not_open=True)
	ser.baudrate = args.BAUDRATE
	ser.parity = args.parity
	ser.rtscts = args.rtscts
	ser.xonxoff = args.xonxoff
	ser.timeout = args.timeout

	if args.rts is not None:
		ser.rts = args.rts

	if args.dtr is not None:
		ser.dtr = args.dtr

	if not args.quiet:
		sys.stderr.write('---  Serial to TCP/IP redirect ---\n \tSerial: {p.name} {p.baudrate},{p.bytesize},{p.parity},{p.stopbits} \n\tUDP forward: {a.HOSTNAME}:{a.remoteport} \n\n '.format(
				p=ser, a=args))
		sys.stderr.write("--- type Ctrl-C / BREAK to quit\n")

	try:
		ser.open()
	except serial.SerialException as e:
		sys.stderr.write("Could not open serial port {}: {}\n".format(ser.name, e))
		sys.exit(1)

	try:
		while True:
			try:
				lines = ser.readlines() #grab a line from the serial socket
				#while line = ser.read(256)
				
				try:
					if lines:
						data = ""
						for line in lines:
							data += line
							
						if not args.quiet:
							print("FWD: "+ (" ".join("{:02x}".format(ord(c)) for c in data)))
							
						#send data via UDP to remote listner
						sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						sock.sendto(data, (args.HOSTNAME, args.remoteport))
				except socket.error as msg:
					sys.stderr.write('ERROR: %s\n' % msg)
					break
			except socket.error as msg:
				sys.stderr.write('ERROR: %s\n' % msg)
				break
	except KeyboardInterrupt:
		pass

	ser.close()
	sys.stderr.write('\n--- exit ---\n')