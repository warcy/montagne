# Montagne

Montagne is an enhance service for OpenStack LBaaS.

**Only OpenStack Juno is supported now.**

## Introduction

Montagne can grab message from applications, such as nova, neutron, ceilometer
and so on, to configure your OpenStack LBaaS module.

## Installation

```bash
# do not support python2
sudo apt-get install python3-dev
python3 tools/install_venv.py
```

## Example

edge switch fault

```bash
$ curl 127.0.0.1:8080/event/switch -X POST -i -d '{
    "tunnel_ip": ["10.0.0.31", "10.0.0.32"],
    "dpid": "0000001e080003ac",
    "status": "False"
}'
```

edge switch port fault

```bash
$ curl 127.0.0.1:8080/event/switch/port -X POST -i -d '{
    "tunnel_ip": ["10.0.0.31", "10.0.0.32"],
    "dpid": "0000001e080003ac",
    "port_no": "1",
    "status": "False"
}'
```
