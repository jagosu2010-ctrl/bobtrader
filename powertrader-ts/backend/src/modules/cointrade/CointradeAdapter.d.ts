import { IStrategy } from "../../engine/strategy/IStrategy";
export declare class CointradeAdapter implements IStrategy {
    name: string;
    interval: string;
    constructor();
    populateIndicators(dataframe: any): Promise<any>;
    populateBuyTrend(dataframe: any): Promise<any>;
    populateSellTrend(dataframe: any): Promise<any>;
}
//# sourceMappingURL=CointradeAdapter.d.ts.map