<div align="center">
    <h1>PosePIE</h1>
    <b>Programmable Input Emulator using AI Pose Estimation</b>
    <br />
    <br />
    <p>
        <a href="#about">About</a>
        &thinsp;•&thinsp;
        <a href="#features">Features</a>
        &thinsp;•&thinsp;
        <a href="#getting-started">Getting Started</a>
        &thinsp;•&thinsp;
        <a href="#license">License</a>
        &thinsp;•&thinsp;
        <a href="#authors">Authors</a>
    </p>
</div>

## About
PosePIE is a programmable input emulator, which emulates input events for virtual gamepads, keyboards and mice based on gestures that are recognized by using AI pose estimation.
It is fully configurable by the user via a Python script.

## Features
 * Works with any off-the-shelf webcam
 * State-of-the-art AI pose estimation models
 * Input emulation for an arbitrary number of gamepads, keyboards and mice
 * Configurable via Python script
 * Easy to use API for mapping gestures to inputs
 * Fully typed for static type checking and advanced IDE support
 * Automatic building of optimized TensorRT models for NVIDIA GPUs

## Getting Started
### Prerequisites
 * Linux
 * Python 3.12
 * Webcam
 * NVIDIA GPU (not strictly required, but highly recommended)

### Setting up uinput (Linux only)
On Linux, PosePIE relies on uinput for emulating input devices.
Therefore, you have to make sure that the uinput kernel module is loaded and that you have write access to the `/dev/uinput` device.
Please consult your distro's documentation on how to set this up.

### Installation
First, make sure you have a conda distribution installed.
Then, install [conda-lock](https://github.com/conda/conda-lock) via one of the installation methods in its readme.

Once you have a conda distribution and conda-lock installed, navigate to your local copy of this repository and create a conda environment using the following command:
```sh
conda-lock install -n pose-pie conda-lock.yml
```

### Running
Before you can run PosePIE, you have to activate the conda environment with:
```sh
conda activate pose-pie
```
This has to be repeated every time you open a new terminal window.

Afterward, you can start PosePIE by providing a user script using the following command:
```sh
python main.py user_scripts/mouse.py
```

## Writing Your Own Scripts
The folder `user_scripts` contains a couple of example user scripts that show how to map various gestures to different input devices.
These scripts can be used as the base for your own scripts and are structured as follows.

A user script implements a single class that is derived from the `ScriptBase` class from the `script.base` module.
There are two methods that should be overridden: `setup()` and `update()`.

The `setup()` method is called once when the program starts and should define variables and set up the required emulated input devices.
Here, `self.max_num_players` should also be set to the maximum number of players, which will be respected by all program logic.
If more than one player should be supported, this variable should also be used in the user script to create one emulated input device per player and to iterated over the detected persons.

The `update()` method is executed at every frame and should contain the main mapping logic.
The logic has to handle each player separately, which can be simplified by using a for loop up to the maximum number of players.

## Optimizations
### Camera Settings
To achieve the best performance, the camera settings should be optimized.
Most pose estimation models work with an internal resolution of 640x640.
Therefore, choosing a resolution that is close to this, such as 640x480 or 640x360 should give you the best results.
Choosing a high frame rate should give you a lower latency at a higher computational cost.
Using an uncompressed video format such as YUYV will result in lower noise and less latency compared to compressed formats like MJPEG or H.264.
All camera settings can be set together by providing them in a single JSON argument.
```
--camera='{"device": 0, "width": 640, "height": 360, "fps": 60, "format_fourcc": "YUYV"}'
```

### TensorRT
It is highly recommended to use an NVIDIA GPU and to optimize the machine learning model for it using TensorRT.
PosePIE can do this automatically for you by starting it with the `--pose.tensorrt=true` command line argument.
Optimizing the model for your GPU will take a few minutes at the first start.

## License
PosePIE is licensed under the [GNU General Public License v3.0](COPYING) or later.

## Authors
 * [Daniel Stolpmann](https://github.com/dstolpmann), [Tegtmeier Inkubator GmbH](https://www.tegtmeier-inkubator.de/), Hamburg, Germany
