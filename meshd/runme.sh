# PORT RANGE
# 33000 -

# START SYNC/PEER NODE
python3 daemon.py --sensorport 33215
# START SYNC/PEER NODE - with sensor status
python3 daemon.py --sensorport 33215 --printsensors True

# START GENERATION/SENSOR NODE
python3 sensor/sensor_daemon.py --sensortype position --sensorport 33215
# TYPE OPTIONS
# [temperature, journey_elapsed, journey_finished, fuel, package_id, speed, humidity]

echo "Starting 2 background nodes and their sensors"
j=0
for (( i=1; i<=2; i++))
do
    echo "Node Sensor Port"
    j=$((i + $1))
    python3 daemon.py --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype position --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype temperature --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype journey_elapsed --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype journey_finished --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype fuel --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype speed --sensorport $j </dev/null >/dev/null 2>&1 &
    python3 sensor/sensor_daemon.py --sensortype humidity --sensorport $j </dev/null >/dev/null 2>&1 &
    echo "Node Created at $j"
done
