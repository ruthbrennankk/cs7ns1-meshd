# Primary Class Author : Mohammad, Secondary: Ruth
python3 sensor_daemon.py --sensortype position --sensorport $1 > /dev/null 2>&1 &
echo "Position sensor ready"
python3 sensor_daemon.py --sensortype journey_elapsed --sensorport $1 > /dev/null 2>&1 &
echo "Temperature sensor ready"
python3 sensor_daemon.py --sensortype temperature --sensorport $1 >/dev/null 2>&1 &
echo "Journey Timer sensor ready"
python3 sensor_daemon.py --sensortype journey_finished --sensorport $1 > /dev/null 2>&1 &
echo "Journey Finished sensor ready"
python3 sensor_daemon.py --sensortype fuel --sensorport $1 > /dev/null 2>&1 &
echo "Fuel sensor ready"
python3 sensor_daemon.py --sensortype package_id  --sensorport $1 > /dev/null 2>&1 &
echo "Packet sensor ready"
python3 sensor_daemon.py --sensortype speed --sensorport $1 > /dev/null 2>&1 &
echo "Speed sensor ready"
python3 sensor_daemon.py --sensortype humidity --sensorport $1 > /dev/null 2>&1 &
echo "Humidity sensor ready"
