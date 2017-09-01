import os, shutil, subprocess
iotivity_root = r'/home/rami/iot/iotivity'
output_root = iotivity_root + r'/out/linux/x86_64/debug'
server_path = r'/resource/csdk/security/provisioning/sample'
client_path = r'/plugins/samples/linux'
server_json_file = iotivity_root + server_path +'/oic_svr_db_server_justworks.json'
server_dat_file = iotivity_root + server_path + '/oic_svr_db_server_justworks.dat'
tool_path = output_root + '/resource/csdk/security/tool'
client_json_file = iotivity_root + client_path + '/oic_svr_db_client.json'
client_dat_file = iotivity_root + client_path + '/oic_svr_db_client.dat'

# check if directories exits
issues = list()
if not os.path.exists(output_root):
    issues.append("output dir does not exist")
if not os.path.exists(output_root + '/resource/'):
    issues.append("resource dir isn ot built")
if not os.path.exists(tool_path):
    issues.append("tool directory is not built")
if not os.path.exists(output_root + '/plugins'):
    issues.append("plugins dir is not built")
if not os.path.exists(server_json_file):
    issues.append("server json file does not exist")
if not os.path.exists(client_json_file):
    issues.append("client json file does not exist")

if len(issues) > 0:
    raise Exception(issues)

current_wd = os.getcwd()
os.chdir(tool_path)

try:
    subprocess.call(["./json2cbor", server_json_file, server_dat_file])
    print "\n\n\n ====================================================================================== \n\n\n"
    subprocess.call(["./json2cbor", client_json_file, client_dat_file])
except Exception:
    raise

if not os.path.exists(server_dat_file):
    issues.append("server dat file does not exist")
if not os.path.exists(client_dat_file):
    issues.append("client dat file does not exist")

if len(issues) > 0:
    raise Exception(issues)

shutil.copy(server_dat_file, output_root + server_path + '/oic_svr_db_server_justworks.dat')
shutil.copy(client_dat_file, output_root + client_path + '/oic_svr_db_client.dat')

if not os.path.exists(output_root + server_path + '/oic_svr_db_server_justworks.dat'):
    issues.append("server output dat file does not exist")
if not os.path.exists(output_root + client_path + '/oic_svr_db_client.dat'):
    issues.append("client output dat file does not exist")

if len(issues) > 0:
    raise Exception(issues)
os.chdir(current_wd)

