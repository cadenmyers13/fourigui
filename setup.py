#!/usr/bin/env python

# Installation script for diffpy.'{{cookiecutter.package_name}}'

"""\
diffpy.fourigui - graphical interface for interfacing with 3D diffraction patterns
in reciprocal space

Packages:   diffpy.fourigui
Scripts:    fourgui -
"""

import os
import re
import sys

from setuptools import find_packages, setup

# Use this version when git data are not available, like in git zip archive.
# Update when tagging a new release.
FALLBACK_VERSION = "0.0.1.post0"

# versioncfgfile holds version data for git commit hash and date.
# It must reside in the same directory as version.py.
MYDIR = os.path.dirname(os.path.abspath(__file__))
versioncfgfile = os.path.join(MYDIR, "src/diffpy/fourigui/version.cfg")
gitarchivecfgfile = os.path.join(MYDIR, ".gitarchive.cfg")

# determine if we run with Python 3.
PY3 = sys.version_info[0] == 3


def gitinfo():
    from subprocess import PIPE, Popen

    kw = dict(stdout=PIPE, cwd=MYDIR, universal_newlines=True)
    proc = Popen(["git", "describe", "--match=v[[:digit:]]*"], **kw)
    desc = proc.stdout.read()
    proc = Popen(["git", "log", "-1", "--format=%H %ct %ci"], **kw)
    glog = proc.stdout.read()
    rv = {}
    rv["version"] = ".post".join(desc.strip().split("-")[:2]).lstrip("v")
    rv["commit"], rv["timestamp"], rv["date"] = glog.strip().split(None, 2)
    return rv


def getversioncfg():
    if PY3:
        from configparser import RawConfigParser
    else:
        from ConfigParser import RawConfigParser
    vd0 = dict(version=FALLBACK_VERSION, commit="", date="", timestamp=0)
    # first fetch data from gitarchivecfgfile, ignore if it is unexpanded
    g = vd0.copy()
    cp0 = RawConfigParser(vd0)
    cp0.read(gitarchivecfgfile)
    if len(cp0.get("DEFAULT", "commit")) > 20:
        g = cp0.defaults()
        mx = re.search(r"\btag: v(\d[^,]*)", g.pop("refnames"))
        if mx:
            g["version"] = mx.group(1)
    # then try to obtain version data from git.
    gitdir = os.path.join(MYDIR, ".git")
    if os.path.exists(gitdir) or "GIT_DIR" in os.environ:
        try:
            g = gitinfo()
        except OSError:
            pass
    # finally, check and update the active version file
    cp = RawConfigParser()
    cp.read(versioncfgfile)
    d = cp.defaults()
    rewrite = not d or (
        g["commit"]
        and (g["version"] != d.get("version") or g["commit"] != d.get("commit"))
    )
    if rewrite:
        cp.set("DEFAULT", "version", g["version"])
        cp.set("DEFAULT", "commit", g["commit"])
        cp.set("DEFAULT", "date", g["date"])
        cp.set("DEFAULT", "timestamp", g["timestamp"])
        with open(versioncfgfile, "w") as fp:
            cp.write(fp)
    return cp


versiondata = getversioncfg()

with open(os.path.join(MYDIR, "README.rst")) as fp:
    long_description = fp.read()


def dest(p):
    return os.path.normpath(p.replace("_build", ""))


def datafiles_html():
    rv = [
        (dest(t), [os.path.join(t, f) for f in fl])
        for t, d, fl in os.walk("doc/manual/_build/html")
    ]
    return rv


def datafiles_examples():
    rv = [(t, [os.path.join(t, f) for f in fl]) for t, d, fl in os.walk("doc/examples")]
    return rv


# define distribution
setup_args = dict(
    name="diffpy.fourigui",
    version=versiondata.get("DEFAULT", "version"),
    packages=find_packages(os.path.join(MYDIR, "src")),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["six"],
    entry_points={
        # define console_scripts here, see setuptools docs for details.
        "console_scripts": [
            "fourigui=diffpy.fourigui:main",
        ],
    },
    author="Simon J.L. Billinge",
    author_email="sb2896@columbia.edu",
    maintainer="'Sani Harouna-Mayer',",
    maintainer_email="sharonna@physnet.uni-hamburg.de",
    # TODO update descriptions
    description="Tool for visualizing 3D diffraction and PDF Images",
    long_description="{{cookiecuttter.long_description}}",
    long_description_content_type="text/plain",
    license="License granted by Columbia University, see LICENSENOTICE.txt",
    url="https://www.diffpy.org/",
    keywords="PDF X-ray neutron Fourier transform",
    classifiers=[
        # List of possible values at
        # http://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)

if __name__ == "__main__":
    setup(**setup_args)

# End of file
