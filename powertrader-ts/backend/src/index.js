"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const server_1 = require("./api/server");
const Trader_1 = require("./trader/Trader");
const RobinhoodConnector_1 = require("./exchanges/RobinhoodConnector");
// Initialize Components
const exchange = new RobinhoodConnector_1.RobinhoodConnector("key", "secret");
const trader = new Trader_1.Trader(exchange);
// Start Services
trader.start();
(0, server_1.startServer)();
//# sourceMappingURL=index.js.map