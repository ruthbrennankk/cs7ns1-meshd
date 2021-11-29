echo "Starting 2 background nodes and their sensors"
for (( i=1; i<=2; i++))
do
    echo "Node Sensor Port"
    echo j=$((i + $1))
    python3 daemon.py --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype position --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype temperature --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype journey_finished --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype fuel --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype speed --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype humidity --sensorport $1+$i </dev/null >/dev/null 2>&1 &
    echo "Node Created at $j"
done