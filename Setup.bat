pyinstaller -y -F -i Assets\AuroraWrapper.ico -n Aurora_Wrapper -w --noupx --uac-admin Aurora.py
copy Tools\Aurora_Wrapper.exe.manifest dist\