# PORT RANGE


# START SYNC/PEER NODE
python3 daemon.py --sensorport 33215
# START SYNC/PEER NODE - with sensor status
python3 daemon.py --sensorport 33215 --printsensors True

# START GENERATION/SENSOR NODE
python3 sensor/sensor_daemon.py --sensortype position --sensorport 33215
# TYPE OPTIONS
# [temperature, journey_elapsed, journey_finished, fuel, speed, humidity]


