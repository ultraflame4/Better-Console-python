import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="Better Console",
    version="0.0.3",
    author="ultraflame4",
    author_email="ultraflame4@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A Better Console for python programs",
    url="https://github.com/ultraflame4/Better-Console-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'PySimpleGuiQt'
    ]
)
