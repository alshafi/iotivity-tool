# IOTivity json security conversion

The cborjsoncon.py is a tool to convert the IOTivity security json file to cbor.

this python tool has the same functionallity as:
https://github.com/iotivity/iotivity/blob/master/resource/csdk/security/tool/json2cbor.c
but since it is python it can run on mutiple systems without compiling for that specific target.

note this is not a normal json2cbor conversion !!!


# usage

cbor2json.py -i <input_file> -o <output_file>
