import cbor, json, sys, getopt


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:')
    except getopt.GetoptError:
        print 'cbor2json.py -i <input_file> -o <output_file>'
        sys.exit(2)
    if len(opts) == 0:
        print 'cbor2json.py -i <input_file> -o <output_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'cbor2json.py -i <input_file> -o <output_file>'
            sys.exit()
        elif opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg
    print 'input file is <{}> and output file is <{}>'.format(input_file, output_file)
    if input_file.endswith('.dat') and output_file.endswith('.json'):
        print 'converting cbor to json'
        write_json(read_cbor(input_file), output_file)
    elif input_file.endswith('.json') and output_file.endswith('.dat'):
        print 'converting json to cbor... not tested feature yet'
        write_cbor(read_json(input_file), output_file)


def read_cbor(input_file):
    cbor_dict = dict()
    with open(input_file, 'rb') as fp:
        data = cbor.load(fp)
    for sec, val in data.iteritems():
        cbor_dict[sec] = cbor.loads(val)
    return cbor_dict


def read_json(input_file):
    json_dict = dict()
    with open(input_file, 'rb') as fp:
        data = json.load(fp)
    return data


def write_cbor(json_dict, output_file):
    cbor_data = cbor.dumps(json_dict, sort_keys=True)
    with open(output_file, 'wb') as cbor_file:
        cbor_file.write(cbor_data)
    return True


def write_json(cbor_dict, output_file):
    json_data = json.dumps(cbor_dict, sort_keys=True, indent=4)
    with open(output_file, 'wb') as json_file:
        json_file.write(json_data)
    return True

if __name__ == '__main__':
    main(sys.argv[1:])
