echo "Starting 2 background nodes and their sensors"
for (( i=1; i<=2; i++ ))
do
    python3 daemon.py --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    echo "Node in Created at"
    echo 3321$i
    python3 sensor/sensor_daemon.py --sensortype position --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype temperature --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype journey_finished --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype fuel --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype speed --sensorport 3321$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype humidity --sensorport 3321$i </dev/null >/dev/null 2>&1 &
done