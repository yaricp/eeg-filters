import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eeg_filters", # Replace with your own username
    version="0.0.1",
    author="Yaric Pisarev",
    author_email="yaricp@gmail.com",
    description="Package for to filter EEG signals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaricp/eeg-filters",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISP License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
