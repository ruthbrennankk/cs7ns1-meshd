## CS7NS1 Project 3 - 2021/22
Group Members; Chao Lin, Mohammad Mahdi Eslami, Ruth Brennan and Anton Yamkovoy

### Scenario
Our network is set up to emulate delivery robots that operate inside a warehouse. 
Each robot has an individual sync node, which is responsible for discovering, forming connections and forwarding 
information with/to other sync nodes. Each sync node has 8 sensor nodes that report information about itself to it, with 
a level of alert related to the contents of the information. Each sensor reports on a unique area of information; 
position, journey status, temperature, fuel, package id, speed and humidity.
The sync nodes discover each other via multicast, form a socket connection and add each other to a list of peers. When 
they receive information from their sensor nodes, they forward this information to each peer in their peer table.
In terms of scaling this system, it would involve bridge/gateway nodes to other pods of robot nodes. These bridge nodes would 
elect themselves through multicast in which worker nodes would be made aware of their existence. This bridge nodes would 
forward information from their own pods to other pod's bridge nodes. Upon receiving outside pod information a bridge node
would distribute it to its own pod sensibly.

### Execution Instructions
A sync node can be started by executing the runme_node script and passing a sensor port number. 
This port number is where the sync node listens for its sensors.
```
./runme_node.sh 33210
```
To start a sensor node and view it's terminal output, execute the following command. Where sensor type specifies the data that this sensor node 
will generate. The options are; position, journey_elapsed, temperature, journey_finished, fuel, package_id, speed and humidity
Note that a sensor node can only start when it has a sync node to communicate with, so it is expected that the passed 
sensor port corresponds to the port that a running sync node is listening for sensors at.
```angular2html
python3 sensor_daemon.py --sensortype package_id  --sensorport 33210
```
To start all of the sensors for a sync node, and have them run in the background, use of sensor script 
```
./runme_sensors.sh 33210
```

We also provide a background script that will start a node and execute it in the background, you will need to also run 
the sensors script for this node
```
./runme_background.sh 33211
```

### File Setup
The daemon file acts as the driver script for sync node execution. It sets up the threads and establishes a sync node setup.
The multicast file implements the discovery functionality for sync nodes. The protocol layer is implemented in the connection,
manager and server files. The transport layer is implemented in the transport file. Finally, the sign file is a collection of 
utils functions.

The files corresponding to our sensors nodes are sensor_daemon and sensor. Sensor_daemon is used to set up a sensor node 
whereas the node functionality is implemented in the sensor script.
