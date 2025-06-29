# Model and Algorithm Documentation

## Slippage Estimation
- Uses linear or quantile regression on the orderbook depth to estimate the price impact of executing a market order of the specified size.

## Fee Calculation
- Rule-based, using fee tiers from OKX documentation. Default taker/maker rates are used unless VIP is selected.

## Market Impact (Almgren-Chriss Model)
- Implements a simplified version of the Almgren-Chriss model, combining temporary and permanent impact with volatility adjustment.

## Maker/Taker Proportion
- Dummy logistic regression based on spread and depth to estimate the likelihood of a trade being maker or taker.

## Latency Measurement
- Measures the time taken to process each orderbook tick and update the UI.

## Performance Optimizations
- Uses efficient data structures (numpy arrays) and threading for WebSocket.
- All calculations are vectorized where possible.
- UI updates are throttled to avoid unnecessary redraws.

## Further Improvements
- Real regression models can be trained on historical data.
- More advanced market impact models can be implemented.