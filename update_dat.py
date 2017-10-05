import os, shutil, subprocess
import platform as p
platform_info = p.platform()

raspberry_pi = 'Linux' in platform_info and \
('armv7l' in platform_info or 'armv6l' in platform_info) and \
'debian' in platform_info
home_dir = r'/home/pi' if raspberry_pi else 'r/home/rami'
arch = r'arm' if raspberry_pi else r'x86_64'

iotivity_root = home_dir + r'/iot/iotivity'
output_root = iotivity_root + r'/out/linux/' + arch + r'/debug'
server_path = r'/examples/OCFSecure/'
client_path = server_path

tool_path = output_root + '/resource/csdk/security/tool'
# server files
server_json_file_name = 'ocf_svr_db_server.json'
server_json_file = iotivity_root + server_path + server_json_file_name
server_dat_file_name = '/ocf_svr_db_server.dat'
server_dat_file_input = iotivity_root + server_path + server_dat_file_name
server_dat_file_output = output_root + server_path + server_dat_file_name
# client files
client_json_file_name = '/ocf_svr_db_client.json'
client_json_file = iotivity_root + client_path + client_json_file_name
client_dat_file_name = '/ocf_svr_db_client.dat'
client_dat_file_input = iotivity_root + client_path + client_dat_file_name
client_dat_file_output = output_root + client_path + client_dat_file_name

# check if directories exits
issues = list()
if not os.path.exists(output_root):
    issues.append("output dir does not exist")
if not os.path.exists(output_root + '/resource/'):
    issues.append("resource dir isn ot built")
if not os.path.exists(tool_path):
    issues.append("tool directory is not built")
if not os.path.exists(server_json_file):
    issues.append("server json file does not exist")
if not os.path.exists(client_json_file):
    issues.append("client json file does not exist")

if len(issues) > 0:
    raise Exception(issues)

current_wd = os.getcwd()
os.chdir(tool_path)

try:
    subprocess.call(["./json2cbor", server_json_file, server_dat_file_input])
    subprocess.call(["./json2cbor", client_json_file, client_dat_file_input])
except Exception:
    raise

if not os.path.exists(server_dat_file_input):
    issues.append("server dat file [{}] does not exist".format(server_dat_file))
if not os.path.exists(client_dat_file_input):
    issues.append("client dat file does not exist")

if len(issues) > 0:
    raise Exception(issues)

shutil.copy(server_dat_file_input, server_dat_file_output)
shutil.copy(client_dat_file_input, client_dat_file_output)

if not os.path.exists(server_dat_file_output):
    issues.append("server output dat file does not exist")
if not os.path.exists(client_dat_file_output):
    issues.append("client output dat file does not exist")

if len(issues) > 0:
    raise Exception(issues)
os.chdir(current_wd)

