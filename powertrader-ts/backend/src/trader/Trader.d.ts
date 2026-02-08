import { IExchangeConnector } from "../engine/connector/IExchangeConnector";
export declare class Trader {
    private connector;
    private config;
    private analytics;
    private activeTrades;
    private dcaLevels;
    private maxDcaBuys;
    constructor(connector: IExchangeConnector);
    start(): Promise<void>;
    private tick;
    private processCoin;
    private executeDCA;
    private exitTrade;
}
//# sourceMappingURL=Trader.d.ts.map