from setuptools import setup, find_packages

setup(
    name="pytrait",
    version="0.0.1",
    description="",
    author="Xander Rudelis",
    url="https://github.com/xrudelis/pytrait",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="trait, traits",
    package_dir={"": "./"},
    packages=find_packages(where="./"),
    python_requires=">=3.6, <4",
)
