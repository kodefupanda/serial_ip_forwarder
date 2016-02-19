# serial_ip_forwarder
Forwards Serial Data to an IP address

(C) 2016 Mark Bristow <mark.bristow@gmail.com>
Inspired by Chris Liechti <cliechti@gmx.net> script found here:
https://github.com/pyserial/pyserial/blob/master/examples/tcp_serial_redirect.py

Software is provided "as-is".  No warranty is implied and functionality is not gaurenteed.
In fact if it works at all and dosn't wipe your system, consider yourself luckey.

SPDX-License-Identifier:	BSD-3-Clause

BE SURE YOU INSTALL PYSERIAL 'sudo apt-get install python-serial'

usage: serial_forwarder.py [-h] [-q] [-t TIMEOUT] [--parity {N,E,O,S,M}]
							[--rtscts] [--xonxoff] [--rts RTS] [--dtr DTR]
							[-P REMOTEPORT]
							HOSTNAME SERIALPORT [BAUDRATE]

positional arguments:
  HOSTNAME              remote processing host IP or Hostname
  SERIALPORT            serial port name
  BAUDRATE              set baud rate, default: 9600

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           suppress non error messages

serial port:
  -t TIMEOUT, --timeout TIMEOUT
                        serial port readline timeout
  --parity {N,E,O,S,M}  set parity, one of {N E O S M}, default: N
  --rtscts              enable RTS/CTS flow control (default off)
  --xonxoff             enable software flow control (default off)
  --rts RTS             set initial RTS line state (possible values: 0, 1)
  --dtr DTR             set initial DTR line state (possible values: 0, 1)

network forwarding settings:
  -P REMOTEPORT, --remoteport REMOTEPORT
                        remote TCP port
