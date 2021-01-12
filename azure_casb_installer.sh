#!/bin/bash

username=""
password=""
java_version=8
while test $# -gt 0
 do
  case "$1" in
  -username)
    shift
    username=$1
    shift
    ;;
  -password)
    shift
    password=$1
    shift
    ;;
  -java_version)
    shift
    ava_version=$1
    shift
    ;;
  *)
    echo "$1 is not a recognized flag!"
    exist 1;
    ;;
  esac
  done
if [ "$username" = "" ]
then
  echo "ERROR: Please Enter your CASB username using -username flag"
  exit 1
fi

if [ "$password" = "" ]
then
  echo "ERROR: lease Enter your CASB password  using -password flag"
  exit 1
fi

sudo apt install software-properties-common -y

wget -qO - http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_17.04/Release.key | sudo apt-key add -
sudo add-apt-repository 'deb http://download.opensuse.org/repositories/home:/laszlo_budai:/syslog-ng/xUbuntu_17.04 ./'
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
# install python
sudo apt-get install -y python3.8  python3.8-distutils
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8.1
sudo apt install unzip -y
sudo apt-get install python -y
apt install libcurl4 -y
apt install curl -y
echo "installing openjdk-8-jdk"
sudo apt install openjdk-8-jdk -y
echo 'export JAVA_HOME=usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
echo "Replacing rsyslog service with syslog-ng service"
sudo systemctl stop rsyslog.service
sudo systemctl disable rsyslog.service
sudo apt-get install syslog-ng syslog-ng-core -y
sudo systemctl enable syslog-ng.service
sudo systemctl start syslog-ng.service
# check if settings file is exists
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SETTINGS_FILE=$DIR/settings.yml

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "The settings file:$SETTINGS_FILE does not exist"
    exit 1
fi
# create required directories
APPLICATION_DIRECTORY="$(python3 "$DIR"/installer_helper.py "$SETTINGS_FILE")"
# shellcheck disable=SC2006
SIEM_FILE=`ls SIEM*.zip 2> /dev/null`
# shellcheck disable=SC2181
if [ $? != 0 ]; then
    echo "No SIEM-Tool-Linux-<date>.zip found"
    exit 1
fi
if [ ! -f "$SIEM_FILE" ]; then
    echo "The SIEM Tool zip file:$SIEM_FILE does not exist"
    exit 1
fi

TRUSTSTORE_FILE="$DIR"/truststore
if [ ! -f "$TRUSTSTORE_FILE" ]; then
    echo "The settings file:$TRUSTSTORE_FILE does not exist"
    exit 1
fi
cp -r ./* "$APPLICATION_DIRECTORY"
mkdir "$APPLICATION_DIRECTORY"/LOGS_BUFFER
cd "$APPLICATION_DIRECTORY" || exist 1
unzip "$SIEM_FILE"
rm "$SIEM_FILE"
chmod a+x "$APPLICATION_DIRECTORY"/scripts/*
echo "Creating credentials file.."
python3 "$DIR"/cli_controller.py  credentials --username "$username" --password "$password" -c "$SETTINGS_FILE"
# shellcheck disable=SC2181
if [ $? != 0 ]; then
    exit 1
fi
echo "Installing azure agent.."
python3 "$DIR"/install_azure_agent.py "$SETTINGS_FILE"

echo "Creating systemd services"
python3 "$DIR"/cli_controller.py service -c "$SETTINGS_FILE"
echo "Enabling systemd services"
systemctl enable azure_casb.service

if [ $java_version == 8 ]; then
  sudo update-java-alternatives --jre-headless --jre --set java-1.8.0-openjdk-amd64
fi
