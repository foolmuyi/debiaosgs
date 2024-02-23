import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="debiaosgs",
    version="0.0.5",
    author="Debiao",
    author_email="muyiorlk@gmail.com",
    description="SGS Room Monitor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/foolmuyi/debiaosgs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['matplotlib', 'numpy', 'pandas', 'requests', 'eth-account', 'web3'],
    python_requires='>=3.6',
)