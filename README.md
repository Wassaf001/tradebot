# tradebot

tradebot is a real-time trading simulator and analytics tool for cryptocurrency order books. It provides live order book data, slippage estimation, fee calculation, market impact modeling, and maker/taker probability analysis. The app is built with Streamlit for an interactive web interface.

## Features
- Real-time order book streaming from OKX
- Slippage estimation using regression models
- Fee calculation based on exchange tiers
- Market impact modeling (Almgren-Chriss)
- Maker/taker probability estimation
- Internal latency measurement
- User-friendly web interface

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd tradebot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run main.py
```

Open your browser and go to the local URL provided by Streamlit.

## Project Structure
- `main.py`: Streamlit app entry point
- `websocket_client.py`: WebSocket client for order book data
- `models.py`: Slippage, fee, impact, and maker/taker models
- `utils.py`: Utility functions (price fetch, fee rates)
- `documentation/`: Model and algorithm explanations


### Backend API
The backend remains a Python service (see above for running instructions). The frontend is in streamlit as of now, but will be deployed using React.