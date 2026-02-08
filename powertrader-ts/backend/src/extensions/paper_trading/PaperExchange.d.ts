import { IExchangeConnector } from "../../engine/connector/IExchangeConnector";
export declare class PaperExchange implements IExchangeConnector {
    name: string;
    private balance;
    private orders;
    fetchTicker(pair: string): Promise<number>;
    fetchOrderBook(pair: string): Promise<any>;
    fetchOHLCV(pair: string, interval: string, limit?: number): Promise<any[]>;
    fetchBalance(): Promise<any>;
    createOrder(pair: string, type: 'market' | 'limit', side: 'buy' | 'sell', amount: number, price?: number): Promise<any>;
    cancelOrder(id: string, pair: string): Promise<boolean>;
    fetchOrder(id: string, pair: string): Promise<any>;
    fetchOpenOrders(pair?: string): Promise<any[]>;
}
//# sourceMappingURL=PaperExchange.d.ts.map