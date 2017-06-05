import os
import subprocess
from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, EnumValue


class BatchController:
    
    def __init__(self, model_path, model_name):
        self.model_name = model_name
        self.model_path = model_path        
        self._get_FS2000_install_directory()
        self._update_batch_nam()
        
    def _get_FS2000_install_directory(self):
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, 'SOFTWARE\Wow6432Node\FS2000\Setup')
        self._install_directory = EnumValue(key, 0)[1]
        
    def _update_batch_nam(self):
        path = os.path.join(self._install_directory, 'batch.nam')
        with open(path, 'w') as nam:
            nam.write(self._generate_nam_data())

    def _generate_nam_data(self):
        return '{0}\{1}\n{1}\n{0}'.format(self.model_path, self.model_name)

    def run_command(self, command):
        exe = 'system/' + command.name + '.exe'
        cmd = os.path.join(self._install_directory, exe)
        command_list = [cmd, command.arg]
        subprocess.call(command_list)
        
    def change_batch_model(self, model_path, model_name):
        self.model_name = model_name
        self.model_path = model_path
        self._update_batch_nam()
        
