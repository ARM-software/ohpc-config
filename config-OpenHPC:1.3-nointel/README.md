# Config for OpenHPC:1.3-nointel

* Source OBS:	https://build.openhpc.community
* Date copied:	Monday 8 May 2017
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

Removed Intel dependencies in configs/OpenHPC:1.3:Factory/prjconf
> -# PXSE 2017  
-#%ifarch x86_64
-#Runscripts: intel-mkl-common-098  
-#Order: intel-mkl-098:intel-compilers-devel-ohpc  
-#Preinstall: intel-ifort-l-ps-098  
-#Preinstall: intel-icc-l-all-098  
-#Preinstall: intel-comp-l-all-vars-098  
-#Preinstall: intel-icc-l-all-common-098  
-#Preinstall: intel-mkl-098  
-#Preinstall: intel-mkl-rt-098  
-#Preinstall: intel-mkl-common-098  
-#Preinstall: intel-mkl-common-c-098  
-#Preinstall: intel-mkl-ps-cluster-rt-098  
-#Preinstall: intel-mpi-psxe-035  
-#Preinstall: intel-mpi-rt-core-098  
-#Preinstall: intel-mpi-sdk-core-098  
-#Prefer: intel-openmp-l-ps-ss-bec-098  
-#Prefer: intel-mkl-rt-098  
-#Prefer: intel-openmp-l-all-098  
-#%endif  
-# PXSE 2016-u3  
-#%ifarch x86_64  
-#Preinstall: intel-ifort-l-ps-devel-210  
-#Preinstall: intel-icc-l-all-210  
-#Preinstall: intel-comp-l-all-vars-223  
-#Preinstall: intel-compxe-pset  
-#Preinstall: intel-mkl-210  
-#Preinstall: intel-mkl-common-210  
-#Preinstall: intel-mpi-psxe-068  
-#Preinstall: intel-mpi-rt-core-223  
-#Preinstall: intel-mpi-sdk-core-223  
-#%endif

Removed NonFree, OPA and licences from both configs/OpenHPC:1.3:Factory/prj and configs/OpenHPC:1.3:Update1:Factory/prj
> \-    \<path project="OPA:10.2.0.0.158" repository="SLE_12_SP1"/>  
\-    \<path project="NonFree:PXSE:2017" repository="SLE_12_SP1"/>  
\-    \<path project="NonFree:PXSE:2017" repository="CentOS_7.2"/>  
\-    \<path project="Licenses" repository="standard"/>

Removed Intel specific packages and repositories:  
``find contents -name "*intel*" -exec rm -fr {} \;``  
``find contents -name "*impi*" -exec rm -fr {} \;``  
``find pkg_configs -name "*intel*" -exec rm -fr {} \;``  
``find pkg_configs -name "*impi*" -exec rm -fr {} \;``  
``rm -fr configs/NonFree\:PXSE\:2017``  
``rm -fr configs/OPA\:10.2.0.0.158``  
``rm -fr configs/Licenses``

## Manual Additions required on OBS after applying config
None.

## Known Issues
None.
