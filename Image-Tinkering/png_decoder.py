import struct, zlib
import numpy as np

def read_chunk(f):
    ''' 
        This is a function that reads the chunks and their type.
        The statement struct.unpack('>I4s', f.read(8)) actually reads the binary data into groups of 8 and then formats it according to '>I4s' to unpack. 
        > - read the data in big endian format
        I - Unsigned integer will be returned (by default the integer is of 4 bytes)
        4s - A single string of 4 bytes will be returned
        Next we read the chunk data by reading the next 'chunk_length' of bytes, the expected CRC and the actual CRC to be compared which indicates if the file is corrupted incase both do not match.
        With the help of zlib.crc32() method, we can compute the checksum for crc32 (Cyclic Redundancy Check) to a particular data. It will give 32-bit integer value as a result by using zlib.crc32() method.
    '''
    # Returns (chunk_type, chunk_data)
    chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
    chunk_data = f.read(chunk_length)
    chunk_expected_crc, = struct.unpack('>I', f.read(4))
    chunk_actual_crc = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
    if chunk_expected_crc != chunk_actual_crc:
        raise Exception('chunk checksum failed')
    return chunk_type, chunk_data

def PaethPredictor(a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        elif pb <= pc:
            return b
        return c

def img(path):

    f = open(path, "rb")

    PngSignature = b'\x89PNG\r\n\x1a\n'
    if f.read(len(PngSignature)) != PngSignature:
        raise Exception("Invalid PNG Signature")

    chunks = []
    while True:
        chunk_type, chunk_data = read_chunk(f)
        chunks.append((chunk_type, chunk_data))
        if chunk_type == b'IEND':
            break

    _, IHDR_data = chunks[0]  # since IHDR is always first chunk
    '''
        B - unsigned char that returns its integer
    '''
    width, height, bitd, colort, compm, filterm, interlacem = struct.unpack('>IIBBBBB', IHDR_data)
    if compm != 0:
        raise Exception('invalid compression method')
    if filterm != 0:
        raise Exception('invalid filter method')
    if colort != 6:
        raise Exception('we only support truecolor with alpha')
    if bitd != 8:
        raise Exception('we only support a bit depth of 8')
    if interlacem != 0:
        raise Exception('we only support no interlacing')

    '''
        With the help of zlib.decompress(s) method, we can decompress the compressed bytes of string into original string by using zlib.decompress(s) method.
        The scratch implementation of zlib.decompress() can be seen from here: https://pyokagan.name/blog/2019-10-18-zlibinflate/
    '''
    IDAT_data = b''.join(chunk_data for chunk_type, chunk_data in chunks if chunk_type == b'IDAT')
    IDAT_data = zlib.decompress(IDAT_data)

    '''
        We reconstruct the pixels by reverting the filter type 0 from the image
    '''
    Recon = []
    bytesPerPixel = 4
    stride = width * bytesPerPixel

    def Recon_a(r, c):
        return Recon[r * stride + c - bytesPerPixel] if c >= bytesPerPixel else 0

    def Recon_b(r, c):
        return Recon[(r-1) * stride + c] if r > 0 else 0

    def Recon_c(r, c):
        return Recon[(r-1) * stride + c - bytesPerPixel] if r > 0 and c >= bytesPerPixel else 0

    i = 0
    for r in range(height): # for each scanline
        filter_type = IDAT_data[i] # first byte of scanline is filter type
        i += 1
        for c in range(stride): # for each byte in scanline
            Filt_x = IDAT_data[i]
            i += 1
            if filter_type == 0: # None
                Recon_x = Filt_x
            elif filter_type == 1: # Sub
                Recon_x = Filt_x + Recon_a(r, c)
            elif filter_type == 2: # Up
                Recon_x = Filt_x + Recon_b(r, c)
            elif filter_type == 3: # Average
                Recon_x = Filt_x + (Recon_a(r, c) + Recon_b(r, c)) // 2
            elif filter_type == 4: # Paeth
                Recon_x = Filt_x + PaethPredictor(Recon_a(r, c), Recon_b(r, c), Recon_c(r, c))
            else:
                raise Exception('unknown filter type: ' + str(filter_type))
            Recon.append(Recon_x & 0xff) # truncation to byte


    img = np.array(Recon).reshape((height, width, 4))
    return img