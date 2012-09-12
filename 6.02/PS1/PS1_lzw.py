# template file for 6.02 PS1, Python Task 4 (LZW Compression/Decompression)
import sys
from optparse import OptionParser
import struct
import array



def compress(filename):
    """
    Compresses a file using the LZW algorithm and saves output in another file.
    Arguments: 
        filename: filename of file to compress.
    Returns:
        None.
    """
    
    # define constants like output file name and max table size
    MAX_TABLE_SIZE = 2**16
    OUTPUT_FILE_NAME = filename + '.zl'

    # open the file and initialize the table and output
    f = open(filename, 'rb')
    input_message = array.array("B", f.read())
    lzw_table = initialize_lzw_table(True)
    output = array.array("B")
    current_message = []
    counter = 256

    # read through the input, performing lzw
    for i in xrange(len(input_message)):
        if lzw_table.has_key("".join(current_message + [chr(input_message[i])])):
            current_message.append(chr(input_message[i]))
        else:
            write_to_table(lzw_table, current_message, output)
            current_message.append(chr(input_message[i]))
            lzw_table["".join(current_message)] = counter
            counter += 1
            if counter >= MAX_TABLE_SIZE:
                raise "This file needs more than 2**16 entries"
            current_message = [chr(input_message[i])]
    write_to_table(lzw_table, current_message, output)
    output.write(open(OUTPUT_FILE_NAME, 'wb'))

def initialize_lzw_table(compression=True):
    lzw_table = {}
    for i in xrange(256):
        if compression:
            lzw_table[chr(i)] = i
        else:
            lzw_table[i] = i
    return lzw_table

def write_to_table(lzw_table, message, output):
    decimal = lzw_table["".join(message)]
    top_half = decimal / 256
    bottom_half = decimal - top_half*256
    output.append(bottom_half)
    output.append(top_half)

def uncompress(filename):
    """
    Decompresses a file using the LZW algorithm and saves output in another file.
    Arguments: 
        filename: filename of file to decompress.
    Returns:
        None.
    """
    # defining constants
    MAX_TABLE_SIZE = 2**16
    OUTPUT_FILE_NAME = filename + '.zl'

    # initialize everything
    f = open(filename, 'rb')
    compressed_message = array.array('H', f.read())
    lzw_table = initialize_lzw_table(False)
    output = array.array("B")
    current_message = []
    counter = 256

    # read through the compressed message, performing decompression
    i = 0
    while i < len(compressed_message):
        current_index = get_two_byte_integer(compressed_message[i], compressed_message[i+1])
        i += 2
        output.append(lzw_table[current_index])

        if lzw_table.has_key("".join(current_message) + [chr(compressed_message[i])]):
            current_message.append(chr(compressed_message[i]))
        else:
            write_to_table(lzw_table, current_message, compressed_message[i])

def get_two_byte_integer(bottom_half, top_half):
    return bottom_half + top_half*256

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--filename", type="string", dest="fname", 
                      default="test", help="file to compress or uncompress")
    parser.add_option("-c", "--compress", action="store_true", dest="uncomp", 
                      default=True, help="compress file")
    parser.add_option("-u", "--uncompress", action="store_true", dest="uncomp", 
                      default=False, help="uncompress file")

    (opt, args) = parser.parse_args()
    
    if opt.uncomp == True:
        uncompress(opt.fname)
    else:
        compress(opt.fname)
