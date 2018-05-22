import os
import sys
import errno


try:
    from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, EnumValue
except ImportError:
    pass


def get_FS2000_install_directory():
    try:
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, 'SOFTWARE\\Wow6432Node\\FS2000\\Setup')
        install_directory = EnumValue(key, 0)[1]
        return install_directory
    except:
        raise RuntimeError('FS2000 must be installed')


def update_nam(nam_type, model_name, model_path):
    install_directory = get_FS2000_install_directory()
    path = os.path.join(install_directory, nam_type + '.nam')
    with open(path, 'w') as nam:
        nam.write(generate_nam_data(model_name, model_path))


def update_batch_nam(model_name, model_path):
    update_nam('batch', model_name, model_path)


def update_model_nam(model_name, model_path):
    update_nam('model', model_name, model_path)


def generate_nam_data(model_name, model_path):
    return '{0}\{1}\n{1}\n{0}'.format(model_path, model_name)


ERROR_INVALID_NAME = 123
ERROR_FILENAME_EXCED_RANGE = 204
'''
Windows-specific error code indicating an invalid pathname.

See Also
----------
https://msdn.microsoft.com/en-us/library/windows/desktop/ms681382%28v=vs.85%29.aspx
    Official listing of all such codes.
'''


def is_pathname_valid(pathname):
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = os.path.splitdrive(pathname)

        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)

            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror in {ERROR_INVALID_NAME,
                                        ERROR_FILENAME_EXCED_RANGE}:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False

    except TypeError as exc:
        return False

    else:
        return True


def is_path_creatable(pathname):
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


def is_path_exists_or_creatable(pathname):
    '''
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        return False
