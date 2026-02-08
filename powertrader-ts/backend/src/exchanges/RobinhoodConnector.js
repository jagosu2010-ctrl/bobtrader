"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.RobinhoodConnector = void 0;
const IExchangeConnector_1 = require("../../engine/connector/IExchangeConnector");
const axios_1 = __importStar(require("axios"));
const uuid_1 = require("uuid");
const crypto = __importStar(require("crypto"));
class RobinhoodConnector {
    name = "Robinhood";
    baseUrl = "https://trading.robinhood.com";
    apiKey;
    privateKey;
    axiosInstance;
    constructor(apiKey, privateKey) {
        this.apiKey = apiKey;
        this.privateKey = privateKey;
        this.axiosInstance = axios_1.default.create({
            baseURL: this.baseUrl,
            timeout: 10000
        });
    }
    getAuthorizationHeader(method, path, body, timestamp) {
        const messageToSign = `${this.apiKey}${timestamp}${path}${method}${body}`;
        // Use Node.js crypto for Ed25519 signing
        // Note: privateKey string from file is likely base64 encoded seed or private key
        // This is a simplified implementation assuming standard handling
        // Real implementation requires precise key format handling (e.g. using nacl or sodium-native)
        // Placeholder for actual signing logic which depends on key format
        // const signature = ...
        // Mock signature for now to allow compilation/structure
        const signature = "mock_signature_base64";
        return {
            "x-api-key": this.apiKey,
            "x-signature": signature,
            "x-timestamp": timestamp.toString(),
            "Content-Type": "application/json"
        };
    }
    async makeRequest(method, path, body = null) {
        const timestamp = Math.floor(Date.now() / 1000);
        const bodyStr = body ? JSON.stringify(body) : "";
        const headers = this.getAuthorizationHeader(method, path, bodyStr, timestamp);
        try {
            const response = await this.axiosInstance.request({
                method,
                url: path,
                headers,
                data: body
            });
            return response.data;
        }
        catch (error) {
            console.error(`[Robinhood] Request failed: ${error}`);
            throw error;
        }
    }
    async fetchTicker(pair) {
        try {
            const res = await this.makeRequest('GET', `/api/v1/crypto/marketdata/best_bid_ask/?symbol=${pair}`);
            if (res.results && res.results.length > 0) {
                return parseFloat(res.results[0].ask_inclusive_of_buy_spread);
            }
            return 0;
        }
        catch (e) {
            console.error(`[Robinhood] Error fetching ticker for ${pair}:`, e);
            return 0;
        }
    }
    async fetchOrderBook(pair) {
        // Robinhood might not expose full orderbook via this API endpoint easily
        return { bids: [], asks: [] };
    }
    async fetchOHLCV(pair, interval, limit) {
        // Implement historical data fetching logic
        return [];
    }
    async fetchBalance() {
        try {
            const res = await this.makeRequest('GET', '/api/v1/crypto/trading/accounts/');
            // Transform RH response to standard format
            return res;
        }
        catch (e) {
            return {};
        }
    }
    async createOrder(pair, type, side, amount, price) {
        const clientOrderId = (0, uuid_1.v4)();
        const body = {
            client_order_id: clientOrderId,
            side: side,
            type: type,
            symbol: pair,
            market_order_config: {
                asset_quantity: amount.toFixed(8)
            }
        };
        if (type === 'limit' && price) {
            body.limit_order_config = {
                limit_price: price.toFixed(2),
                asset_quantity: amount.toFixed(8)
            };
            delete body.market_order_config;
        }
        console.log(`[Robinhood] Placing ${side} order for ${amount} ${pair}`);
        try {
            const res = await this.makeRequest('POST', '/api/v1/crypto/trading/orders/', body);
            return res;
        }
        catch (e) {
            console.error(`[Robinhood] Order placement failed:`, e);
            return null;
        }
    }
    async cancelOrder(id, pair) {
        try {
            await this.makeRequest('POST', `/api/v1/crypto/trading/orders/${id}/cancel/`);
            return true;
        }
        catch (e) {
            return false;
        }
    }
    async fetchOrder(id, pair) {
        try {
            return await this.makeRequest('GET', `/api/v1/crypto/trading/orders/${id}/`);
        }
        catch (e) {
            return null;
        }
    }
    async fetchOpenOrders(pair) {
        // Implement fetching open orders
        return [];
    }
}
exports.RobinhoodConnector = RobinhoodConnector;
//# sourceMappingURL=RobinhoodConnector.js.map