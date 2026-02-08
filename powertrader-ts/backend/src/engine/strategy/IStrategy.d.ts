export interface IStrategy {
    name: string;
    interval: string;
    populateIndicators(dataframe: any): Promise<any>;
    populateBuyTrend(dataframe: any): Promise<any>;
    populateSellTrend(dataframe: any): Promise<any>;
    stopLoss?: number;
    trailingStop?: boolean;
    trailingStopPositive?: number;
    trailingStopPositiveOffset?: number;
    positionSize?: number;
}
export interface IStrategyManager {
    loadStrategy(name: string): Promise<IStrategy>;
    getAvailableStrategies(): string[];
    validateStrategy(strategy: IStrategy): boolean;
}
//# sourceMappingURL=IStrategy.d.ts.map