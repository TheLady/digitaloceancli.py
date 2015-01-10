from cx_Freeze import setup, Executable

setup(
    name='DigitalOceanCLI',
    version="0.1",
    author="Yusuf Tuğrul Kocaman",
    author_email="ytugrultr@gmail.com",
    description="DigitalOcean Command Line Interface",
      executables= [Executable(base="Console", script="digitaloceancli.py"
                               , targetName="DigitalOceanCLI.exe", compress=True)],
      options={'build.exe':{'packages':[],'includes':[]}})
