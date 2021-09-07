"""Setuptools based setup module."""

from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kim-property',
    version=versioneer.get_version(),
    description='kim-property - KIM-PROPERTY utility module.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/openkim/kim-property',
    author='Yaser Afshar',
    author_email='yafshar@umn.edu',
    license='LGPL-2.1-or-later',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    install_requires=['kim-edn'],
    python_requires='>=3.6',
    include_package_data=True,
    keywords='kim-property',
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
)
