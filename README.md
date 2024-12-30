# Microphone Blow Detection
<ins>__Note: I recommend downloading the code as a zip rather than switching to this branch to test it.__<ins>

## Installation
Ensure your environment has Python and Pip installed.
- [Python Installation](https://www.python.org/downloads/)
- [Pip Installation](https://pip.pypa.io/en/stable/installation/)
    - Usually automically installed with Python
```
python --version
```
```
pip --version
```
Both commands should print out the installation version when successfully installed.

## Setup
Ensure that you are in the main directory (WATW_Microphone) and run:
```
pip install -r requirements.txt
```
If this doesn't work, install the dependencies individually.
```
pip install matplotlib
pip install numpy
pip install scipy
pip install sounddevice
```

## Running the Program
```
python blow_detection.py
```
