from setuptools import setup, find_packages


def long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="virgo",
    version="1.0.0",
    url="https://github.com/Mozzo1000/virgo",
    license="Apache 2.0",
    author="Andreas Backström",
    author_email="mozzo242@gmail.com",
    description="A TCP connection protocol for simpler sharing of data",
    install_requires=[
        ""
    ],
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=['virgo', 'virgo.core'],
    entry_points={
        "console_scripts": [
            "virgo=virgo.server:main",
        ]
    },
    python_requires=">=3.7",
    keywords="virgo server tcp",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
