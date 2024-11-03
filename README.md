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


## More Info

The project uses the same OSC addresses as the original repo, so the README there could be useful. Here's a brief overview:

## Server Address

| Addresss                            | Value Type | Description                  |
| ----------------------------------- | ---------- | ---------------------------- |
| /avatar/parameters/HeartRateInt     | Int        | Int [0, 255]                 |
| /avatar/parameters/HeartRate3       | Int        | See HeartRateInt             |
| /avatar/parameters/HeartRateFloat   | Float      | Float ([0, 255] -> [-1, 1])  |
| /avatar/parameters/HeartRate        | Float      | See HeartRateFloat           |
| /avatar/parameters/HeartRateFloat01 | Float      | Float ([0, 255] -> [0, 1])   |
| /avatar/parameters/HeartRate2       | Float      | See HeartRateFloat01         |
| /avatar/parameters/HeartBeatToggle  | Bool       | Reverses with each heartbeat |

### Example Avatars

[Vard](https://twitter.com/VardFree) made this Avatar, you can use his Avatar to test: [Example_Avatar.unitypackage](https://github.com/vard88508/vrc-osc-miband-hrm/releases) (This Avatar uses RED_SIM's [Simple counter shader](https://patreon.com/posts/simple-counter-62864361) to display numbers)

The value used by this Avatar is `Heartrate`, which is of type Float and ranges from -1(0bpm) to 1(255bpm).
