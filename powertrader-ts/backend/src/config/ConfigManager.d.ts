export declare class ConfigManager {
    private static instance;
    private config;
    private configPath;
    private constructor();
    static getInstance(): ConfigManager;
    load(): void;
    get(key: string): any;
    private createDefault;
}
//# sourceMappingURL=ConfigManager.d.ts.map