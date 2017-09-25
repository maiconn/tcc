from pyobd_ffries import decoders

import binascii




data = b'4301'
codes = []
d = []
d += message.data[2:] # remove the mode and DTC_count bytes

# look at data in pairs of bytes
# looping through ENDING indices to avoid odd (invalid) code lengths
for n in range(1, len(d), 2):

    # parse the code
    dtc = parse_dtc( (d[n-1], d[n]) )

    if dtc is not None:
        codes.append(dtc)

return codes