from setuptools import find_packages, setup

__version__ = "0.0.1"


setup(
    author="Matt Rasband",
    author_email="matt.rasband@gmail.com",
    description="Read-only Asyncio based APRS client",
    install_requires=["aprslib==0.6.46"],
    name="aioaprs",
    packages=find_packages(),
    python_requires=">=3.7",
    url="https://github.com/mrasband/aioaprs",
    version=__version__,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
)
