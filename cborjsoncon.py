"""
This tool basically converts json to cbor and vice versa
"""
import cbor, json, sys, getopt
__author__ = "Rami Alshafi"
__email__ = "ralshafi@vtmgroup.com"
__copyright__ = "Copyright 2017, VTM Group"
__version__ = "0.0.1"
__status__ = "alpha"


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:')
    except getopt.GetoptError:
        print('cbor2json.py -i <input_file> -o <output_file>')
        sys.exit(2)
    if len(opts) == 0:
        print('cbor2json.py -i <input_file> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('cbor2json.py -i <input_file> -o <output_file>')
            sys.exit()
        elif opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg
    print ('input file is <{}> and output file is <{}>'.format(input_file, output_file))
    if input_file.endswith('.dat') and output_file.endswith('.json'):
        print('converting cbor to json')
        write_json(read_cbor(input_file), output_file)
    elif input_file.endswith('.json') and output_file.endswith('.dat'):
        print('converting json to cbor')
        write_cbor(read_json(input_file), output_file)
    else:
        raise Exception("this conversion is not supported")


def read_cbor(input_file):
    cbor_dict = dict()
    with open(input_file, 'rb') as fp:
        data = cbor.load(fp)
        traverse(data, cbor_dict)
    return cbor_dict


def traverse(in_dict, out_dict):
    # base case?
    if not isinstance(in_dict, dict):
        return
    for sec, val in in_dict.items():
        try:
            out_dict[sec] = cbor.loads(val)
        except TypeError:
            out_dict[sec] = val
        except Exception as e:
            raise e
        traverse(out_dict[sec], out_dict[sec])


def read_json(input_file):
    with open(input_file, 'rb') as fp:
        data = json.load(fp)
    return data


def write_cbor(json_dict, output_file):
    cbor_data = cbor.dumps(json_dict, sort_keys=True)
    with open(output_file, 'wb') as cbor_file:
        cbor_file.write(cbor_data)
    return True


def write_json(cbor_dict, output_file):
    try:
        json_data = json.dumps(cbor_dict, sort_keys=True, indent=4)
    except Exception:
        print("failed to write json, will try it with latin1 encoding")
        json_data = json.dumps(cbor_dict, sort_keys=True, indent=4, encoding='latin1')
    with open(output_file, 'w') as json_file:
        json_file.write(json_data)
    return True

if __name__ == '__main__':
    main(sys.argv[1:])
