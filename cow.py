#!/usr/local/bin/python

import sys
import codecs
import chardet


def read_then_write(in_file, guess_encoding, out_encoding):
    dot_pos = in_file.rfind('.')
    output_file = in_file[0:dot_pos] + '(%s)' % out_encoding + in_file[dot_pos:]
    writer = open(output_file, 'wb')
    reader = open(in_file, 'rw')
    for line in reader:
        line = codecs.decode(line, guess_encoding)
        encoded_line = codecs.encode(line, out_encoding)
        writer.write(encoded_line)
    reader.close()
    writer.close()


def convert(in_file, out_encoding):
    confidence, guess_encoding = detect(input_file)
    if confidence > 40.0:
        read_then_write(in_file, guess_encoding, out_encoding)
        print 'Convert from %s to %s Completed (with a confidence of %.2f%%)!' \
              % (guess_encoding, out_encoding, confidence)
    else:
        print 'Convert failed! [Debug info] confidence->%s, guess_encoding->%s' % (confidence, guess_encoding)


def detect(in_file):
    with open(in_file, 'rb') as f:
        result = chardet.detect(f.read())
        confidence = float(result['confidence']) * 100
        guess_encoding = result['encoding']
    return confidence, guess_encoding


def print_usage():
    print 'Usage: python cow.py [detect/convert] input_file [output_encoding(default: utf-8)]'


if __name__ == '__main__':
    arg_num = len(sys.argv)
    if arg_num > 2:
        a_type = sys.argv[1]
        input_file = sys.argv[2]
        output_encoding = 'utf-8'
        if a_type == 'detect':
            g_confidence, g_encoding = detect(input_file)
            print 'Guess encoding: %s (with a confidence of %.2f%%).' % (g_encoding, g_confidence)
        elif a_type == 'convert':
            if arg_num > 3:
                output_encoding = sys.argv[2]
            convert(input_file, output_encoding)
    else:
        print_usage()
