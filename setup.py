from setuptools import setup, find_packages


setup(
    name='debiaosgs',
    version='0.0.8',
    python_requires='>=3.6.0',
    author='Debiao',
    author_email='muyiorlk@gmail.com',
    url='https://github.com/foolmuyi/debiaosgs',
    description='SGS Room Monitor',
    long_description='Monitoring SGS website for new listed room, notify by email',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.4.3',
        'aiohttp>=3.7.4',
        'matplotlib>=3.3.3',
        'numpy>=1.21.2',
        'pandas>=1.1.1',
        'requests>=2.22.0',
        'eth-account>=0.8.0',
        'web3>=6.0.0',
        ],
    classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ],
)
