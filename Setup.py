VERSION = "1.2.1"

import py2exe
from distutils.core import setup
additional_files = [('', ['Tools/Aurora_Wrapper.exe.manifest'])]
extra_options = dict(
    options={'py2exe': {"bundle_files": 2,
                        "dist_dir": "dist",
                        "compressed": True,
                        "optimize": 2}},
    windows=[{"script": "Aurora.py",
              "dest_base": "Aurora_Wrapper",
              "version": VERSION,
              "copyright": "Pawel Jastrzebski © 2014",
              "legal_copyright": "GNU General Public License (GPL-3)",
              "product_version": VERSION,
              "product_name": "AuroraWrapper",
              "file_description": "AuroraWrapper",
              "icon_resources": [(1, "Assets\Aurora.ico")]}],
    zipfile=None,
    data_files=additional_files)


setup(
    name="Aurora Wrapper",
    version=VERSION,
    author="Pawel Jastrzebski",
    author_email="pawelj@vulturis.eu",
    license="GPL-3",
    **extra_options
)