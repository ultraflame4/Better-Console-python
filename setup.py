import setuptools
long_description='''
Please go to the github [here](https://github.com/ultraflame4/Better-Console-python)
'''
setuptools.setup(
    name="Better Console",
    version="0.0.6",
    author="ultraflame4",
    author_email="ultraflame4@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A Better Console for python programs",
    url="https://github.com/ultraflame4/Better-Console-python",
    packages=["Better_Console"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'PySimpleGuiQt'
    ]
)
