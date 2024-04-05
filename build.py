from PyInstaller.utils.hooks import copy_metadata, collect_data_files
import PyInstaller.__main__
import versioneer

data = list()
with open('requirements.txt') as requirements:
    for line in requirements.readlines():
        data += copy_metadata('humanize')
        data += collect_data_files('humanize')

dist_path = 'dist'

console_project_path = "dl/__main__.py"
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
