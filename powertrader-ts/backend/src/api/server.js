"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.startServer = startServer;
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const body_parser_1 = __importDefault(require("body-parser"));
const ConfigManager_1 = require("../config/ConfigManager");
const AnalyticsManager_1 = require("../analytics/AnalyticsManager");
const app = (0, express_1.default)();
const port = 3000;
app.use((0, cors_1.default)());
app.use(body_parser_1.default.json());
const config = ConfigManager_1.ConfigManager.getInstance();
const analytics = new AnalyticsManager_1.AnalyticsManager();
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
function startServer() {
    app.listen(port, () => {
        console.log(`[API] Backend running at http://localhost:${port}`);
    });
}
//# sourceMappingURL=server.js.map