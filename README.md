# Emulated IoT (ELIOT) Platform

The Emulated IoT (ELIOT) platform enables emulating simple IoT devices on Docker. It is based on libraries, [coap-node](https://github.com/PeterEB/coap-node) and [Leshan](https://github.com/eclipse/leshan), which implement device management over CoAP and LWM2M. Devices consisting of simple sensors and actuators can be built using IPSO objects. The current implementation provides ready-to-use devices, such as weather observer, presence detector, light controller and radiator.

More detailed information about ELIOT can be found from [wiki](https://github.com/Alliasd/ELIOT/wiki)

Run multiple clients with docker-compose
   `docker-compose build` to build 
   `docker-compose up`

   `docker-compose scale light=X`

   i trimmed down the devices in the docker compose, please return them in the same way as the light one

