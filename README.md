# Uniswap V3 Arbitrage
Calculating real arbitrage opportunities at uniswap v3.

### Create pairs
```python
$ python main.py
```
It generates a `json` file with all the surface rates which can then be used to calculate depth.

### Find oppertunities
```js
$ node main
```
It uses the `json` file and calculate the depth by using real blockchain data.
