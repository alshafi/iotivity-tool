# IOTivity json security conversion

The cborjsoncon.py is a tool to convert the IOTivity security virtual resources (SVR) database from json file to cbor and vice versa.

## Motivation
Prior to making this tool, I used to use the [json2cbor](https://github.com/iotivity/iotivity/blob/master/resource/csdk/security/tool/json2cbor.c) tool that ships with IoTivity to convert the SVR from json to cbor and [cbor.me](cbor.me) to convert the other way.
json2cbor needed to be built before I could use it and python would be hany as it could run on multiple systems without compiling for a specific target.
However, the pressing reason for making this tool was converting cbor back to json which required the following steps:
* get the hex value of the cbor file
* paste the hex value of the cbor file into cbor.me
* cbor.me decodes 1 layer of cbor so I need to backup the decoded cbor and traverse manulaly to decode all cbor layers. PAIN!!
* use a json editor in order to format the final decoded file so I can read it easier.

This tool does all of the above steps in the backgroud using the python cbor.

note this is not a normal json2cbor conversion !!!


# usage

cbor2json.py -i <input_file (cbor or json)> -o <output_file (cbor or json)>

the tool will determine the direction of conversion based on the file extensions 
