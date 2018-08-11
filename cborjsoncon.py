"""
This tool basically converts json to cbor and vice versa
"""
import cbor, json, sys, getopt, os, re

_IS_PY3 = sys.version_info[0] >= 3

__author__ = "Rami Alshafi"
__email__ = "ralshafi@vtmgroup.com"
__copyright__ = "Copyright 2017, VTM Group"
__version__ = "0.1.0"
__status__ = "beta"


def main(argv):
    input = ''
    output = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:')
    except getopt.GetoptError:
        print('cbor2json.py -i <input file | input folder> -o <output file | output folder>')
        sys.exit(2)
    if len(opts) == 0:
        print('cbor2json.py -i <input file | input folder> -o <output file | output folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('cbor2json.py -i <input file | input folder> -o <output file | output folder>')
            sys.exit()
        elif opt == '-i':
            input = arg
        elif opt == '-o':
            output = arg
    if os.path.isdir(input) and not os.path.isdir(output):
        print("The given output folder is not found. Creating it...")
        if output.endswith(".json") or output.endswith(".dat"):
            raise Exception("the input was a folder so the output must be a folder!")
        os.mkdir(output)
    if os.path.isdir(input) and os.path.isdir(output):
        print('input folder is <{}> and output folder is <{}>'.format(input, output))
        json_files = list()
        cbor_files = list()
        for dirpath, dirnames, filenames in os.walk(input):
            for file in filenames:
                if file.endswith('.dat'):
                    cbor_files.append(os.path.join(dirpath, file))
                elif file.endswith('.json'):
                    json_files.append(os.path.join(dirpath, file))
                else:
                    continue
        for json_file in json_files:
            output_file = os.path.join(output, get_output_file_name(json_file))
            print('converting json input <{}> to cbor output <{}>'.format(json_file, output_file))
            write_cbor(read_json(json_file), output_file)
        for cbor_file in cbor_files:
            output_file = os.path.join(output, get_output_file_name(cbor_file))
            print('converting cbor input <{}> to json output <{}>'.format(cbor_file, output_file))
            write_json(read_cbor(cbor_file), output_file)
    elif os.path.isfile(input):
        if input.endswith('.dat') and output.endswith('.json'):
            print('converting cbor input <{}> to json output <{}>'.format(input, output))
            check_output_folder(output)
            write_json(read_cbor(input), output)
        elif input.endswith('.json') and output.endswith('.dat'):
            print('converting json input <{}> to cbor output <{}>'.format(input, output))
            check_output_folder(output)
            write_cbor(read_json(input), output)
        else:
            raise Exception("This conversion is not supported. Please make sure you have the right file extensions."
                            " Got input file <{}> and output file <{}>".format(input, output))
    else:
        raise Exception("Input and output files and/or directories are not valid! Both of them must be either files or "
                        "directories. Got input ({}) and output ({})".format(input, output))


def read_cbor(input_file):
    cbor_dict = dict()
    with open(input_file, 'rb') as fp:
        data = cbor.load(fp)
        traverse(data, cbor_dict)
    return cbor_dict


def check_output_folder(file_name):
    out_dir_ = re.split(r"\\|/", file_name)
    if len(out_dir_) > 1:
        out_dir_ = out_dir_[:len(out_dir_)-1]
        out_dir_ = os.path.join(*out_dir_)
        if not os.path.exists(out_dir_):
            print("output file <{}> was pointed to a folder that does not exists so creating <{}>".format(file_name, out_dir_))
            os.mkdir(out_dir_)


def get_output_file_name(file_name):
    out_dir_ = re.split(r"\\|/", file_name)
    name_ = out_dir_[len(out_dir_) - 1]
    if name_.endswith(".json"):
        return name_.split(".json")[0] + ".dat"
    elif name_.endswith(".dat"):
        return name_.split(".dat")[0] + ".json"
    else:
        raise Exception("wrong file name <{}>".format(file_name))


def traverse(in_dict, out_dict):
    # base case?
    if not isinstance(in_dict, dict):
        return
    for sec, val in in_dict.items():
        # workaround python 2 issue. cbor false pass the conversion of unicode as it is already converted
        if not _IS_PY3 and isinstance(val, unicode):
            out_dict[sec] = val
        elif val == '':
            out_dict[sec] = val
        else:
            try:
                out_dict[sec] = cbor.loads(val)
            except TypeError:
                out_dict[sec] = val
            except ValueError:
                out_dict[sec] = val
            except Exception as e:
                raise e
        traverse(out_dict[sec], out_dict[sec])


def read_json(input_file):
    with open(input_file, 'r') as fp:
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
    except TypeError:
        if _IS_PY3:
            def cast_byte_str(diction):
                if diction['creds']:
                    for cred in diction['creds']:
                        if cred['privatedata']:
                            cred['privatedata']['data'] = str(cred['privatedata']['data'])
            if cbor_dict['cred']:
                if cbor_dict['resetpf']['cred']:
                    cast_byte_str(cbor_dict['resetpf']['cred'])
                cast_byte_str(cbor_dict['cred'])
            json_data = json.dumps(cbor_dict, sort_keys=True, indent=4)
    except Exception:
        print("failed to write json, will try it with latin1 encoding")
        json_data = json.dumps(cbor_dict, sort_keys=True, indent=4, encoding='latin1')
    with open(output_file, 'w') as json_file:
        json_file.write(json_data)
    return True

if __name__ == '__main__':
    main(sys.argv[1:])
