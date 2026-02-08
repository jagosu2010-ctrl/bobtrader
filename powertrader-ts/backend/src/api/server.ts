import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import http from 'http';
import { ConfigManager } from '../config/ConfigManager';
import { AnalyticsManager } from '../analytics/AnalyticsManager';
import { WebSocketManager } from './websocket';
import { CointradeAdapter } from '../modules/cointrade/CointradeAdapter';

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

const config = ConfigManager.getInstance();
const analytics = new AnalyticsManager();
const cointrade = new CointradeAdapter();

// --- API ROUTES ---

// Dashboard Data
app.get('/api/dashboard', (req, res) => {
    const perf = analytics.getPerformance();
    res.json({
        account: {
            total: 10000,
            pnl: perf.pnl
        },
        trades: [
            { symbol: 'BTC', pnl: 1.2, stage: 0 },
            { symbol: 'ETH', pnl: -0.5, stage: 1 }
        ]
    });
});

app.get('/api/settings', (req, res) => {
    res.json(config.get('trading'));
});

app.post('/api/settings', (req, res) => {
    // In a real implementation: config.set('trading', req.body);
    res.json({ success: true });
});

app.get('/api/volume/:coin', (req, res) => {
    res.json({
        profile: { average: 5000, median: 4500, p90: 8000 },
        recent: [
            { timestamp: Date.now(), volume: 4200, ratio: 1.1, trend: 'increasing' }
        ]
    });
});

// Strategy Sandbox Endpoint
app.post('/api/strategy/backtest', async (req, res) => {
    try {
        console.log("[API] Running Strategy Backtest...", req.body);

        // Mock data generation for simulation
        const mockData = Array.from({ length: 50 }, (_, i) => ({
            time: i,
            open: 50000 + Math.random() * 100,
            high: 50100 + Math.random() * 100,
            low: 49900 + Math.random() * 100,
            close: 50000 + Math.random() * 1000,
            volume: 1000 + Math.random() * 500
        }));

        // Run Cointrade logic
        const enrichedData = await cointrade.populateIndicators(mockData);
        const withBuy = await cointrade.populateBuyTrend(enrichedData);
        const finalResults = await cointrade.populateSellTrend(withBuy);

        res.json(finalResults);
    } catch (e) {
        console.error(e);
        res.status(500).json({ error: "Backtest failed" });
    }
});

export function startServer() {
    const server = http.createServer(app);
    WebSocketManager.getInstance().initialize(server);

    server.listen(port, () => {
        console.log(`[API] Backend running at http://localhost:${port}`);
    });
}
