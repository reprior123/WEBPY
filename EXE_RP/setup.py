from distutils.core import setup, Extension
import distutils.sysconfig
sysconfig = distutils.sysconfig.get_config_vars()
import os, sys

setup(name="pycheckbook",
      version = "0.52",
      description = "Python checkbook manager",
      author = "Rick Muller",
      author_email = "rpm@wag.caltech.edu",
      url = "http://pycheckbook.sourceforge.net",
      licence = "GPL",
      packages = ["pycheckbook"],
      scripts = ["PyCheckbook.py"]
      )

