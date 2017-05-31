# Config for OpenHPC:1.3

* Source OBS:	https://build.openhpc.community
* Date copied:	Monday 8 May 2017
* Command run:	``./collect_obs_config https://build.openhpc.community config-OpenHPC:1.3 OpenHPC:1.3``

These are the config files as pulled from the openhpc OBS, which have then been modifed for ease of use.  
For the unmoddified versions, see ../config-OpenHPC:1.3-raw/  
For versions with intel compiler and IMPI removed see ../config-OpenHPC:1.3-nointel/


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

Added DOD to configs/EPEL7-deps/prj
>\+    \<download arch="aarch64" url="http://dl.fedoraproject.org/pub/epel/7/x86_64/" repotype="rpmmd"/>  
\+    \<download arch="x86_64" url="http://dl.fedoraproject.org/pub/epel/7/aarch64/" repotype="rpmmd"/>

Added DOD to 7.3 section of configs/CentOS/prj
>   \<repository name="7.3">  
\+    \<download arch="aarch64" url="http://mirror.centos.org/altarch/7.3.1611/os/aarch64/" repotype="rpmmd"/>  
\+    \<download arch="x86_64" url="http://mirror.centos.org/centos-7/7.3.1611/os/x86_64/" repotype="rpmmd"/>  
     \<arch>x86_64\</arch>  
\+    \<arch>aarch64\</arch>

Removed Aarch64 from 7.2 section of configs/CentOS/prj
>   \<repository name="7.2">  
     \<arch>x86_64\</arch>  
\-    \<arch>aarch64\</arch>


## Manual Additions required on OBS after applying config
In order to build most x86_64 packages, the required dependency .rpms will need to be manually downloaded into the :full directories in /srv/obs/build/ for:
* Licenses
* NonFree:PXSE:2017
* OPA:10.2.0.0.158	

Instead, if you do not require intel builds then
* Either: remove the "ifarch x86_64" section from the OpenHPC:1.3:Factory project config
* Or: Use the intel free "config-OpenHPC:1.3-nointel" instead

## Known Issues
Without resolving the intel dependencies, most x86_64 builds will fail.
