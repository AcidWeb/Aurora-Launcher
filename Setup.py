from cx_Freeze import setup, Executable

extra_options = dict(
    options={"build_exe": {"optimize": 2,
                           "include_files": [['Tools/Aurora_Wrapper.exe.manifest', 'Aurora_Wrapper.exe.manifest']],
                           "copy_dependent_files": True,
                           "create_shared_zip": False,
                           "append_script_to_exe": True,
                           "replace_paths": '*=',
                           "excludes": ['tkinter']}},
    executables=[Executable("Aurora.py",
                            base="Win32GUI",
                            targetName="Aurora_Wrapper.exe",
                            icon="Assets/Aurora.ico",
                            compress=False)])

setup(
    name="Aurora Wrapper",
    version="1.0",
    author="Pawel Jastrzebski",
    author_email="pawelj@vulturis.eu",
    license="GPL-3",
    **extra_options
)