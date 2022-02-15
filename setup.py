import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="hashpic",
    version="0.5.1",
    description="Create an image from a MD5, SHA512, SHA3-512, Blake2b or SHAKE256 hash",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/0xflotus/hashpic",
    author="0xflotus",
    author_email="0xflotus+pypi@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["hashpic"],
    include_package_data=True,
    install_requires=["argparse", "Pillow"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["hashpic=hashpic.__main__:main"]},
)
