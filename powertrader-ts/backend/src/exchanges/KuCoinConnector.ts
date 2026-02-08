import { IExchangeConnector } from "../../engine/connector/IExchangeConnector";
import axios from 'axios';

export class KuCoinConnector implements IExchangeConnector {
    name = "KuCoin";
    private baseUrl = "https://api.kucoin.com";

    async fetchTicker(pair: string): Promise<number> {
        try {
            // KuCoin symbol format: BTC-USDT
            const symbol = pair.replace("USD", "USDT");
            const res = await axios.get(`${this.baseUrl}/api/v1/market/orderbook/level1?symbol=${symbol}`);
            return parseFloat(res.data.data.price);
        } catch (e) {
            console.error(`[KuCoin] Error fetching ticker for ${pair}:`, e);
            return 0;
        }
    }

    async fetchOrderBook(pair: string): Promise<any> { return {}; }
    async fetchOHLCV(pair: string, interval: string, limit?: number): Promise<any[]> { return []; }
    async fetchBalance(): Promise<any> { return {}; }
    async createOrder(pair: string, type: 'market'|'limit', side: 'buy'|'sell', amount: number, price?: number): Promise<any> { return {}; }
    async cancelOrder(id: string, pair: string): Promise<boolean> { return true; }
    async fetchOrder(id: string, pair: string): Promise<any> { return {}; }
    async fetchOpenOrders(pair?: string): Promise<any[]> { return []; }
}
