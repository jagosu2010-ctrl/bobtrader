# MCP Servers and Financial Libraries Research - PowerTrader AI

**Version:** 2.0.0
**Last Updated:** 2026-01-18
**Research Date:** 2026-01-18
**Purpose:** Comprehensive research on MCP servers and financial libraries for potential integration

---

## Table of Contents

- [MCP Servers](#mcp-servers)
- [Alpha Vantage](#alpha-vantage)
- [CoinGecko](#coingecko)
- [Binance Servers](#binance-servers)
- [Bybit](#bybit)
- [CoinMarketCap](#coinmarketcap)
- [Dappier](#dappier)
- [OKX](#okx)
- [Armor Crypto](#armor-crypto)
- [Hive Crypto](#hive-crypto)
- [Crypto Fear/Greed](#crypto-feargreed)
- [Crypto Indicators](#crypto-indicators)
- [Crypto Sentiment](#crypto-sentiment)
- [CryptoPanic](#cryptopanic)
- [Freqtrade](#freqtrade)
- [Upbit](#upbit)
- [Uniswap](#uniswap)
- [TwelveData](#twelvedata)
- [Token Metrics](#token-metrics)
- [PaperInvest](#paperinvest)
- [Polymarket](#polymarket)

---

## MCP Servers

### OctagonAI MCP Servers

#### 1. Octagon Stock Market Data
**Repository/Website:** [GitHub](https://github.com/OctagonAI/octagon-stock-market-data-mcp) | [Docs](https://docs.octagonagents.com/guide/mcp-server.html)

**Description:** Provides specialized AI-powered stock market data and valuation analysis capabilities integrating with advanced stock data agents. Offers real-time market data, comprehensive technical indicators, and unlimited market intelligence.

**API Endpoints:** Stock price data, technical indicators, valuation analysis, market intelligence

**Use Cases for PowerTrader AI:** Real-time market monitoring, technical analysis integration, valuation models, AI-powered market research

**Dependencies:** Octagon API key

**Integration Difficulty:** Medium (Requires API key and setup)

**Recommendation:** Consider (Good for comprehensive stock data but requires Octagon API subscription)

---

#### 2. Octagon Market Data (Public Markets)
**Documentation:** [https://docs.octagonagents.com/guide/mcp-server.html](https://docs.octagonagents.com/guide/mcp-server.html)

**Description:** AI-powered financial research and analysis integrating with Octagon Market Intelligence API. Covers SEC filings, earnings call transcripts, financial metrics, and stock market data for 8,000+ public companies.

**API Endpoints:** SEC filings (10-K, 10-Q, 8-K, 20-F, S-1), Earnings call transcript analysis (10 years historical), Financial metrics/ratios (10 years historical), Stock market data (10,000+ tickers)

**Use Cases for PowerTrader AI:** Fundamental analysis, earnings call sentiment analysis, SEC filing parsing, historical financial data research

**Dependencies:** Octagon API key (OAuth or API key-based authentication)

**Integration Difficulty:** Medium

**Recommendation:** Use (Excellent for fundamental analysis and SEC data)

---

#### 3. Octagon Private Markets
**Documentation:** [https://docs.octagonagents.com/guide/mcp-server.html](https://docs.octagonagents.com/guide/mcp-server.html)

**Description:** Specialized AI agents for private company research covering 3M+ companies, funding rounds (500k+ deals), M&A/IPO transactions (2M+ deals), and debt transactions (1M+ deals).

**API Endpoints:** Private company research, VC funding analysis, M&A/IPO data, debt transaction research

**Use Cases for PowerTrader AI:** Pre-IPO research, private equity analysis, funding round tracking, VC deal flow monitoring

**Dependencies:** Octagon API key

**Integration Difficulty:** Medium

**Recommendation:** Consider (Valuable for private market research if that's a focus area)

---

### Alpha Vantage MCP

**Repository/Website:** [GitHub](https://github.com/matteoantoci/mcp-alphavantage) | [Official URL](https://mcp.alphavantage.co/mcp) | [Docs](https://www.alphavantage.co/documentation/)

**Description:** Official Alpha Vantage MCP server providing comprehensive financial data endpoints. Covers stocks, options, forex, cryptocurrencies, commodities, technical indicators, and economic data.

**API Endpoints:** TIME_SERIES_DAILY_ADJUSTED, REALTIME_OPTIONS, COMPANY_OVERVIEW, 50+ technical indicators (RSI, MACD, SMA, Bollinger Bands, etc.), economic data, crypto data, forex data

**Use Cases for PowerTrader AI:** Multi-asset trading (stocks, forex, crypto), technical analysis automation, economic data integration, options chain analysis

**Dependencies:** Alpha Vantage API key (free tier available), Python/Node.js

**Integration Difficulty:** Easy (Official server, well-documented)

**Recommendation:** Use (One of the best overall - comprehensive coverage, official support, free tier available)

---

### CoinGecko MCP

**Repository/Website:** [Documentation](https://docs.coingecko.com/docs/mcp-server) | [Public Endpoint](https://mcp.api.coingecko.com/mcp)

**Description:** Official CoinGecko MCP server for crypto price & market data. World's largest independent crypto data aggregator with 18,000+ coins across 600+ categories, 1,000+ exchanges integrated.

**API Endpoints:** 76+ available tools including price feeds, market data, metadata, historical data, NFT collections, DeFi pools data across 250+ blockchain networks, 15M+ tokens

**Use Cases for PowerTrader AI:** Real-time crypto price tracking, market cap analysis, token discovery, DeFi analytics, multi-chain support

**Dependencies:** No API key required for public beta (rate limits apply), Pro version requires API key

**Integration Difficulty:** Easy (Remote server, no setup required)

**Recommendation:** Use (Excellent - no setup needed, comprehensive coverage, public beta available)

---

### Binance MCP Servers

#### 1. AnalyticAce BinanceMCP
**Repository:** [GitHub](https://github.com/AnalyticAce/BinanceMCPServer)

**Description:** Unofficial tools and server implementation for Binance's MCP. Supports developers building crypto trading AI agents.

**API Endpoints:** Trading operations, account management, market data access (specific tools vary by implementation)

**Use Cases for PowerTrader AI:** Binance trading automation, portfolio management, real-time market data from Binance

**Dependencies:** Binance API keys, Python/Node.js

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good alternative, but multiple implementations exist)

#### 2. tienan92it Binance MCP
**Repository:** [GitHub](https://github.com/tienan92it/binance-mcp)

**Description:** MCP server exposing Binance cryptocurrency exchange data to LLM agents. Provides real-time and historical market data through standardized interface.

**API Endpoints:** Live price data, order book access, historical price data, trading capabilities

**Use Cases for PowerTrader AI:** Real-time Binance trading, order book analysis, historical backtesting

**Dependencies:** Binance API credentials, Python

**Integration Difficulty:** Medium

**Recommendation:** Consider

#### 3. alexcandrabersiva Bin-MCP
**Repository:** [Awesome MCP Servers](https://mcpservers.org/servers/MCP-Mirror/alexcandrabersiva_bin-mcp)

**Description:** Comprehensive Binance Futures API access with 17 essential trading tools across account information and market data categories.

**API Endpoints:** Account information, market data, smart ticker caching (5-min refresh), authentication handling, active symbol filtering, order management, risk management tools

**Use Cases for PowerTrader AI:** Binance futures trading, risk management, position management

**Dependencies:** Binance API key and secret key, pip install

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good for futures trading focus)

#### 4. shanrichard Binance MCP
**Documentation:** [Skywork Guide](https://skywork.ai/skyware/en/binance-mcp-server-guide-ai-engineers/1980550812654673920)

**Description:** Definitive Binance MCP server with 30+ tools for AI engineers.

**API Endpoints:** 30+ tools (comprehensive trading, market data, and account management)

**Use Cases for PowerTrader AI:** Complete Binance integration, automated trading strategies

**Dependencies:** Binance API keys

**Integration Difficulty:** Medium

**Recommendation:** Consider (Feature-rich but evaluate against other implementations)

#### 5. snjyor Binance MCP
**Documentation:** [Skywork Guide](https://skywork.ai/skyware/en/ai-crypto-binance-mcp/1980925217705484288)

**Description:** Real-time data and low latency with comprehensive data access across Binance. Read-only approach with robust error handling.

**API Endpoints:** Live price data, order book snapshots, historical data, real-time WebSocket updates

**Use Cases for PowerTrader AI:** High-frequency data analysis, real-time monitoring

**Dependencies:** Binance API keys

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good for read-only focus)

**Overall Binance MCP Recommendation:** Use one of the implementations, but evaluate based on specific needs (spot vs futures, trading vs read-only). Multiple community implementations available.

---

### Bybit MCP Servers

#### 1. ethancod1ng Bybit MCP Server
**Repository:** [GitHub](https://github.com/ethancod1ng/bybit-mcp-server)

**Description:** MCP server integrating AI assistants with Bybit cryptocurrency exchange APIs. Enables automated trading, market data access, and account management.

**API Endpoints:** Trading operations, market data access, account management

**Use Cases for PowerTrader AI:** Bybit trading automation, market analysis, portfolio management

**Dependencies:** Bybit API keys, Node.js

**Integration Difficulty:** Medium

**Recommendation:** Consider

#### 2. sammcj Bybit MCP
**Repository:** [GitHub](https://github.com/sammcj/bybit-mcp)

**Description:** Ollama MCP server for Bybit exchange integration.

**API Endpoints:** Bybit market data and trading operations

**Use Cases for PowerTrader AI:** Bybit integration, Ollama-based workflows

**Dependencies:** Bybit API credentials

**Integration Difficulty:** Medium

**Recommendation:** Skip (If not using Ollama)

#### 3. BCusack Bybit Py MCP
**Documentation:** [Glama](https://glama.ai/mcp/servers/@BCusack/bybit-py-mcp)

**Description:** Comprehensive Bybit v5 API access with full trading operations. Production-ready with Docker support and VS Code integration.

**API Endpoints:** Server time, tickers, order book, recent trades, candlesticks, trading operations, positions management

**Use Cases for PowerTrader AI:** Complete Bybit automation, trading strategies, position management

**Dependencies:** Bybit API keys, Docker (optional), Python

**Integration Difficulty:** Medium

**Recommendation:** Use (Most comprehensive, production-ready)

**Overall Bybit MCP Recommendation:** Use BCusack implementation (most comprehensive, production-ready).

---

### CoinMarketCap MCP

**Repository/Website:** [GitHub](https://github.com/shinzo-labs/coinmarketcap-mcp) | [API Docs](https://coinmarketcap.com/api/documentation/v1/)

**Description:** Complete MCP implementation for CoinMarketCap API. Provides standardized interface for cryptocurrency market data, exchange info, and blockchain metrics.

**API Endpoints:** Cryptocurrency listings, quotes, info, market pairs, OHLCV data, conversion, exchange listings/info/map, global metrics, Fear & Greed Index

**Use Cases for PowerTrader AI:** Crypto market data, price tracking, market sentiment via Fear & Greed, global metrics

**Dependencies:** CoinMarketCap API key, Node.js, subscription tier selection (Basic, Hobbyist, Startup, Standard, Professional, Enterprise)

**Integration Difficulty:** Easy (Well-documented)

**Recommendation:** Use (Comprehensive, well-maintained, good docs)

---

### Dappier MCP

**Repository/Website:** [GitHub](https://github.com/DappierAI/dappier-mcp) | [Docs](https://docs.dappier.com/integrations/dappier-mcp-server-integration)

**Description:** Real-time, rights-cleared data from trusted sources. Enables AI to access specialized models including web search, news, sports, financial stock market data, crypto data, and exclusive content from premium publishers.

**API Endpoints:** Real-Time Web Search (Google results, news, weather, stock prices), Stock Market Data (Polygon.io integration), AI-Powered Recommendations (Sports, lifestyle, pets, travel), Crypto Data

**Use Cases for PowerTrader AI:** Real-time news integration, stock market data aggregation, web search for research, crypto data from premium sources

**Dependencies:** Dappier API key, Python, uv package manager

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good for multi-source data aggregation, especially news and web search)

---

### OKX MCP Servers

#### 1. badger3000 OKX MCP Server
**Repository:** [GitHub](https://github.com/badger3000/okx-mcp-server)

**Description:** MCP server fetching real-time cryptocurrency data from OKX exchange with enhanced visualization and WebSocket live updates.

**API Endpoints:** get_price (latest price with visual formatting), get_candlesticks (historical data with ASCII charts), subscribe_ticker (WebSocket updates), get_live_ticker (live WebSocket data), unsubscribe_ticker

**Use Cases for PowerTrader AI:** OKX price monitoring, WebSocket-based real-time data, technical chart visualization

**Dependencies:** OKX API credentials, Node.js

**Integration Difficulty:** Medium

**Recommendation:** Consider

#### 2. memetus OKX MCP
**Documentation:** [Cursor MCP](https://cursormcp.dev/mcp-servers/778-okx-mcp-server)

**Description:** Blockchain data and market price data via OKX API. Enables asset prices, transaction data, account history, and trade instruction data retrieval.

**API Endpoints:** Balance operations (supported chains, token balances, total balances, total value), Gateway operations (supported chains, broadcast transactions, gas limits, gas prices, transaction orders)

**Use Cases for PowerTrader AI:** Blockchain analytics, account management, gas estimation

**Dependencies:** OKX API keys

**Integration Difficulty:** Medium

**Recommendation:** Consider

#### 3. maxbarinov OKX MCP
**Documentation:** [PulseMCP](https://pulsemcp.com/servers/okx)

**Description:** Read-only access to OKX account portfolios, trading positions, order history, and account summaries for portfolio management and trading analytics.

**API Endpoints:** Portfolio data, trading positions, order history, account summaries

**Use Cases for PowerTrader AI:** Portfolio monitoring, performance tracking, order analysis

**Dependencies:** OKX API credentials

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good for read-only portfolio analysis)

#### 4. aahl OKX MCP
**Documentation:** [PulseMCP](https://pulsemcp.com/servers/aahl-okx)

**Description:** Trading and portfolio management for OKX cryptocurrency exchange.

**API Endpoints:** Trading and portfolio management tools

**Use Cases for PowerTrader AI:** OKX trading automation, portfolio management

**Dependencies:** OKX API keys

**Integration Difficulty:** Medium

**Recommendation:** Consider

**Overall OKX MCP Recommendation:** Consider based on specific needs (trading vs read-only, market data vs blockchain data).

---

### Armor Crypto MCP

**Repository/Website:** [GitHub](https://github.com/armorwallet/armor-crypto-mcp) | [Docs](https://www.augmentcode.com/mcp/armor-crypto-mcp)

**Description:** Backend server for AI-agent access to crypto ecosystem - wallet management, swaps, DCA/limit/stop-loss orders, staking and cross-chain operations. Currently supports Solana (alpha), planned support for 12+ blockchains.

**API Endpoints (10 tools):** Wallet Management (create, manage, organize), Grouping & Organization, Archiving, Normal swap, DCA (place/list/cancel), Scheduled Orders, Limit Orders (place/list/cancel), Staking and Unstaking, Token Search & Trending Tokens, Statistical Calculator

**Use Cases for PowerTrader AI:** Automated wallet management, DCA strategies, stop-loss/take-profit orders, staking automation, cross-chain operations

**Dependencies:** Python, MCP RPC URL, MCP API key, wallet private keys

**Integration Difficulty:** Hard (Requires wallet management, private keys, blockchain understanding)

**Recommendation:** Consider (Powerful but complex - best for DeFi-focused workflows, not beginner-friendly)

---

### Hive Crypto MCP

**Repository/Website:** [GitHub](https://github.com/hive-intel/hive-crypto-mcp) | [Docs](https://hiveintelligence.xyz/mcp-docs) | [Remote Endpoint](https://hiveintelligence.xyz/mcp)

**Description:** Official crypto MCP server enabling instant blockchain data access for AI applications. Connects to 60+ blockchains with real-time crypto data, DeFi analytics, and on-chain intelligence. Cloud-based, no local installation required.

**API Endpoints (200+ tools):** Market data, on-chain analytics, token prices, liquidity pools, NFTs, smart contracts, DeFi protocols across 60+ chains

**Use Cases for PowerTrader AI:** Multi-chain blockchain data, DeFi analytics, token discovery, on-chain analysis, portfolio tracking across chains

**Dependencies:** No local installation - cloud endpoint, no API keys required

**Integration Difficulty:** Easy (Remote endpoint, no setup)

**Recommendation:** Use (Excellent - comprehensive, free, no setup, multi-chain)

---

### Crypto Fear/Greed MCP

**Repository:** [GitHub](https://github.com/kukapay/crypto-feargreed-mcp)

**Description:** Provides real-time and historical cryptocurrency market sentiment data through Fear & Greed Index API. Analyzes market psychology and potential price movements.

**API Endpoints:** Real-time Fear & Greed Index, historical Fear & Greed data, sentiment analysis

**Use Cases for PowerTrader AI:** Market sentiment analysis, contrarian trading strategies, market psychology monitoring

**Dependencies:** Fear & Greed API access, Python

**Integration Difficulty:** Easy

**Recommendation:** Use (Simple, valuable for sentiment analysis)

---

### Crypto Indicators MCP

**Repository:** [GitHub](https://github.com/kukapay/crypto-indicators-mcp)

**Description:** MCP server providing 50+ cryptocurrency technical analysis indicators and trading strategies. Enables quantitative strategy development without implementing complex algorithms.

**API Endpoints (78 tools):** 50+ technical analysis indicators (RSI, MACD, SMA, EMA, Bollinger Bands, etc.), trading strategies, live-price adapters

**Use Cases for PowerTrader AI:** Technical analysis automation, trading strategy development, quantitative analysis, signal generation

**Dependencies:** Node.js 18+, npm, optional exchange API keys (BINANCE_API_KEY, etc.)

**Integration Difficulty:** Medium

**Recommendation:** Use (Comprehensive indicators, well-maintained, 106 stars)

---

### Crypto Sentiment MCP

**Repository:** [GitHub](https://github.com/kukapay/crypto-sentiment-mcp)

**Description:** Delivers cryptocurrency sentiment analysis to AI agents leveraging Santiment's aggregated social media and news data.

**API Endpoints:** get_sentiment_balance (positive vs negative), get_social_volume (mentions), alert_social_shift (spikes/drops), trending word identification, dominance measurement

**Use Cases for PowerTrader AI:** Social sentiment monitoring, volume shift alerts, trend detection, narrative tracking

**Dependencies:** Santiment API access, Python

**Integration Difficulty:** Medium

**Recommendation:** Use (Valuable for sentiment-based trading)

---

### CryptoPanic MCP

**Repository:** [GitHub](https://github.com/kukapay/cryptopanic-mcp-server)

**Description:** Provides latest cryptocurrency news to AI agents, powered by CryptoPanic news aggregation API.

**API Endpoints:** get_crypto_news (kind: "news" or "media", num_pages: 1-10)

**Use Cases for PowerTrader AI:** Real-time news monitoring, event-driven trading, content aggregation

**Dependencies:** CryptoPanic API key and plan, Python

**Integration Difficulty:** Easy

**Recommendation:** Use (Simple, effective for news integration)

---

### Freqtrade MCP

**Repository:** [GitHub](https://github.com/kukapay/freqtrade-mcp)

**Description:** MCP server integrating with Freqtrade cryptocurrency trading bot. Enables automated trading operations through REST API.

**API Endpoints (17 tools):** Get market data, view bot status, get profit summary, execute buy/sell orders, start/stop trading bot, position management

**Use Cases for PowerTrader AI:** Automated trading bot control, strategy management, backtesting integration, trade monitoring

**Dependencies:** Python 3.10+, running Freqtrade instance with REST API enabled, freqtrade-client, MCP CLI

**Integration Difficulty:** Medium (Requires Freqtrade setup)

**Recommendation:** Use (If already using Freqtrade - excellent integration)

---

### Upbit MCP

**Repository/Website:** [GitHub](https://github.com/solangii/upbit-mcp-server)

**Description:** MCP server for Upbit Cryptocurrency Exchange OpenAPI. Provides market data, account information, order management, and technical analysis.

**API Endpoints:** Market data (ticker, orderbook, trades, candle data, market summary), Account information (balances, order history, deposits/withdrawals), Trading operations (limit/market orders, order cancellation), Technical analysis tools

**Use Cases for PowerTrader AI:** Korean market access, Upbit trading automation, technical analysis integration

**Dependencies:** Upbit API keys, Python

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good for Korean market trading)

---

### Uniswap MCP Servers

#### 1. Uniswap Trader MCP
**Documentation:** [FlowHunt](https://www.flowhunt.io/mcp-servers/uniswap-trader-mcp/)

**Description:** Enables AI agents to automate token swaps on Uniswap DEX across multiple blockchains. Supports multi-hop route optimization and trading strategies.

**API Endpoints:** getPrice (price quotes for swaps), multi-chain support (Ethereum, Optimism, Polygon, Arbitrum, Celo, BNB Chain, Avalanche, Base)

**Use Cases for PowerTrader AI:** DeFi trading on Uniswap, automated swaps, cross-chain arbitrage, liquidity management

**Dependencies:** Uniswap integration, blockchain RPC endpoints

**Integration Difficulty:** Hard (Requires DeFi/DEX understanding)

**Recommendation:** Consider (For DeFi-specific workflows)

#### 2. Uniswap PoolSpy MCP
**Repository:** [GitHub](https://github.com/kukapay/uniswap-poolspy-mcp)

**Description:** Tracks newly created liquidity pools on Uniswap across nine blockchain networks. Provides real-time data on pool creation, transaction counts, volume, and TVL.

**API Endpoints:** Pool monitoring across 9 networks (Ethereum, Base, Optimism, Arbitrum, Polygon, BNB Chain, Avalanche, Celo, Blast), customizable time ranges, sorting by metrics

**Use Cases for PowerTrader AI:** Liquidity pool discovery, new token tracking, DeFi analytics, TVL monitoring

**Dependencies:** Python 3.10+, uv, The Graph API key

**Integration Difficulty:** Medium

**Recommendation:** Consider (For liquidity analytics and pool discovery)

**Overall Uniswap MCP Recommendation:** Consider for DeFi-specific workflows; evaluate based on trading vs analytics needs.

---

### TwelveData MCP

**Repository/Website:** [GitHub](https://github.com/twelvedata/mcp) | [Official URL](https://mcp.twelvedata.com/) | [Website](https://twelvedata.com/)

**Description:** Official Twelve Data MCP server providing real-time financial market data via WebSocket. Offers unified access to stocks, forex, cryptocurrencies, ETFs, fundamentals, and more.

**API Endpoints:** Real-time quotes via WebSocket, historical OHLCV price data, instrument metadata, stock/forex/crypto data, ETFs, fundamentals data

**Use Cases for PowerTrader AI:** Multi-asset trading (stocks, forex, crypto), real-time streaming, backtesting, fundamental data integration

**Dependencies:** Twelve Data API key (free tier available)

**Integration Difficulty:** Easy (Official server, remote endpoint available)

**Recommendation:** Use (Excellent - comprehensive financial data, official support, free tier available)

---

### Token Metrics MCP

**Documentation:** [Blog](https://tokenmetrics.com/blog/crypto-mcp-server-token-metrics-brings-one-key-data-to-openai-claude-cursor-windsurf) | [Integration](https://mcp.composio.dev/token_metrics)

**Description:** Token Metrics MCP providing AI-powered cryptocurrency data and insights for building trading bots, dashboards, and portfolio tools.

**API Endpoints:** Real-time crypto data, AI-powered insights, 5+ tools for token analysis

**Use Cases for PowerTrader AI:** AI-powered crypto analysis, token research, portfolio analytics

**Dependencies:** Token Metrics API key

**Integration Difficulty:** Medium

**Recommendation:** Consider (Good for AI-enhanced crypto analysis)

---

### PaperInvest MCP

**Repository/Website:** [GitHub](https://github.com/paperinvest/mcp-server) | [Docs](https://docs.paperinvest.io/mcp-protocol)

**Description:** Official MCP server for Paper's trading platform. Enables AI assistants to trade, manage portfolios, and analyze market data through conversational interfaces with real-time execution and market simulation.

**API Endpoints:** Account Management (get_account, update_account, freeze_account), Portfolio Management (create_portfolio, get_portfolio, get_account_portfolios), Trading (create_order, cancel_order, create_batch_orders), Order Management, Market Data, Portfolio Analytics

**Use Cases for PowerTrader AI:** Paper trading simulation, strategy backtesting, portfolio management, educational trading

**Dependencies:** Paper Trading Account, API key, Node.js

**Integration Difficulty:** Medium

**Recommendation:** Use (Excellent for paper trading, backtesting, and strategy development without real money risk)

---

### Polymarket MCP

**Repository/Website:** [GitHub](https://github.com/berlinbra/polymarket-mcp)

**Description:** MCP Server for Polymarket's Gamma Markets API. Fetches and analyzes prediction market data for financial insights and decision support.

**API Endpoints:** Prediction market data, market odds, betting/trading on prediction markets, market analysis

**Use Cases for PowerTrader AI:** Prediction market trading, event-based speculation, sentiment from prediction markets

**Dependencies:** Polymarket API access, Python

**Integration Difficulty:** Medium

**Recommendation:** Consider (Niche - valuable for prediction markets, but specific use case)

---

## Summary Recommendations

### Top Picks for PowerTrader AI (Must Use - Easy Integration)

1. **CoinGecko MCP** - No setup, public beta, comprehensive crypto data
2. **Hive Crypto MCP** - 200+ tools, 60+ chains, no installation, free
3. **CryptoPanic MCP** - Simple news integration
4. **Crypto Fear/Greed MCP** - Valuable sentiment indicator
5. **PaperInvest MCP** - Excellent for backtesting and paper trading

### Should Use (High Value):

6. **Alpha Vantage MCP** - Comprehensive multi-asset data (stocks, forex, crypto)
7. **TwelveData MCP** - Official, real-time WebSocket, comprehensive coverage
8. **CoinMarketCap MCP** - Well-maintained, comprehensive crypto data
9. **OctagonAI MCP (Public Markets)** - SEC filings, earnings transcripts, fundamentals
10. **Crypto Indicators MCP** - 50+ technical indicators, well-maintained

### Consider (Specialized Use Cases):

11. **Crypto Sentiment MCP** - Social sentiment analysis
12. **Freqtrade MCP** - If using Freqtrade bot
13. **BCusack Bybit MCP** - Most comprehensive Bybit integration
14. **Dappier MCP** - Multi-source aggregation (news, stocks, web)
15. **Uniswap MCP** - DeFi trading needs

### Evaluate Based on Needs:

16. **Armor Crypto MCP** - Powerful but complex (DeFi/wallet focus)
17. **Binance MCP Servers** - Multiple implementations, evaluate based on needs
18. **OKX MCP Servers** - Evaluate based on trading vs read-only needs
19. **Token Metrics MCP** - AI-enhanced crypto analysis
20. **Upbit MCP** - Korean market access
21. **CoinAPI MCP** - Unified data but commercial API required
22. **Polymarket MCP** - Prediction markets niche

---

**Last Updated:** 2026-01-18
**Researcher:** Librarian Agent (3m 0s)

---

**DO NOT TRUST THE POWERTRADER FORK FROM Drizztdowhateva!!!**

This is my personal trading bot that I decided to make open source. This system is meant to be a foundation/framework for you to build your dream bot!
