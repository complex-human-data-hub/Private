import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Private",
    version="0.0.1",
    author="Simon Dennis",
    author_email="simon.dennis@unimelb.edu.au",
    description="Private privacy preserving language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/complex-human-data-hub/Private",
    packages=['Private'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
