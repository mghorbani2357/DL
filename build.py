from PyInstaller.utils.hooks import copy_metadata, collect_data_files
import PyInstaller.__main__
import platform
import versioneer

data = list()
with open('requirements.txt') as requirements:
    for line in requirements.readlines():
        data += copy_metadata('humanize')
        data += collect_data_files('humanize')

if platform.system() == 'Linux':

    dist_path = 'dist/linux'

elif platform.system() == 'Windows':

    dist_path = 'dist/windows'

elif platform.system() == 'MacOS':

    dist_path = 'build/mac'

else:
    dist_path = 'dist'

console_project_path = "interfaces/console/main.py"
output_file_name = "dl"

installer_config = [
    console_project_path,
    '--onefile',
    '--name', output_file_name,
    '--distpath', dist_path,
    '--version-file', versioneer.get_version()

]

for item in data:
    installer_config += ['--add-data', f'{item[0]}:{item[1]}']

PyInstaller.__main__.run(installer_config)
