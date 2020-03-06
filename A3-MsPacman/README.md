# Ms. Pacman AI using Reinforcement Learning

The code in the directory comprise the python 3 code that compose the Ms. Pacman AI using RL to perform its actions. The agent is meant to be run on the [__Arcade Learning Environment__ (ALE) interface ](https://github.com/mgbellemare/Arcade-Learning-Environment) of the __Stella__ Atari game emulator. The setup instructions are found on the ALE github repository. The instructions to run the agent assume that the ALE interface is properly installed with the python module of the interface named _ale_py_. 

### Dependencies

The agent requires a few python module in order to be properly interpreted. The dependencies are : _ale_py_, _numpy_, _collections_, _copy_, _math_, _random_, and _csv_. Most of the dependencies are python 3.7 basic modules that come with the distribution of python. If they are not in the python environment, they can be downloaded by doing:
```
pip3 install module_name
```

An example for numpy is:
```
pip3 install numpy
```

### Running the Agent

To agent is comprised of three files: _agent.py_, _RL.py_, and _csv_util.py_. In order to run the agent, the following command with the indicated system arguments needs to run:

```python
python3 agent.py rom_file -a [learning rate] -g [discount rate] -e [exploration factor] -x [prior experience file (csv)(optional)] -s [seed(optional)]
```
The prior experience, -x argument, and seed, -s argument, are optional and do not need to be included in the call. 

An example call would be:
```python
python3 agent.py ms_pacman.bin -a 0.2 -g 0.9 -e 0.05 -s 90
```

Note: The agent will save its weights to a file named _weights.csv_ when it has finished running. CSV files with the same number of feature weights (5) can be used. Files with less weights will cause the program to throw exceptions and stop running.