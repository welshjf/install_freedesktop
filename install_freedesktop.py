# Copyright 2015 Jacob Welsh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools.command.install import install
import os
from distutils import log
from distutils.core import Command
from distutils.errors import DistutilsSetupError

__version__ = '0.1.2'

def current_umask():
    old = os.umask(0)
    os.umask(old)
    return old

install.sub_commands.extend([
    ('install_desktop', lambda self: True),
#    ('install_icons', lambda self: True),
])

class install_desktop(Command):

    "Distutils subcommand to generate desktop entry files"

    description = "Generate and install desktop entry files"

    user_options = [
        ('script-dir=', None,
         "installation directory for Python scripts"),
        ('data-dir=', None,
         "installation directory for data files"),
    ]

    def initialize_options(self):
        self.root = None
        self.data_dir = None
        self.script_dir = None
        self.outfiles = []

    def finalize_options(self):
        self.set_undefined_options('install',
                ('root', 'root'),
                ('install_data', 'data_dir'),
                ('install_scripts', 'script_dir'),
                )

    def run(self):
        dist = self.distribution
        if dist.desktop_entries is None:
            desktop_entries = {}
        else:
            desktop_entries = dist.desktop_entries

        scripts = list(desktop_entries.keys())

        # Automatically add gui_scripts
        if dist.entry_points:
            gui_scripts = [s.split('=')[0] for s in
                    dist.entry_points.get('gui_scripts', [])]
            scripts += [s for s in gui_scripts if s not in desktop_entries]

        if not self.root:
            self.root = '/'
        target_script_dir = '/' + os.path.relpath(self.script_dir, self.root)

        for script in scripts:
            data = desktop_entries.get(script, {})
            # Fill required keys
            if 'Name' not in data:
                data['Name'] = script
            if 'Icon' not in data:
                data['Icon'] = script # not required but convenient
            data['Type'] = 'Application'
            data['Exec'] = os.path.join(target_script_dir, script)
            dest_dir = os.path.join(self.data_dir, 'share/applications')
            dest_file = os.path.join(dest_dir, data['Name'] + '.desktop')
            self.mkpath(dest_dir)
            log.info('writing ' + dest_file)
            with open(dest_file, 'w') as f:
                f.write('[Desktop Entry]\n')
                for key, value in sorted(data.items()):
                    f.write('%s=%s\n' % (key, value))
            os.chmod(dest_file, 0o777 - current_umask())
            self.outfiles.append(dest_file)

    def get_inputs(self):
        return []

    def get_outputs(self):
        return self.outfiles

def check_desktop_entries(dist, attr, value):

    "Partial validator for the desktop_entries setup argument"

    if type(value) is not dict:
        raise DistutilsSetupError("%r must be a dict (got %r)" % (attr, value))

    entry_points = (dist.entry_points.get('console_scripts', []) +
                    dist.entry_points.get('gui_scripts', []))
    scripts = [ep.split('=')[0] for ep in entry_points]
    if dist.scripts:
        scripts.extend([os.path.basename(script) for script in dist.scripts])

    for entry, contents in value.items():
        if entry not in scripts:
            raise DistutilsSetupError(
                "Desktop entry name must match an installed script "
                "(got: %r, options: %s)" %
                (entry, ', '.join([repr(s) for s in scripts])))
        if type(contents) is not dict:
            raise DistutilsSetupError(
                "Desktop entry must be a dict (got %r)" % contents)
