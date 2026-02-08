import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export const StrategySandbox: React.FC = () => {
    const [backtestData, setBacktestData] = useState<any[]>([]);
    const [rsiThreshold, setRsiThreshold] = useState(30);
    const [isRunning, setIsRunning] = useState(false);

    const runSimulation = async () => {
        setIsRunning(true);
        try {
            // In a real app, this would be a POST to /api/strategy/backtest with parameters
            // mocking the response for now
            const mockData = Array.from({ length: 50 }, (_, i) => ({
                time: i,
                price: 50000 + Math.random() * 1000,
                rsi: 20 + Math.random() * 60,
                signal: Math.random() > 0.8 ? 1 : 0 // 1 = buy
            }));

            // Simulate delay
            await new Promise(r => setTimeout(r, 800));
            setBacktestData(mockData);
        } catch (e) {
            console.error(e);
        } finally {
            setIsRunning(false);
        }
    };

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">Strategy Sandbox</h1>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Controls */}
                <div className="bg-white p-6 rounded-lg shadow lg:col-span-1">
                    <h2 className="text-xl font-semibold mb-4">Parameters</h2>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Strategy</label>
                            <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border">
                                <option>Cointrade (External)</option>
                                <option>SMA Crossover</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">RSI Buy Threshold</label>
                            <input
                                type="number"
                                value={rsiThreshold}
                                onChange={(e) => setRsiThreshold(Number(e.target.value))}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                            />
                        </div>
                        <button
                            onClick={runSimulation}
                            disabled={isRunning}
                            className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${isRunning ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
                        >
                            {isRunning ? 'Running...' : 'Run Backtest'}
                        </button>
                    </div>
                </div>

                {/* Charts */}
                <div className="bg-white p-6 rounded-lg shadow lg:col-span-3">
                    <h2 className="text-xl font-semibold mb-4">Results Visualization</h2>
                    {backtestData.length > 0 ? (
                        <div className="h-96">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={backtestData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="time" />
                                    <YAxis yAxisId="left" domain={['auto', 'auto']} />
                                    <YAxis yAxisId="right" orientation="right" domain={[0, 100]} />
                                    <Tooltip />
                                    <Legend />
                                    <Line yAxisId="left" type="monotone" dataKey="price" stroke="#8884d8" name="Price" dot={false} />
                                    <Line yAxisId="right" type="monotone" dataKey="rsi" stroke="#82ca9d" name="RSI" dot={false} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    ) : (
                        <div className="h-96 flex items-center justify-center bg-gray-50 rounded border border-dashed">
                            <p className="text-gray-500">Run a simulation to see results</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
