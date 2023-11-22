FROM archlinux:latest

RUN pacman -Syu base-devel git python python-pip python-setuptools gcc procps-ng xterm wget tk python-wxpython python-numpy --noconfirm && pacman -Sc --noconfirm

# Create a user
RUN useradd -m parkvision

RUN echo "parkvision ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# From this point, the container runs as the `parkvision` user is logged in
USER parkvision
WORKDIR /home/parkvision
RUN pip install wheel pymavlink mavproxy opencv-python empy pexpect --no-cache-dir --break-system-packages

# From now on, following the official guide: https://github.com/ArduPilot/ardupilot/blob/master/BUILD.md
RUN git clone --recursive https://github.com/ArduPilot/ardupilot.git --depth 1
WORKDIR /home/parkvision/ardupilot

RUN ./waf configure
RUN ./waf copter

FROM archlinux:latest

RUN pacman -Syu gcc procps-ng git python python-pip python-setuptools xterm wget tk python-wxpython python-numpy --noconfirm && pacman -Sc --noconfirm

RUN useradd -m parkvision
RUN mkdir /home/parkvision/ardupilot
RUN pip install opencv-python wheel pymavlink mavproxy pexpect matplotlib --no-cache-dir --break-system-packages

COPY --from=0 /home/parkvision/ardupilot /home/parkvision/ardupilot

USER parkvision
WORKDIR /home/parkvision/ardupilot/Tools/autotest

# Custom ParkVision locations
RUN echo "Legnicka=16.99042,51.11818,120,0" >> locations.txt
RUN echo "Janiszewskiego=51.10975,17.05911,120,0" >> locations.txt
RUN echo "Wronskiego=51.10891,17.05562,120,0" >> locations.txt

# Disable pre-arm checks to reduce startup time
# https://ardupilot.org/copter/docs/common-prearm-safety-checks.html
RUN echo "ARMING_CHECK    0" >> default_params/plane.parm
RUN echo "ARMING_CHECK    0" >> default_params/copter.parm
