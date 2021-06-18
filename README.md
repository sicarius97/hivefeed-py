# hivefeed-py
The purpose of this program is to establish a pricefeed for Hive witnesses. It is a lightweight implementation written in python that pulls an aggregated Hive to USD price from coingecko, formats the data, and uses the beempy library to build a transaction to be submitted to a Hive api.

## Required Pkgs
Currently, the easiest way to setup and establish this price feed is to use miniconda3 to easily reproduce the necessary environment. An even easier docker implementation will be coming soon.

hivefeed-py requires python3 and the following python packages:

- requests
- beem

## Setup Instructions
As mentioned above, the setup is easiest with miniconda3/anaconda3, however, if you prefer to use pip it can also be used. Instructions for pip and requirements.txt will not be provided.

### Install miniconda3
Miniconda3 can be installed here: https://docs.conda.io/en/latest/miniconda.html

### Clone git repo

Open terminal and follow along with provided cmds

Paste command below to clone git repo

`git clone https://github.com/sicarius97/hivefeed-py.git`

### Use miniconda3 to install necessary pkgs within repo and activate environment

Set repo as working directory:

`cd hivefeed-py`

Use conda pkg manager to create an environment in envs directory within repo with necessary packages from provided environment.yml:

`conda env create --prefix ./envs --file environment.yml`

Activate environment, you will know it is activated as terminal will now be prefixed with (<environment name>):

`conda activate ./envs`

### Setup program

Setup for the hivefeed is pretty simple. First copy the sample json config like so:

`cp sample.config.json config.json`

Open config.json for editing:

`nano config.json`

Insert the active key for the witness owner in the empty parenthesis in the json file and edit the witness name to reflect the name of your witness. You can also set the publish interval in seconds within the config.json file. By default it is set to 900, or about 15 mins.

You can also set the variables directly in hivefeed.py, but I would recommend keeping your secrets in the ignored config.json if you plan to push your configuration back to a public repo to avoid uploading secret keys.

### Run program

After activating the environment, the program can be run with the command:

`python hivefeed.py`

The program can be exited via the ctrl^C keypress or via other termination methods. It is set up with an elegant timeloop that will send a soft kill signal when it is interrupted by either the user or another process.

Feel free to fork, improve, submit merge requests, etc!

