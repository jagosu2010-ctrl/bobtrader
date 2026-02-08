"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnalyticsManager = void 0;
const better_sqlite3_1 = __importDefault(require("better-sqlite3"));
const path_1 = __importDefault(require("path"));
class AnalyticsManager {
    db;
    constructor() {
        const dbPath = path_1.default.join(process.cwd(), 'trades.db');
        this.db = new better_sqlite3_1.default(dbPath);
        this.init();
    }
    init() {
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                amount REAL NOT NULL,
                price REAL NOT NULL,
                timestamp INTEGER NOT NULL
            )
        `);
    }
    logTrade(trade) {
        const stmt = this.db.prepare('INSERT INTO trades (symbol, side, amount, price, timestamp) VALUES (?, ?, ?, ?, ?)');
        stmt.run(trade.symbol, trade.side, trade.amount, trade.price, Date.now());
    }
    getPerformance() {
        // Mock performance calculation
        return {
            totalTrades: 150,
            winRate: 0.65,
            pnl: 1250.50
        };
    }
}
exports.AnalyticsManager = AnalyticsManager;
//# sourceMappingURL=AnalyticsManager.js.map