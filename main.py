import streamlit as st
import time
from websocket_client import OrderBookWebSocketClient
from models import estimate_slippage, calculate_fee, almgren_chriss_impact, predict_maker_taker
from utils import get_usd_price, get_fee_rate

st.set_page_config(page_title="tradebot", layout="wide")
st.title("tradebot")

with st.sidebar:
    st.header("Input Parameters")
    exchange = st.selectbox("Exchange", ["OKX"])
    spot_asset = st.text_input("Spot Asset (e.g. BTC-USDT)", "BTC-USDT-SWAP")
    order_type = st.selectbox("Order Type", ["market"])
    usd_quantity = st.number_input("Quantity (USD equivalent)", min_value=10.0, value=100.0)
    volatility = st.slider("Volatility (annualized, %)", min_value=1.0, max_value=100.0, value=5.0)
    fee_tier = st.selectbox("Fee Tier", ["default", "VIP"])

col1, col2 = st.columns(2)
with col1:
    st.subheader("Processed Output")
    slippage_out = st.empty()
    fee_out = st.empty()
    impact_out = st.empty()
    net_cost_out = st.empty()
with col2:
    st.subheader("Other Metrics")
    maker_taker_out = st.empty()
    latency_out = st.empty()

orderbook_data = {}

def on_orderbook_message(data):
    global orderbook_data
    orderbook_data = data

ws_url = f"wss://ws.gomarket-cpp.tradebot.io/ws/l2-orderbook/okx/{spot_asset}"
client = OrderBookWebSocketClient(ws_url, spot_asset, on_orderbook_message)
client.start()
time.sleep(1)  

while True:
    if orderbook_data:
        price = float(orderbook_data['asks'][0][0])
        base_quantity = usd_quantity / price

        slippage = estimate_slippage(orderbook_data, base_quantity, side='buy', regression_type='linear')
        slippage_out.metric("Expected Slippage", f"{slippage:.2f} USD")

        fee_rate = get_fee_rate(fee_tier, taker=True)
        fee = calculate_fee(base_quantity, price, fee_rate)
        fee_out.metric("Expected Fees", f"{fee:.2f} USD")

        impact = almgren_chriss_impact(orderbook_data, base_quantity, volatility / 100)
        impact_out.metric("Expected Market Impact", f"{impact:.2f} USD")

        net_cost = slippage + fee + impact
        net_cost_out.metric("Net Cost", f"{net_cost:.2f} USD")

        prob_taker, prob_maker = predict_maker_taker(orderbook_data)
        maker_taker_out.metric("Maker/Taker Proportion", f"{prob_maker*100:.1f}% / {prob_taker*100:.1f}%")

        latency = client.get_last_latency()
        latency_out.metric("Internal Latency (s)", f"{latency:.4f}" if latency else "N/A")

    time.sleep(1)