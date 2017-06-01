# Config for OpenHPC:1.3-nointel

* Source OBS:	https://build.openhpc.community
* Date copied:	Thursday 1 June 2017
* Command run:	``./collect_obs_config https://build.openhpc.community config-OpenHPC:1.3 OpenHPC:1.3``

These are the config files as pulled from the openhpc OBS, which have then been modifed for ease of use.  
For the unmoddified versions, see ../config-OpenHPC:1.3-raw/  
All intel and impi packages have been removed. For a version with them included see ../config-OpenHPC:1.3/


## Manual Edits already made to config after collection
This section is for information only. No action is required.

Fixed up configuration using:  
``for f in $(find configs -name prj); do sed -i -e 's/<releasetarget.*\/>//g; /<person userid="Admin".*\/>/b; s/<person userid=".*".*\/>//g' $f; done``  
``for f in $(find contents -name _aggregate); do sed -i -e 's/OpenHPC:1.2/OpenHPC:1.3/g' $f; done``  
``rm contents/OpenHPC:1.3:Factory/numactl/_link``  
``rm contents/OpenHPC:1.3:Factory/numpy-intel/_link``  
``for f in $(find contents -name _service); do sed -i -e 's/git@github.com:openhpc/http:\/\/github.com\/openhpc/g' $f; done``  
``for f in $(find contents -name _service); do sed -i '/changesauthor/d' $f; done``  
``for f in $(find contents -name _service); do sed -i '/changesgenerate/a \\    <param name=\"changesauthor\">Admin<\/param>' $f; done``

Removed Intel specific packages and repositories:  
``find contents -name "*intel*" -exec rm -fr {} \;``  
``find contents -name "*impi*" -exec rm -fr {} \;``  
``find pkg_configs -name "*intel*" -exec rm -fr {} \;``  
``find pkg_configs -name "*impi*" -exec rm -fr {} \;``  
``rm -fr configs/NonFree*``  
``rm -fr configs/OPA\:10.2.0.0.158``  
``rm -fr configs/Licenses``

Added DOD to EPEL7-deps and CentOS. Removed CentOS 7.2 for Aarch64. Removed Intel dependencies. Removed NonFree, OPA and licences from other projects:  
``patch -p2 < deps.patch``

## Manual Additions required on OBS after applying config
None.

## Known Issues
None.
