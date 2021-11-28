echo "Node in Created at 33202"
python3 daemon.py --sensorport 33202
nohup python3 sensor/sensor_daemon.py --sensortype position --sensorport 33202
echo "Position sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport 33202
echo "Journey Timer sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype journey_finished --sensorport 33202
echo "Journey Finished sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype fuel --sensorport 33202
echo "Fuel sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype speed --sensorport 33202
echo "Speed sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype humidity --sensorport 33202
echo "Humidity sensor ready"
echo "Set up Temperature Sensor"