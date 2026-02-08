import { startServer } from './api/server';
import { Trader } from './trader/Trader';
import { RobinhoodConnector } from './exchanges/RobinhoodConnector';

// Initialize Components
const exchange = new RobinhoodConnector("key", "secret");
const trader = new Trader(exchange);

// Start Services
trader.start();
startServer();
