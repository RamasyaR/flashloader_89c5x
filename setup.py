# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flashloader',
 'flashloader.cli',
 'flashloader.ezdl',
 'flashloader.gui']

package_data = \
{'': ['*']}

install_requires = \
['pyserial',
 'intelhex',
 'pydantic']

setup_kwargs = {
    'name': 'flashloader',
    'version': '0.0.1',
    'description': 'Flash loader utility for 89C51 microcontrollers',
    'long_description': '',
    'author': 'Raman Rakavets',
    'author_email': 'radikot88@gmail.com',
    'maintainer': 'Raman Rakavets',
    'maintainer_email': 'radikot88@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

