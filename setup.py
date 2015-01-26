from setuptools import setup

setup(
    name='install_freedesktop',
    version='0.1',
    description='Setuptools extension to install freedesktop.org app icons',
    author='Jacob Welsh',
    author_email='jacob@welshcomputing.com',
    url='https://github.com/welshjf/install_freedesktop',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Build Tools',
    ],
    py_modules=['install_freedesktop'],
    entry_points={
        'distutils.commands': [
            'install = install_freedesktop:install',
            'install_desktop = install_freedesktop:install_desktop',
        ],
        'distutils.setup_keywords': [
            'desktop_entries = install_freedesktop:check_desktop_entries',
        ],
    },
)
