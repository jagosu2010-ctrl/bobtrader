"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Thinker = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const ConfigManager_1 = require("../config/ConfigManager");
class Thinker {
    memories = new Map();
    config;
    tfChoices = ["1hour", "2hour", "4hour", "8hour", "12hour", "1day", "1week"];
    constructor() {
        this.config = ConfigManager_1.ConfigManager.getInstance();
    }
    async loadMemory(coin) {
        // Porting logic to load memories from file system
        // Python version loads files like "memories_1hour.txt" from coin folder
        // We will assume a similar structure in `hub_data/neural/<coin>`
        const neuralDir = this.config.get("trading.main_neural_dir") || "hub_data";
        const coinDir = path_1.default.join(neuralDir, coin);
        for (const tf of this.tfChoices) {
            const memoryPath = path_1.default.join(coinDir, `memories_${tf}.txt`);
            const weightPath = path_1.default.join(coinDir, `memory_weights_${tf}.txt`);
            if (fs_1.default.existsSync(memoryPath) && fs_1.default.existsSync(weightPath)) {
                // Parse files (logic from pt_thinker.py: split by '~', clean chars)
                const memRaw = fs_1.default.readFileSync(memoryPath, 'utf-8');
                const wgtRaw = fs_1.default.readFileSync(weightPath, 'utf-8');
                const memList = memRaw.replace(/['",\[\]]/g, "").split("~");
                const wgtList = wgtRaw.replace(/['",\[\]]/g, "").split(" ");
                const patterns = [];
                for (let i = 0; i < memList.length; i++) {
                    if (!memList[i].trim())
                        continue;
                    // Parse "pattern{}high{}low" format
                    const parts = memList[i].split("{}");
                    if (parts.length < 3)
                        continue;
                    const candles = parts[0].trim().split(" ").map(parseFloat);
                    const nextHigh = parseFloat(parts[1]);
                    const nextLow = parseFloat(parts[2]);
                    const weight = parseFloat(wgtList[i] || "0");
                    patterns.push({
                        candles,
                        nextHigh,
                        nextLow,
                        weight,
                        highWeight: 1.0, // Simplified port
                        lowWeight: 1.0 // Simplified port
                    });
                }
                // Store using a key like "BTC_1hour"
                this.memories.set(`${coin}_${tf}`, patterns);
                console.log(`[Thinker] Loaded ${patterns.length} patterns for ${coin} ${tf}`);
            }
        }
    }
    async predict(coin, timeframe, currentCandlePct) {
        const key = `${coin}_${timeframe}`;
        const memory = this.memories.get(key);
        if (!memory || memory.length === 0) {
            return { prediction: "NEUTRAL", confidence: 0 };
        }
        // kNN Logic
        // Find closest patterns based on Euclidean distance of the pattern sequence
        // For simplicity (and matching Python code which often checks just the last candle or simplified diff):
        // Load threshold
        // const threshold = loadThreshold(coin, timeframe);
        const threshold = 0.5; // Mock threshold
        let weightedMoves = 0;
        let totalWeight = 0;
        let matches = 0;
        for (const pat of memory) {
            // Compare current candle pct with the last candle in pattern
            // Python: abs((abs(current - memory) / avg) * 100)
            const memCandle = pat.candles[0]; // Assuming length 1 pattern for basic port
            const avg = (currentCandlePct + memCandle) / 2;
            let diff = 0;
            if (avg !== 0) {
                diff = Math.abs((Math.abs(currentCandlePct - memCandle) / avg) * 100);
            }
            if (diff <= threshold) {
                weightedMoves += pat.nextHigh * pat.weight; // Simplified prediction logic
                totalWeight += pat.weight;
                matches++;
            }
        }
        if (matches === 0)
            return { prediction: "NEUTRAL", confidence: 0 };
        const predictedMove = totalWeight > 0 ? weightedMoves / totalWeight : 0;
        return {
            coin,
            timeframe,
            prediction: predictedMove > 0 ? "LONG" : "SHORT",
            predictedValue: predictedMove,
            confidence: matches / memory.length
        };
    }
}
exports.Thinker = Thinker;
//# sourceMappingURL=Thinker.js.map