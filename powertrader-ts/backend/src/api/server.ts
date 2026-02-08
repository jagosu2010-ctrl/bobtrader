import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import { ConfigManager } from '../config/ConfigManager';
import { AnalyticsManager } from '../analytics/AnalyticsManager';

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

const config = ConfigManager.getInstance();
const analytics = new AnalyticsManager();

// --- API ROUTES ---

// Dashboard Data
app.get('/api/dashboard', (req, res) => {
    const perf = analytics.getPerformance();
    res.json({
        account: {
            total: 10000, // Mock for now, hook to Trader later
            pnl: perf.pnl
        },
        trades: [
            // Mock active trades
            { symbol: 'BTC', pnl: 1.2, stage: 0 },
            { symbol: 'ETH', pnl: -0.5, stage: 1 }
        ]
    });
});

// Settings
app.get('/api/settings', (req, res) => {
    res.json(config.get('trading'));
});

app.post('/api/settings', (req, res) => {
    // Save settings logic
    // config.set('trading', req.body);
    res.json({ success: true });
});

// Volume Data (Mock for VolumeDashboard)
app.get('/api/volume/:coin', (req, res) => {
    res.json({
        profile: { average: 5000, median: 4500, p90: 8000 },
        recent: [
            { timestamp: Date.now(), volume: 4200, ratio: 1.1, trend: 'increasing' }
        ]
    });
});

export function startServer() {
    app.listen(port, () => {
        console.log(`[API] Backend running at http://localhost:${port}`);
    });
}
