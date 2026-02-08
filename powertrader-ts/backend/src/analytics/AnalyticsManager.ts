import Database from 'better-sqlite3';
import path from 'path';
import { ConfigManager } from '../config/ConfigManager';

export class AnalyticsManager {
    private db: Database.Database;

    constructor() {
        const config = ConfigManager.getInstance();
        const hubDir = config.get("trading.hub_data_dir") || "hub_data";

        // Ensure path is absolute or correct relative to execution
        // We assume hub_data is at project root
        const dbPath = path.resolve(process.cwd(), '..', hubDir, 'trades.db');

        console.log(`[Analytics] Initializing database at ${dbPath}`);
        this.db = new Database(dbPath);
        this.init();
    }

    private init(): void {
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                amount REAL NOT NULL,
                price REAL NOT NULL,
                type TEXT,
                timestamp INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS performance_daily (
                date TEXT PRIMARY KEY,
                pnl REAL DEFAULT 0,
                trades_count INTEGER DEFAULT 0
            );
        `);
    }

    public logTrade(trade: any): void {
        try {
            const stmt = this.db.prepare(
                'INSERT INTO trades (symbol, side, amount, price, type, timestamp) VALUES (?, ?, ?, ?, ?, ?)'
            );
            stmt.run(trade.symbol, trade.side, trade.amount, trade.price, trade.type || 'market', trade.timestamp || Date.now());
            console.log(`[Analytics] Logged trade: ${trade.side} ${trade.symbol}`);
        } catch (e) {
            console.error("[Analytics] Failed to log trade:", e);
        }
    }

    public getPerformance(): any {
        try {
            const row = this.db.prepare(`
                SELECT
                    COUNT(*) as totalTrades,
                    SUM(CASE WHEN side = 'sell' THEN (price * amount) ELSE -(price * amount) END) as pnl
                FROM trades
            `).get() as any;

            // Simple Win Rate calculation (heuristic: sell > average buy price)
            // Real implementation requires tracking trade groups/positions

            return {
                totalTrades: row.totalTrades || 0,
                winRate: 0.0, // Placeholder until trade grouping is ported
                pnl: row.pnl || 0.0
            };
        } catch (e) {
            console.error("[Analytics] Error calculating performance:", e);
            return { totalTrades: 0, winRate: 0, pnl: 0 };
        }
    }
}
