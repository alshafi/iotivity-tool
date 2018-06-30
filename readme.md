# IoTivity json security conversion

The cborjsoncon.py is a tool to convert the IoTivity security virtual resources (SVR) database from json format to cbor format and vice versa. It should be compatible for both Python 2 and Python 3 and should run on any operating system with python installed in it. Please file a github issue if your OS or Python version is not compatible with this tool with as much details as possible for me to reproduce the issue and fix it. you can also file a PR if you want to fix it yourself.

## Motivation
Prior to making this tool, I used to use the [json2cbor](https://github.com/iotivity/iotivity/blob/master/resource/csdk/security/tool/json2cbor.c) tool that ships with IoTivity to convert the SVR from json to cbor and use another tool [cbor.me](cbor.me) to convert the other way (cbor to json).

json2cbor needed to be built before I could use it and python would be handy as it could run on multiple systems without compiling for a specific target.
However, the pressing reason for making this tool was converting cbor back to json which required the following steps:
* get the hex value of the cbor file, which requires the use of yet another tool!
* cbor.me decodes only 1 layer of cbor so I need to backup the decoded cbor and traverse manually to decode all cbor layers. PAIN!!
* use a json editor in order to format the final decoded file so I can read it easier.

## Advantages
* This is the only tool needed to replace the 4 tools mentioned above (which could be different depending on the operating system! :disappointed:) Instead of using json2cbor, cbor.me and whatever tool used for reading the hex value of the cbor file and whatever tool to format the json file.
* It can detect the direction of the conversion (cbor to json or json to cbor) based on the file extensions (.json for JSON and .dat for CBOR)
* Decodes cbor completely regardless of how deeply nested it is
* Formats the output json for much better readability. 
* Additionally, you can point the input to a folder containing many json and cbor files and it will convert all of them regardless of the folder structure that was given as an input.  

note this is not a normal json2cbor conversion !!!

# Dependencies
This tool depends on the [cbor](https://bitbucket.org/bodhisnarkva/cbor) package. To install it, you can either use the requirements file with the following command

`$sudo pip install -r requirements.txt`

Or this command to install cbor alone, which is the only dependency so far

`$sudo pip install cbor`

# usage

`python cbor2json.py -i <input file | input folder> -o <output file | output folder>`

* The tool will determine the direction of conversion based on the file extensions
* The input and output must be the same type. Either both are files for converting individual files or both are folders for converting a group of files at once.

# Troubleshooting
If you get an error for not finding pip, type the following command
On Linux and python 2

`sudo apt-get install python-pip`

On Linux and Python 3

`sudo apt-get install python3-pip`
