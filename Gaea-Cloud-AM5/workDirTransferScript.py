#!/usr/bin/env python3
## \date November 7, 2023
## \author Bennett Chang
## \email bennett.chang@noaa.gov
## \description Retrieves work directory from /am5xml/ and initiates transfer via Globus CLI to cloud.

import io
import subprocess

global cloud
cloud = 'aa0a5eb9-3d07-495b-a04a-1a64fdf6a3e8'

global gaea
gaea = 'be56688a-99e0-11ea-8eca-02c81b96a709'

global cloudDir
cloudDir = "gfdl-none-cz-c4-id/am5/gaea_codeTransfer"

# make sure Globus CLI and fre/bronx-20 modules are loaded before executing script, and use Python version 3.7 or later 
# make sure user is signed into Globus CLI, can check with `globus whoami`

# fre commands needed to obtain directory path, Globus CLI command needed to execute transfer
def executeCommands():
    # get experiment name by using frelist
    frelistCommand = "frelist -x am5.xml -p ncrc5.intel23-classic -t prod-openmp"
    getExperimentName = subprocess.run(frelistCommand, stdout=subprocess.PIPE, text=True, shell=True, check=True)
    output_lines = getExperimentName.stdout.splitlines()
    experimentName = output_lines[0]
    
    # use experiment name and frelist again to obtain source directory for experiment
    experimentCommand = f"frelist -x am5.xml -p ncrc5.intel23-classic -t prod-openmp -d src {experimentName}"
    getSourceDir = subprocess.run(experimentCommand, stdout=subprocess.PIPE, text=True, shell=True, check=True)
    sourceDir = getSourceDir.stdout.strip()

    # run fremake with --force-checkout (-f) flag
    freMakeCommand = f"fremake --force-checkout -x am5.xml -p ncrc5.intel23-classic -t prod-openmp {experimentName}"
    runFreMake = subprocess.run(freMakeCommand, stdout=subprocess.PIPE, text=True, shell=True, check=True)

    # use Globus CLI to initiate transfer from AM5 experiment's source directory within gaea to cloud
    transferCommand = f"globus transfer {gaea}:{sourceDir} {cloud}:{cloudDir} --recursive --preserve-mtime"
    runGlobusTransfer = subprocess.run(transferCommand, stdout=subprocess.PIPE, text=True, shell=True, check=True)
    showGlobusCommand = "globus task list"
    showGlobusTransfer = subprocess.run(showGlobusCommand, stdout=subprocess.PIPE, text=True, shell=True, check=True)
    globusTasks = showGlobusTransfer.stdout
    print(globusTasks)

if __name__ == '__main__':
    executeCommands()