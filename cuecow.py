#!/usr/local/bin/python

import sys
import codecs
import chardet


def read_then_write(input_file, guess_encoding, output_encoding):
    ipos = input_file.rfind('.')
    output_file = input_file[0:ipos] + '(%s)' % output_encoding + input_file[ipos:]
    writer = open(output_file, 'wb')
    reader = open(input_file, 'rw')
    for line in reader:
        line = codecs.decode(line, guess_encoding)
        encoded_line = codecs.encode(line, output_encoding)
        writer.write(encoded_line)
    reader.close()
    writer.close()


def convert(input_file, output_encoding):
    origin_fobj = open(input_file, 'rb')
    result = chardet.detect(origin_fobj.read())
    confidence = float(result['confidence'])
    if confidence > 0.5:
        guess_encoding = result['encoding']
        read_then_write(input_file, guess_encoding, output_encoding)
        print 'Convert from %s to %s Complete! (with a confidence of %d %%)' \
              % (guess_encoding, output_encoding, int(confidence*100))
    else:
        print 'Convert failed!'

def print_usage():
    print 'python cuecow.py input_file [output_encoding(default: utf-8)]'

if __name__ == '__main__':
    arg_num = len(sys.argv)
    if arg_num > 1:
        input_file = sys.argv[1]
        output_encoding = 'utf-8'
        if arg_num > 2:
            output_encoding = sys.argv[2]
        convert(input_file, output_encoding)
    else:
        print_usage()
