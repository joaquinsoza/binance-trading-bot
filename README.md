# Binance Trading Bot

## Overview

This project is a cryptocurrency trading bot for the Binance platform, specifically designed to trade on 5-minute intervals. It uses a combination of real-time data collection via WebSockets and historical data analysis to make informed trading decisions.

## Features

- Real-time data collection using WebSocket connections.
- Historical data fetching to initialize the trading context.
- Automated trading based on predefined strategies.
- Dockerized environment for consistent and isolated execution.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Basic understanding of Docker and containerization.

### Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/joaquinsoza/binance-trading-bot
```

2. Navigate to the project directory:

```bash
cd binance-trading-bot
```

3. Start the Docker environment:

```bash
docker-compose up
```

### Usage

1. Open another terminal session and connect to the Python Docker container:

```bash
bash connect_to_docker.sh -p
```

2. Inside the container, run the main application:

```bash
python main.py
```

This will initialize the database with historical data and start the WebSocket data collection.

## Components

- `btcusdt_5m_data_collector.py`: Manages the collection of 5-minute interval data for BTC/USDT.
- `btcusdt_5m_websocket.py`: Handles the WebSocket connection for real-time data.
- `main.py`: The main entry point of the application, orchestrating various components.
- `fetch_historical_data.py`: Fetches historical data to provide initial context for trading decisions.
- Other utility scripts for database initialization, configuration, and testing.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
coderipper

Changing a bit the readme fiel
