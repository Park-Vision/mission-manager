# Run ardupilot SITL in docker + zookeeper + kafka

gnome-terminal -e "docker run -it --net=host --env="DISPLAY" --volume="/run/user/1000/.mutter-Xwaylandauth.51D0B2:/home/akl/.Xauthority:rw" wnt3rmute/ardupilot-sitl ./sim_vehicle.py -v ArduCopter -N"
gnome-terminal -e "sudo /opt/kafka_2.13-3.6.0/bin/zookeeper-server-start.sh /opt/kafka_2.13-3.6.0/config/zookeeper.properties"
gnome-terminal -e "sudo /opt/kafka_2.13-3.6.0/bin/kafka-server-start.sh /opt/kafka_2.13-3.6.0/config/server.properties"
gnome-terminal -e "/opt/kafka_2.13-3.6.0/bin/kafka-console-consumer.sh --topic drones-info --from-beginning --bootstrap-server localhost:9092"