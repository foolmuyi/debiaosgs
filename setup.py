from setuptools import setup
from setuptools import find_packages


setup(
    name='debiaosgs',
    version='0.0.4',
    python_requires='>=3.6.0',
    author='Debiao',
    author_email='muyiorlk@gmail.com',
    url='https://github.com/foolmuyi/debiaosgs',
    description='SGS Room Monitor',
    long_description='Monitoring SGS website for new listed room, notify by email',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
    'console_scripts': ['example=src.sgs:main'],
    },
    install_requires=['selenium'],
    classifiers=[
    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
)
