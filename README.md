# CHIMA: CHain Installation, Monitoring and Adjustment

This repository contains a prototype of CHIMA, a framework for the deployment of heterogeneous Service Function Chains whose performance can be guaranteed through the use of runtime redeployments and monitoring with In-band Network Telemetry.

## Installation
This software and its dependencies have been tested on a fresh install of Ubuntu 20.04 LTS

- Clone this repository
```
cd
git clone https://github.com/simotone97/CHIMA
cd CHIMA
```

- Install FOP4 dependencies
    - Be aware that this process may take a very long time, probably one hour. If this is run in a VM you may want to assign an appropriate number of cores to it, since it involves compiling different packages
    - As described in FOP4's readme, at least 2GB of RAM and 12GB of FREE disk space are required
```
./install/fop4/install-dependencies.sh
```

- Install FOP4
```
./install/fop4/install-fop4.sh
cd ~/CHIMA
```

- Install ONOS
```
./install/onos/install-onos.sh
```

- Install Framework
```
./install/framework/install-framework.sh
```

- Install InfluxDB
```
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.9-amd64.deb
sudo dpkg -i influxdb2-2.0.9-amd64.deb
```
- Start the service
```
sudo service influxdb start
```
- The service should run automatically at every restart. You can restart and check with
```
sudo service influxdb status
```
- InfluxDB starts a webserver at localhost:8086. If you use Vagrant you should add a portforwarding into your Vagrantfile. For example add this line
```
config.vm.network :forwarded_port, host: 4567, guest: 8086
```
- Open the webserver at localhost:4567 and create an access account, a bucket called "COLLECTOR", organization called "PoliMi" and an API key for full access. Copy this key and add it as an environmental variable
```
sudo nano /etc/environment
```
- Then add in a new line the following
```
INFLUXDB_TOKEN=your_API_key_value
```
- Install telegraf
```
cd
# influxdata-archive_compat.key GPG fingerprint:
#     9D53 9D90 D332 8DC7 D6C8 D3B9 D8FF 8E1F 7DF8 B07E
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update && sudo apt-get install telegraf
```
- Log out of your current session and log back in to ensure the correct loading of groups, environment variables and bash profile


## Running tests
After all the installation steps have been completed, tests can be executed.

### Running ONOS
- Start ONOS with the correct set of applications
```
cd $CHIMA_ROOT
./run-onos.sh
```

- Wait for ONOS to complete its startup process

- Build and install the CHIMAStub application from a different terminal
```
cd $CHIMA_ROOT/chima-stub
make
```

### Running tests
- Run the "pre" expect script for the system to be correctly setup. This step is only needed once.
```
cd $CHIMA_ROOT/measurements
sudo -E ./pre.exp
```

- Run telegraf
```
sudo telegraf --config telegraf.conf
```

- Run desired tests using the provided expect script, with configurable parameters
```
sudo -E ./test.exp [topology] [polling interval] [ewma coefficent]
```

The available topologies are the following:
- minimal
- medium
- large
- concentrated
- datacenter
- mesh
- unbalanced

Here is an example command to run a test on the _minimal_ topology:
```
sudo -E ./test.exp minimal 3 3
```

### Collecting results
After a test is completed, its results can be found in the `$CHIMA_ROOT/measurements/Times` directory.
Text files containing the recorded measurements are named according to the timestamp at which they are generated, the name of the used topology, and the value of the two parameters. It is also possible to explore the telemetry data at localhost:4567
