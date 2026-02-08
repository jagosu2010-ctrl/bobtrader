"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConfigManager = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const yaml_1 = __importDefault(require("yaml"));
class ConfigManager {
    static instance;
    config = {};
    configPath;
    constructor() {
        this.configPath = path_1.default.join(process.cwd(), 'config.yaml');
        this.load();
    }
    static getInstance() {
        if (!ConfigManager.instance) {
            ConfigManager.instance = new ConfigManager();
        }
        return ConfigManager.instance;
    }
    load() {
        try {
            if (fs_1.default.existsSync(this.configPath)) {
                const fileContents = fs_1.default.readFileSync(this.configPath, 'utf8');
                this.config = yaml_1.default.parse(fileContents);
            }
            else {
                console.log("Config file not found, creating default.");
                this.createDefault();
            }
        }
        catch (e) {
            console.error("Error loading config:", e);
        }
    }
    get(key) {
        return key.split('.').reduce((o, i) => o?.[i], this.config);
    }
    createDefault() {
        this.config = {
            trading: {
                coins: ["BTC", "ETH", "XRP", "BNB", "DOGE"],
                trade_start_level: 3,
                start_allocation_pct: 0.005,
                dca_multiplier: 2.0,
                dca_levels: [-2.5, -5.0, -10.0, -20.0, -30.0, -40.0, -50.0],
                max_dca_buys_per_24h: 2
            },
            system: {
                log_level: "INFO"
            }
        };
        fs_1.default.writeFileSync(this.configPath, yaml_1.default.stringify(this.config));
    }
}
exports.ConfigManager = ConfigManager;
//# sourceMappingURL=ConfigManager.js.map