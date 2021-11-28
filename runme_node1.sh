echo "Node in Created at 33201"
python3 meshd/daemon.py --sensorport 33201
nohup python3 meshd/sensor/sensor_daemon.py --sensortype position --sensorport 33201
echo "Position sensor ready"
nohup python3 meshd/sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport 33201
echo "Journey Timer sensor ready"
nohup python3 meshd/sensor/sensor_daemon.py --sensortype journey_finished --sensorport 33201
echo "Journey Finished sensor ready"
nohup python3 meshd/sensor/sensor_daemon.py --sensortype fuel --sensorport 33201
echo "Fuel sensor ready"
nohup python3 meshd/sensor/sensor_daemon.py --sensortype speed --sensorport 33201
echo "Speed sensor ready"
nohup python3 meshd/sensor/sensor_daemon.py --sensortype humidity --sensorport 33201
echo "Humidity sensor ready"
echo "Set up Temperature Sensor"
#nohup python3 meshd/sensor/sensor_daemon.py --sensortype temperature --sensorport 33201