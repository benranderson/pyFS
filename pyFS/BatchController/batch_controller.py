import os
import subprocess
import pyFS.SystemUtils as util


class BatchController:

    def __init__(self, model_path, model_name):
        self._install_directory = util.get_FS2000_install_directory()
        util.update_batch_nam(model_name, model_path)

    def run_command(self, command):
        exe = 'system/' + command.name + '.exe'
        cmd = os.path.join(self._install_directory, exe)
        command_list = [cmd, command.arg]
        subprocess.call(command_list)

    def change_batch_model(self, model_path, model_name):
        util.update_batch_nam(model_name, model_path)

    def run_commands(self, commands):
        [run_command(command) for command in commands]
