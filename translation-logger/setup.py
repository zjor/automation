import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="rutrans",
    version="0.0.1",
    author="Sergey Royz",
    author_email="zjor.se@gmail.com",
    description=("Logs words you translate with 'trans' command."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zjor/automation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "rutrans = downloader.cli:main",
        ]
    }
)