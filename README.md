A command line interface written with Python 3. It provides easy access to [DigitalOcean](https://digitalocean.com) via their V2 API.
It depends on [koalalorenzo's python-digitalocean](https://github.com/koalalorenzo/python-digitalocean/) package.

How to use
==========
If you're on Windows, download the RAR archive and execute the exe file. If you installed Python on your system, you also install the
requirements and click the `digitaloceancli.py` file.

If you're on Linux distro, install requirements with `pip install -r requirements.txt` and run the program with `python3 digitaloceancli.py`.

Features
========
- List user's droplets
- List user's images
- Shutdown/Reboot/Poweron droplets
- Get droplet info
- Create droplet from user's image
- Destroy droplet
- Show account info