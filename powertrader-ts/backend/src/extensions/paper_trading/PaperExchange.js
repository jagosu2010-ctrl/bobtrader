"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PaperExchange = void 0;
const IExchangeConnector_1 = require("../../engine/connector/IExchangeConnector");
class PaperExchange {
    name = "Paper";
    balance = { USD: 10000 };
    orders = [];
    async fetchTicker(pair) {
        return 100 + Math.random() * 10; // Mock price
    }
    async fetchOrderBook(pair) {
        return { bids: [], asks: [] };
    }
    async fetchOHLCV(pair, interval, limit) {
        return [];
    }
    async fetchBalance() {
        return this.balance;
    }
    async createOrder(pair, type, side, amount, price) {
        const id = Math.random().toString(36).substring(7);
        const order = { id, pair, type, side, amount, price, status: 'open' };
        this.orders.push(order);
        console.log(`[Paper] Created order: ${side} ${amount} ${pair} @ ${price}`);
        return order;
    }
    async cancelOrder(id, pair) {
        this.orders = this.orders.filter(o => o.id !== id);
        return true;
    }
    async fetchOrder(id, pair) {
        return this.orders.find(o => o.id === id);
    }
    async fetchOpenOrders(pair) {
        return this.orders;
    }
}
exports.PaperExchange = PaperExchange;
//# sourceMappingURL=PaperExchange.js.map