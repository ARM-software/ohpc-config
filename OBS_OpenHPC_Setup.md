# OBS_OpenHPC_Setup.md
Instructions for creating an OBS instance ready for OpenHPC

Note: This setup has only been tried with OBS 2.8.  
Lines starting with $ should be entered on the command line.

## Install OBS

Install OBS using of of the following options:

#### 1. Install onto VM
Download ISO from http://openbuildservice.org/download/  
Note, the ISO works better than the vmdk/vdi/qcow2 images.  
Install onto machine/VM with at least 2 CPUs, 4 Gb of memory, 100Gb Disk  
Image will automatically connect to DNS upon start-up. Hostname will be "linux.suse".  
If your network automatically hands out new DNS leases, then the suggested method to change the hostname is to initially boot/install without network connected, edit /etc/hostname, then shutdown, connect networking and boot.

#### 2. Install onto existing server using package manager:
Find image at "Select Your Operating System" from http://openbuildservice.org/download/
TODO  


## Setup OBS command line

Create the .ssh dir  
``$ mkdir /usr/lib/obs/.ssh``  
If you require ssh keys for OBS to access your own git repos, then add them to /usr/lib/obs/.ssh/

Create a ssh certificate for the OBS server.  
Without doing this step you'll get insecure warnings when accessing the web gui  
TODO  

Enable auto start of ssh on boot  
``$ rcsshd start``  
``$ systemctl enable sshd.service``

Change root password (note the OBS usernames are different to the Linux usernames)

To the top of /etc/sysconfig/obs-server add the following:  
> OBS_SCHEDULER_ARCHITECTURES=“aarch64 x86_64” 

Add sudo (required)  
``$ zypper install sudo``

Now reboot the server

At this point the console should list the hostname of the OBS server at the login prompt. If it doesn't then **fix the networking before going any further**. OBS can get confused if the hostname changes later.

## Setup OBS GUI
Go to the address given on the console after boot and log in with Admin/opensuse

Change Admin password under Admin -> Change your password

As Admin, on the main page do:  
Configuration -> Interconnect -> OpenSUSE -> Save Changes  
Configuration -> Architectures -> Tick "Aarch64" -> Update

## Clone an OBS configuration
Whilst on a command line terminal on your OBS server

Clone the obs-cloner repo  
``$ git clone http://ds-gerrit.euhpc.arm.com:8008/hpc/openhpc/obs-cloner``  
``$ cd obs-cloner``

(Optional) Setup username/password for obs command line tool  
``$ osc -A https://localhost ls``  
You'll be asked for username/password. Preferably use Admin, however this will be cached as plaintext in /root/.oscrc.  
If you skip this step, it'll be performed as part of apply_obs_config

Apply a config
Choose a configuration set to use. It is recommended to use either config-OpenHPC:1.3 or config-OpenHPC:1.3-nointel if you do not require Intel Compiler / IMPI builds. See the README.md file inside each configuration directory for more details.  
``$ ./apply_obs_config config-OpenHPC:1.3``  
Warning: copying package contents may take many hours.  
Warning: If the script hangs forever printing asterix's whilst "waiting for server", then find current log dir and restart with:  
``./apply_obs_config -c -d /tmp/<previous_temp_dir> config-OpenHPC:1.3``

Remove constraint files (required until a fix is found).  
Some of the packages in OpenHPC have \_constraint files that specify workers require 3000 Mb memory. This includes gnu_compilers which is a pre-requisite for many packages. We have currently been unable to find the settings required to make these constraints pass. Therefore, for now it is recommended to run:  
``$ ./remove_constraints OpenHPC:1.3:Factory``  
``$ ./remove_constraints OpenHPC:1.3:Update1:Factory``


## Fix dependencies 
This is only required if OBS is running inside a network that cannot access the internet.  
OBS requires access to prebuilt packages for use whilst building. 

**SUSE dependencies**
Are normally resolved by using a SUSE interconnect which connects to openSUSE.org  
TODO: How do you fix this without openSUSE.org connections?
 
**CentOS dependencies**
Are normally resolved using "Download on demand". Alternatively, the .rprms can be copied manually.  
* Remove the "download" lines from https://MYOBSSERVER/project/meta/CentOS  
* scp/rsync all the x86_64 and aarch64 CentOS rpms to:  
/srv/obs/build/CentOS/7.3/x86_64/:full/  
/srv/obs/build/CentOS/7.3/aarch64/:full/  
* These rpms can be obtained from the packages/ dir on the given DOD link, eg http://mirror.centos.org/altarch/7.3.1611/os/aarch64/packages/
* Refresh the scheduler:  
``$ obs_admin --rescan-repository CentOS 7.3 x86_64``
``$ obs_admin --rescan-repository CentOS 7.3 aarch64``
* Repeat all the CentOS steps for EPEL7-deps - https://MYOBSSERVER/project/meta/EPEL7-deps

**Intel dependencies**  
This are not required if using config-OpenHPC:1.3-nointel
TODO


## OBS Worker installation

You'll need an x86 worker and an aarch64 worker. Each worker runs on a new machine/VM  
You will automatically get an x86 worker on the OBS server (as long as it has >1 CPU), but more can be added to speed up the build process.  
You'll need to explicitly add an aarch64 worker.  

To create a new worker, you'll need a machine/VM with installed opensuse 42.2:  
* Get the X86 SuSE image from: http://download.opensuse.org/distribution/leap/42.1/iso/  
* Get the Aarch64 image from: http://download.opensuse.org/ports/aarch64/factory/iso/  
* It should be possible to use RedHat/CentOS instead, but this has not been tested.  

On the new machine(s) you want to set up as a worker:

install obs-worker:  
``$ zypper addrepo http://download.opensuse.org/repositories/openSUSE:Tools/openSUSE_42.2/openSUSE:Tools.repo``    
``$ zypper refresh``  
``$ zypper install osc``  
``$ zypper install obs-service-tar_scm obs-service-format_spec_file obs-worker obs-service-extract_file obs-service-recompress obs-service-obs_scm-common obs-service-download_src_package obs-service-set_version obs-service-source_validator obs-service-download_url obs-service-verify_file obs-source_service obs-common obs-service-download_files obs-utils``  
``$ zypper install perl-XML-Structured``  

In /etc/sysconfig/obs-server set the following. Note, memory must be set to at least 3000  
> OBS_SCHEDULER_ARCHITECTURES=“aarch64 x86_64”  
OBS_INSTANCE_MEMORY="3000"  
OBS_SRC_SERVER="MYOBSSERVER:5352"  
OBS_REPO_SERVERS="MYOBSSERVER:5252"

Run:  
``$ ln -s /etc/sysconfig/obs-server /etc/buildhost.config``  
``$ systemctl restart obsworker.service``

Finally, on the OBS server, run:  
``$ rcobsscheduler restart``


## Start the builds

On the OBS server

Enable the builds. By default, most packages are disabled from building. You'll need to enable, either manually in the GUI, or:  
``$ ./enable_project_builds OpenHPC:1.3:Dep:Lmod``  
``$ ./enable_project_builds OpenHPC:1.3:Factory``  
``$ ./enable_project_builds OpenHPC:1.3:Update1:Factory``  

The OBS server should automatically resolve all dependencies (a package will be marked as "service" during this time) and start building. Check https://MYOBSSERVER/monitor and/or the files /srv/obs/log/scheduler_x86_64.log and /srv/obs/log/scheduler_aarch64.log


