
<h1>How to setup Ewatercycle package on Windows in Pycharm (Using commandline)</h1>

<h3>Download WSL for windows</h3>

Windows Powershell:
wsl --install

Refresh Windows Powershell

Open WSL:
Windows Powershell: wsl

<h3>Download conda on WSL</h3>

In WSL, run:

- wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

- bash Miniconda3-latest-Linux-x86_64.sh

**Refresh Windows Powershell And Open WSL Again**

In WSL run:

- conda init

- rm Miniconda3-latest-Linux-x86_64.sh

<h3>Create ewatercycle conda environment.</h3>

Make sure environment.yml is in the project file. (Should be when this is merged)

If environment.yml is not in the project folder then navigate to the project folder in WSL (using: cd [next folder]),
then run in WSL: wget https://raw.githubusercontent.com/eWaterCycle/ewatercycle/main/environment.yml

- conda install mamba -n base -c conda-forge -y

- mamba env create --file environment.yml

- conda activate ewatercycle

<h3>Download the ewatercycle package into the ewatercycle conda environment.</h3>
While the ewatercycle conda environment is activated (conda activate ewatercycle) run:

- pip install ewatercycle ewatercycle-hype ewatercycle-lisflood ewatercycle-marrmot ewatercycle-pcrglobwb ewatercycle-wflow  ewatercycle-leakybucket

<h3> Setup config for esmvaltool </h3>

While the ewatercycle conda environment is activated (conda activate ewatercycle) run:

- esmvaltool config get_config_user

<h3> Install and setup era5cli </h3>

While the ewatercycle conda environment is activated (conda activate ewatercycle) run:

- pip install era5cli

To get access to the data go to https://cds.climate.copernicus.eu/user/register?destination=%2F%23!%2Fhome

Create an account and login

Click on your profile (top right)

Find your UID and API Key at the bottom of the page and use them in the following command

Run in ewatercycle env: 

- era5cli config --uid ID_NUMBER --key "KEY"

<h3> Install Docker for WSL </h3>

Run: 

- sudo apt update && sudo apt upgrade

- sudo apt install --no-install-recommends apt-transport-https ca-certificates curl gnupg2

- update-alternatives --config iptables

- . /etc/os-release

- curl -fsSL https://download.docker.com/linux/${ID}/gpg | sudo tee /etc/apt/trusted.gpg.d/docker.asc

- echo "deb [arch=amd64] https://download.docker.com/linux/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list

- sudo apt update

- sudo apt install docker-ce docker-ce-cli containerd.io

- sudo groupadd docker

- sudo usermod -aG docker $USER

<h3> Pull model images </h3>

- docker pull ewatercycle/lisflood-grpc4bmi:20.10

- docker pull ewatercycle/marrmot-grpc4bmi:2020.11

- docker pull ewatercycle/pcrg-grpc4bmi:setters

- docker pull ewatercycle/wflow-grpc4bmi:2020.1.1

- docker pull ewatercycle/wflow-grpc4bmi:2020.1.2

- docker pull ewatercycle/wflow-grpc4bmi:2020.1.3

- docker pull ewatercycle/hype-grpc4bmi:feb2021

- docker pull ghcr.io/ewatercycle/leakybucket-grpc4bmi:v0.0.1

- docker pull ghcr.io/ewatercycle/sfincs-bmiserver:sfincs-v2.0.2-blockhaus-release-q2-2023

<h2> Pycharm Setup</h2>

Open your gitlab repo in pycharm.

Click on Python Interpreter (bottom right) 
-> Add New Interpreter 
-> On WSL 
-> Next 
-> Conda Environment 
-> Select ewatercycle

<h3> Setup WSL Terminal in Pycharm (Optional) </h3>

Press CTRL + ALT + S to open Settings

Go to Tools -> Terminal

Put wsl.exe as the Shell Path

Press Apply










