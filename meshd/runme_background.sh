# Primary Class Author : Mohammad
echo "Node in Created at $1"
python3 daemon.py --sensorport $1 >/dev/null 2>&1 &
echo "Start Sensors"
