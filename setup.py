# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import setuptools
from naive_foss_health.config import NFHC_VERSION

with open("README.md") as i:
    _long_description = i.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

requirements_dev = []
with open('requirements-dev.txt') as f:
    requirements_dev = f.read().splitlines()

setuptools.setup(
    name="nfhc",
    version=NFHC_VERSION,
    author="Henrik Sanklef",
    author_email="hesa@sandklef.com",
    description="Naive FOSS Health Checker",
    long_description=_long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE',),
    url="https://github.com/hesa/nfhc",
    packages=['naive_foss_health', 'naive_foss_health.scrapers', 'naive_foss_health.output' ],
    entry_points={
        "console_scripts": [
            "nfhc = naive_foss_health.__main__:main",
        ],
    },
    package_data={
        'naive_foss_health': ['var/*.json'],
    },
    install_requires=requirements,
    extras_require={
        'dev': requirements_dev,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires='>=3.7',
)
