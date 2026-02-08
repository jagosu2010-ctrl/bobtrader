export declare class Thinker {
    private memories;
    private config;
    private tfChoices;
    constructor();
    loadMemory(coin: string): Promise<void>;
    predict(coin: string, timeframe: string, currentCandlePct: number): Promise<any>;
}
//# sourceMappingURL=Thinker.d.ts.map