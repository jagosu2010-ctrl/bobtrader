"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Trader = void 0;
const IExchangeConnector_1 = require("../engine/connector/IExchangeConnector");
const ConfigManager_1 = require("../config/ConfigManager");
const AnalyticsManager_1 = require("../analytics/AnalyticsManager");
class Trader {
    connector;
    config;
    analytics;
    activeTrades = new Map();
    dcaLevels;
    maxDcaBuys;
    constructor(connector) {
        this.connector = connector;
        this.config = ConfigManager_1.ConfigManager.getInstance();
        this.analytics = new AnalyticsManager_1.AnalyticsManager();
        const cfg = this.config.get("trading");
        this.dcaLevels = cfg.dca_levels || [-2.5, -5.0, -10.0, -20.0, -30.0, -40.0, -50.0];
        this.maxDcaBuys = cfg.max_dca_buys_per_24h || 2;
    }
    async start() {
        console.log("Starting Trader Engine...");
        setInterval(() => this.tick(), 10000); // 10 seconds tick
    }
    async tick() {
        const coins = this.config.get("trading.coins");
        if (!coins)
            return;
        for (const coin of coins) {
            try {
                await this.processCoin(coin);
            }
            catch (e) {
                console.error(`Error processing ${coin}:`, e);
            }
        }
    }
    async processCoin(coin) {
        const pair = `${coin}-USD`;
        const currentPrice = await this.connector.fetchTicker(pair);
        // Mock position retrieval (In real app, fetch from DB or Exchange)
        let position = this.activeTrades.get(coin);
        // 1. Check for ENTRY
        if (!position) {
            // Logic: If Thinker signal is LONG, buy
            // Placeholder for Thinker integration
            // const signal = await this.thinker.getSignal(coin);
            // if (signal === 'LONG') this.enterTrade(coin, currentPrice);
            return;
        }
        // 2. Calculate PnL
        const pnlPct = ((currentPrice - position.avgPrice) / position.avgPrice) * 100;
        console.log(`[Trader] ${coin} Price: ${currentPrice} PnL: ${pnlPct.toFixed(2)}%`);
        // 3. Check for DCA (Dollar Cost Averaging)
        // Only DCA if PnL is negative and we haven't hit max DCA count
        if (pnlPct < 0 && position.dcaCount < this.maxDcaBuys) {
            // Determine next DCA trigger level
            // This logic mirrors pt_trader.py: using levels based on current dcaCount
            // Level 0 uses dcaLevels[0], Level 1 uses dcaLevels[1], etc.
            const levelIndex = position.dcaCount;
            const nextLevel = this.dcaLevels[levelIndex] !== undefined
                ? this.dcaLevels[levelIndex]
                : this.dcaLevels[this.dcaLevels.length - 1]; // Repeat last level if out of bounds
            if (pnlPct <= nextLevel) {
                console.log(`[Trader] Triggering DCA for ${coin} at ${pnlPct.toFixed(2)}% (Level: ${nextLevel}%)`);
                await this.executeDCA(coin, currentPrice, position);
            }
        }
        // 4. Check for Trailing Stop Sell
        // Logic: if pnl > start_pct, activate trail. if price < trail_line, sell.
        const trailingCfg = this.config.get("trading");
        const startPct = position.dcaCount === 0 ? trailingCfg.pm_start_pct_no_dca : trailingCfg.pm_start_pct_with_dca;
        // Activate trailing
        if (pnlPct >= startPct) {
            if (!position.trailActive) {
                position.trailActive = true;
                position.trailPeak = currentPrice;
                // Trail line is gap% below peak
                position.trailLine = currentPrice * (1 - (trailingCfg.trailing_gap_pct / 100));
                console.log(`[Trader] Activated Trailing Stop for ${coin} at ${currentPrice}. Line: ${position.trailLine}`);
            }
            else {
                // Update peak and trail line if price moves up
                if (currentPrice > position.trailPeak) {
                    position.trailPeak = currentPrice;
                    const newLine = currentPrice * (1 - (trailingCfg.trailing_gap_pct / 100));
                    // Ensure trail line only moves UP
                    if (newLine > position.trailLine) {
                        position.trailLine = newLine;
                        console.log(`[Trader] Updated Trailing Stop for ${coin}. New Line: ${position.trailLine}`);
                    }
                }
            }
        }
        // Execute Sell if trail hit
        if (position.trailActive && currentPrice < position.trailLine) {
            console.log(`[Trader] Trailing stop hit for ${coin}. Selling at ${currentPrice}.`);
            await this.exitTrade(coin, currentPrice, position, "trailing_stop");
        }
    }
    async executeDCA(coin, price, position) {
        const dcaMultiplier = this.config.get("trading.dca_multiplier");
        const amount = position.amount * dcaMultiplier;
        console.log(`[Trader] Executing DCA Buy: ${amount} ${coin} @ ${price}`);
        // Execute Buy Order via Connector
        const pair = `${coin}-USD`;
        await this.connector.createOrder(pair, 'market', 'buy', amount);
        // Update position average logic
        const totalCost = (position.avgPrice * position.amount) + (price * amount);
        const totalAmount = position.amount + amount;
        position.amount = totalAmount;
        position.avgPrice = totalCost / totalAmount;
        position.dcaCount++;
        // Log to analytics
        this.analytics.logTrade({
            symbol: coin,
            side: 'buy',
            amount: amount,
            price: price,
            type: 'dca',
            timestamp: Date.now()
        });
    }
    async exitTrade(coin, price, position, reason) {
        console.log(`[Trader] Executing Sell: ${position.amount} ${coin} @ ${price}`);
        const pair = `${coin}-USD`;
        await this.connector.createOrder(pair, 'market', 'sell', position.amount);
        this.analytics.logTrade({
            symbol: coin,
            side: 'sell',
            amount: position.amount,
            price: price,
            type: reason,
            timestamp: Date.now()
        });
        this.activeTrades.delete(coin);
    }
}
exports.Trader = Trader;
//# sourceMappingURL=Trader.js.map