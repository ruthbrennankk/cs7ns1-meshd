echo "---FOUR NODES IN BACKGROUND---"
for (( i=1; i<=4; i++ ))
do
    nohup python3 daemon.py --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    echo "Node in Created at"
    echo 3321$i
    nohup python3 sensor/sensor_daemon.py --sensortype position --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype temperature --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype journey_finished --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype fuel --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype speed --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype wind --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    nohup python3 sensor/sensor_daemon.py --sensortype humidity --sensorport 3321$i </dev/null >/dev/null 2>&1 &
done

echo "---ONE NODE IN FOREGROUND---"
echo "Node in Created at"
echo 33215
python3 daemon.py --sensorport 33215
nohup python3 sensor/sensor_daemon.py --sensortype position --sensorport 33215
echo "Position sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype temperature --sensorport 33215
echo "Temperature sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport 33215
echo "Journey Timer sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype journey_finished --sensorport 33215
echo "Journey Finished sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype fuel --sensorport 33215
echo "Fuel sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype speed --sensorport 33215
echo "Speed sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype wind --sensorport 33215
echo "Wind sensor ready"
nohup python3 sensor/sensor_daemon.py --sensortype humidity --sensorport 33215
echo "Humidity sensor ready"
