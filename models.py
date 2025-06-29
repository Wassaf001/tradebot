import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression, QuantileRegressor

def estimate_slippage(orderbook, quantity, side='buy', regression_type='linear'):
    """
    Estimate slippage using regression on orderbook depth.
    """
    prices, sizes = [], []
    if side == 'buy':
        for ask in orderbook['asks']:
            prices.append(float(ask[0]))
            sizes.append(float(ask[1]))
    else:
        for bid in orderbook['bids']:
            prices.append(float(bid[0]))
            sizes.append(float(bid[1]))

    cum_sizes = np.cumsum(sizes)
    prices = np.array(prices)
    if regression_type == 'quantile':
        model = QuantileRegressor(quantile=0.5, alpha=0)
    else:
        model = LinearRegression()
    X = cum_sizes.reshape(-1, 1)
    y = prices
    model.fit(X, y)
    est_price = model.predict(np.array([[quantity]]))[0]
    best_price = prices[0]
    slippage = abs(est_price - best_price)
    return slippage

def calculate_fee(quantity, price, fee_rate):
    """
    Calculate expected fee for the trade.
    """
    return quantity * price * fee_rate

def almgren_chriss_impact(orderbook, quantity, volatility, eta=0.142, gamma=2.5e-7):
    """
    Simplified Almgren-Chriss market impact model.
    """
    mid_price = (float(orderbook['bids'][0][0]) + float(orderbook['asks'][0][0])) / 2
    temp_impact = eta * (quantity ** 2)
    perm_impact = gamma * quantity
    impact = temp_impact + perm_impact + volatility * mid_price * 0.01
    return impact

def predict_maker_taker(orderbook, features=None):
    """
    Dummy logistic regression for maker/taker proportion.
    """
    spread = float(orderbook['asks'][0][0]) - float(orderbook['bids'][0][0])
    depth = sum(float(ask[1]) for ask in orderbook['asks'][:5]) + sum(float(bid[1]) for bid in orderbook['bids'][:5])
    X = np.array([[spread, depth]])
    model = LogisticRegression()
    model.coef_ = np.array([[1.0, -1.0]])
    model.intercept_ = np.array([0.0])
    model.classes_ = np.array([0, 1])
    prob_taker = model.predict_proba(X)[0][1]
    return prob_taker, 1 - prob_taker