def parse_dtc(_bytes):
    """ converts 2 bytes into a DTC code """

    # check validity (also ignores padding that the ELM returns)
    if (len(_bytes) != 2) or (_bytes == (0,0)):
        return None

    # BYTES: (16,      35      )
    # HEX:    4   1    2   3
    # BIN:    01000001 00100011
    #         [][][  in hex   ]
    #         | / /
    # DTC:    C0123

    dtc  = ['P', 'C', 'B', 'U'][ _bytes[0] >> 6 ] # the last 2 bits of the first byte
    dtc += str( (_bytes[0] >> 4) & 0b0011 ) # the next pair of 2 bits. Mask off the bits we read above
    dtc += bytes_to_hex(_bytes)[1:4]

    # pull a description if we have one
    ##return (dtc, DTC.get(dtc, ""))
    return dtc

def dtc(data):
    """ converts a frame of 2-byte DTCs into a list of DTCs """
    codes = []
    d = []
   
    d += data[2:] # remove the mode and DTC_count bytes

    # look at data in pairs of bytes
    # looping through ENDING indices to avoid odd (invalid) code lengths
    for n in range(1, len(d), 2):

        # parse the code
        dtc = parse_dtc( (d[n-1], d[n]) )

        if dtc is not None:
            codes.append(dtc)

    return codes


print(str(dtc(43020251046043010890)))