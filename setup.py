from setuptools import setup

setup(
    name='pyarcadia',
    packages=['pyarcadia'],
    version='1.0.0',
    description='An arcadia-api wrapper built for python3+',
    author='Zenrac',
    author_email='zenrac@outlook.fr',
    url='https://github.com/Zenrac/arcadia.py',
    download_url='https://github.com/Zenrac/arcadia.py/archive/1.0.0.tar.gz',
    keywords=['arcadia'],
    include_package_data=True,
    install_requires=['aiohttp']
)