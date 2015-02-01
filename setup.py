from setuptools import setup
import codecs

with codecs.open('README.rst', encoding='utf-8') as f:
    README = f.read()
with codecs.open('CHANGES.rst', encoding='utf-8') as f:
    CHANGES = f.read()

setup(
    name='install_freedesktop',
    version='0.1.1',
    description='Setuptools extension to install freedesktop.org app icons',
    long_description=README + '\n\n' + CHANGES,
    author='Jacob Welsh',
    author_email='jacob@welshcomputing.com',
    url='https://github.com/welshjf/install_freedesktop',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Build Tools',
    ],
    py_modules=['install_freedesktop'],
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'distutils.commands': [
            'install_desktop = install_freedesktop:install_desktop',
        ],
        'distutils.setup_keywords': [
            'desktop_entries = install_freedesktop:check_desktop_entries',
        ],
    },
)
