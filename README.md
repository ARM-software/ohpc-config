# ohpc-config
Scripts and config files for recreating an OpenHPC OBS instance.

OpenHPC ( http://www.openhpc.community/ ) is a collaborative, community effort that initiated from a desire to aggregate a number of common ingredients required to deploy and manage High Performance Computing (HPC) Linux clusters including provisioning tools, resource management, I/O clients, development tools, and a variety of scientific libraries. Packages provided by OpenHPC have been pre-built with HPC integration in mind with a goal to provide re-usable building blocks for the HPC community.

OpenHPC is built using OBS (Open Build Server) at https://build.openhpc.community/. The builds pull in spec files and patches directly from https://github.com/openhpc/ohpc

This repository contains instructions and scripts for reproducing your own instance of the OpenHPC repository. 

In most instances, a complete recreation of OpenHPC will be unnecessary, and users should first consider creating a fork on the OpenHPC OBS in a private home directory.

In order to reproduce OpenHPC, this repository contains configuration data scraped directly from the live OpenHPC build server, in both raw and modified versions. This data is not contained in the OpenHPC github repository.

# License
This project is licensed under Apache-2.0.


# Contents

**OBS_OpenHPC_Setup.md**
* Instructions for creating an OpenHPC OBS clone from scratch. These instructions require minimal effort, but assume a basic familiarity with Linux administration. The main apply step with take a couple of hours to run, and the final builds themselves many hours more.

**config-OpenHPC:1.3-raw/**
* The unmodified configuration data pulled directly from the OpenHPC OBS. See its README.md file for more details. 

**config-OpenHPC:1.3/**
* The same configuration data, but modified to make it suitable for quick application onto a clean OBS. See its README.md file for more details. 

**config-OpenHPC:1.3-nointel/**
* The modified configuration data, but with all the intel compiler and IMPI packages removed. See its README.md file for more details. 

**collect_obs_config**
* Script for collecting an OpenHPC configuration. The configuration data above was pulled using this script.

**apply_obs_config**
* Script for applying an OpenHPC configuration obtained using collect_obs_config.

**enable_project_builds**
* Script for enabling the builds for all the packages in a given project.

**remove_constraints**
* Script for removing the build constraints for all the packages in a given project.

