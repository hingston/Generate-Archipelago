# Python Programming Task
### Exercise 1 – Generating islands
We would like you to write some code to generate some ‘islands’ in an N * N grid of Boolean numbers (1s or 0s). Land is indicated with a 1, and sea by a 0. Islands are connected pieces of land.

The code should allow some flexibility in generating different types of archipelago:
- number of islands
- size of islands
- shape of islands
### Exercise 2 – Counting islands
Please write some code to read in an N * N grid of Boolean numbers, and count the number of islands in the grid. Land is indicated with a 1, and sea by a 0. Islands are connected pieces of land.
### Requirements
- Python 3.6+
- Install requirements.txt with `$ pip3 install -r requirements.txt`
### Usage
##### Archipelago.py
`$ python Archipelago.py [-h] [--n N] [--weathering WEATHERING] [--sea_level SEA_LEVEL] [--seed SEED]`
###### optional arguments:
```
  -h, --help              Show this help message and exit.
  --n N                   Used to create an N * N grid of pixels. Must be greater than 0.
  --weathering WEATHERING The weathering of the islands. Must be between 1 and 5, where 1 is most weathered
                          (smoother edges) and 5 is least weathered (rougher edges).
  --sea_level SEA_LEVEL   The sea level. Must be between -1 and 1, where -1 is all land and 1 is all water.
  --seed SEED             The seed the islands are generated from. Must be between 0 and 65535.
```
##### Tests.py
`$ python Tests.py`
