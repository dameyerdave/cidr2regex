#!/usr/bin/python
''' Not my script, found on the Internet, and rediscovered on my hard drive
'''
from __future__ import division
from __future__ import print_function
import sys

def cidr_to_regex(cidr):
    ip, prefix = cidr.split('/')

    base = 0
    for val in map(int, ip.split('.')):
        base = (base << 8) | val

    shift = 32 - int(prefix)
    start = base >> shift << shift
    end = start | (1 << shift) - 1

    def regex(lower, upper):
        if lower == upper:
            return str(lower)

        from math import log10
        exp = int(log10(upper - lower))
        if (int(str(lower)[-1]) > int(str(upper)[-1]) and exp == 0):
            # increasing exp due to base 10 wrap to next exp"
            exp += 1
        delta = 10 ** exp

        if lower == 0 and upper == 255:
            return "\d+"

        if delta == 1:
            val = ""
            for a, b in zip(str(lower), str(upper)):
                if a == b:
                    val += str(a)
                elif (a, b) == ("0", "9"):
                    val += '\d'
                elif int(b) - int(a) == 1:
                    val += '[%s%s]' % (a, b)
                else:
                    val += '[%s-%s]' % (a, b)
            return val

        def gen_classes():
            floor_ = lambda x: int(round(x // delta, 0) * delta)

            xs = range(floor_(upper) - delta, floor_(lower), -delta)
            for x in map(str, xs):
                yield '%s%s' % (x[:-exp], r'\d' * exp)

            yield regex(lower, floor_(lower) + (delta - 1))
            yield regex(floor_(upper), upper)

        return "({})".format('|'.join(gen_classes()))

    def get_parts():
        for x in range(24, -1, -8):
            yield regex(start >> x & 255, end >> x & 255)

    return '%s$' % r'.'.join(get_parts())

for line in sys.stdin.readlines():
	print(cidr_to_regex( line ))

