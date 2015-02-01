===================
install_freedesktop
===================

Setuptools extension to install launcher icons for KDE, GNOME, or other
freedesktop.org compatible Linux/UNIX environments.

Desktop entry spec:
http://standards.freedesktop.org/desktop-entry-spec/latest/index.html

License
=======

Copyright 2015 Jacob Welsh

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Usage
=====

Once this module is installed (such as by using the ``setup_requires``
argument), desktop entry files will be automatically installed for each
``gui_scripts`` entry point. Example::

    setup(
        ...
        setup_requires=['install_freedesktop'],
        entry_points={
            'gui_scripts': [
                'myapp=myapp:main',
            ],
        },
    )

This would create *myapp.desktop*, setting the Name and Icon keys to “myapp”
and Exec to the full path of the script.

To customize, or add desktop files for non-entry-point based scripts, pass a
dict to the ``desktop_entries`` argument, where each key matches a script name
and its value is a dict containing the desktop entry keys/values. Example::

    setup(
        ...
        setup_requires=['install_freedesktop'],
        scripts=['myscript'],
        desktop_entries={
            'myscript': {
                'Name': 'MyApp',
                'GenericName': 'Data Processor',
                'Categories': 'Office;Database;',
            },
        },
    )

Notes
=====

Either system-wide or ``--user`` mode installation is supported, as well as
``--root=`` (for package builders). But the setuptools default egg-based
installation does not work. (It doesn't run ``install_`` subcommands; even if
it did, the data files would go in the egg, not the real data directory.) So
you must either use ``pip`` (recommended) or provide the
``--single-version-externally-managed`` option yourself, on the command line or
in *setup.cfg*. Wheels and any other relocatable bdist formats will also not
work, due to the need to use the final script path for the Exec in the desktop
file.

Using the ``setup_requires`` argument is potentially dangerous: if the package
is not found, EasyInstall will be invoked to fetch it from PyPI, even if the
user thinks they have disabled this or chosen a different index. See
https://pip.pypa.io/en/latest/reference/pip_install.html#controlling-setup-requires.

There is no automatic handling of icon files presently, though that's in scope
for this project. Quick example for doing it manually::

    setup(
        ...
        data_files=[
            ('share/icons/hicolor/16x16/apps', ['icons/16x16/myapp.png']),
            ('share/icons/hicolor/48x48/apps', ['icons/48x48/myapp.png']),
            ('share/icons/hicolor/scalable/apps', ['icons/scalable/myapp.svg']),
        ],
    )
