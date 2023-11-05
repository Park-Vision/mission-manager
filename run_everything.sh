#!/usr/bin/bash

# run as root
# works on my machine ;D
gnome-terminal -e "docker run -it --net=host --env="DISPLAY" --volume="/run/user/1000/.mutter-Xwaylandauth.51D0B2:/home/akl/.Xauthority:rw" wnt3rmute/ardupilot-sitl ./sim_vehicle.py -v ArduCopter -N"
gnome-terminal -e "sudo /opt/kafka_2.13-3.6.0/bin/zookeeper-server-start.sh /opt/kafka_2.13-3.6.0/config/zookeeper.properties"
gnome-terminal -e "sudo /opt/kafka_2.13-3.6.0/bin/kafka-server-start.sh /opt/kafka_2.13-3.6.0/config/server.properties"
gnome-terminal -e "cd /home/szymon/development/parkvision/mission-manager && runuser -l szymon -c 'poetry run python mission-manager'"
gnome-terminal -e "cd /home/szymon/development/parkvision/parkvision-frontend && runuser -l szymon -c 'npm start'"
