# Pulsoid-to-VRChat-OSC-python
Python implementation of [Pulsoid-to-VRChat-OSC](https://github.com/Sonic853/Pulsoid-to-VRChat-OSC), with simplifeid codebase and QoL changes

Main features:
- More portable & overall simpler code stucture compared to original (or HRtoVRChat_OSC)
- Written in pure python with no additional requirements


## Setup


1. follow the official pulsoid guide to setup the heartrate monitor: [How to display your heart rate in VRChat](https://blog.pulsoid.net/post/how-to-display-your-heart-rate-in-vrchat). Go to next step when you can successfully see your device's readings on pulsoid website.

2. clone the repo, install python if you haven't:

```bash
git clone https://github.com/trojblue/Pulsoid-to-VRChat-OSC-python
cd Pulsoid-to-VRChat-OSC-python
```

3. start the service. It will attempt to get auth token if a `token.txt` is not found in the root directory:

```bash
python pulsoid_bridge.py
```

