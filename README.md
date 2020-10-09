# soft_information

The purpose of this code is to adapt the methods presented in the publication [Soft Information for Localization-of-Things](https://ieeexplore.ieee.org/abstract/document/8827486) for locating firefighters on an intervention site.


## Installation

Create a virtual environment and run the following lines:

    git clone https://github.com/bsppbep/soft_information
    cd soft_information
    pip install -r requirements.txt

## Usage
We consider the scenario in which 3 beacons are placed respectively at the coordinates (0,0), (1,1) and (2,2). The goal is to find these positions based only on the following measurements:
- position of 0 : (0,0) (low uncertainty)
- position of 2 : (2,2) (low uncertainty)
- distance 0-1 : 1.41 (medium uncertainty)
- distance 1-2 : 1.41 ((medium uncertainty))
These measurements are stored in the `data/si1.json` file.

Run:

```python
import soft_information

SI_list = soft_information.parse_scenario('soft_information/data/si1.json')
positions, _ = soft_information.compute_positions(SI_list, nb_points=3)

print(positions.round())
``` 

It returns

    [[0. 0.]
     [1. 1.]
     [2. 2.]]

Correct answer.

