from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, EnumValue
import os

def get_FS2000_install_directory():
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg, 'SOFTWARE\Wow6432Node\FS2000\Setup')
    install_directory = EnumValue(key, 0)[1]
    return install_directory
    
def update_batch_nam(model_name, model_path):
    install_directory = get_FS2000_install_directory()
    path = os.path.join(install_directory, 'batch.nam')
    with open(path, 'w') as nam:
        nam.write(generate_nam_data(model_name, model_path))

def generate_nam_data(model_name, model_path):
    return '{0}\{1}\n{1}\n{0}'.format(model_path, model_name)