import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Layout and Theme Settings
st.set_page_config(page_title="Quant Analytics Pro", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Dark-Tech Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        background-color: #4A90E2 !important; color: white !important;
        border-radius: 8px !important; width: 100% !important; height: 45px !important;
        font-weight: bold !important; font-size: 16px !important;
        border: none !important; transition: 0.3s !important;
    }
    .stButton>button:hover { background-color: #357ABD !important; transform: scale(1.02); }
    .card-market {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .card-strategy {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .telemetry-box {
        background-color: #161b22; padding: 25px; border-radius: 12px; 
        border: 1px solid #30363d; min-height: 290px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Premium Top Banner
st.markdown("""
    <div style="background: linear-gradient(90deg, #0F2027 0%, #203A43 50%, #2C5364 100%); padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 25px; border-left: 8px solid #38ef7d;">
        <h1 style="color: white; margin: 0; font-family: 'Helvetica Neue', sans-serif; font-size: 32px;">📊 QUANTITATIVE TRADING INTEL & BACKTESTER</h1>
        <p style="color: #b2bec3; margin: 5px 0 0 0; font-size: 16px;">High-Frequency Algorithmic Analytics Platform for Global Asset Markets</p>
    </div>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
st.sidebar.markdown("<h2 style='color: #4A90E2;'>⚙️ ARCHITECTURE ENGINE</h2>", unsafe_allow_html=True)
ticker = st.sidebar.text_input("Enter Asset Ticker Symbol:", "AAPL").upper().strip()
st.sidebar.markdown("---")
st.sidebar.write("💡 **Tip:** Use `AAPL`, `TSLA`, `GOOG` for US Markets or `RELIANCE.NS`, `TCS.NS` for Indian Markets.")

run_btn = st.sidebar.button("DEPLOY ALGORITHM 🚀")

# Default Screen state when no button is pressed
if not run_btn:
    st.markdown("""
        <div style="background-color: #161b22; padding: 40px; border-radius: 12px; text-align: center; border: 1px dashed #30363d; margin-top: 50px;">
            <h3 style="color: #8b949e; margin: 0;">Welcome to the Terminal</h3>
            <p style="color: #58a6ff; margin: 10px 0 0 0;">Configure your asset ticker in the left sidebar and click "Deploy Algorithm" to instantly execute backtests and stream live signals.</p>
        </div>
    """, unsafe_allow_html=True)

# 4. Main Algorithm Execution
if run_btn:
    with st.spinner("⏳ Establishing API secure handshake & syncing historical pipelines..."):
        try:
            stock_obj = yf.Ticker(ticker)
            data = stock_obj.history(period="2y")
            
            if data.empty:
                st.warning(f"⚠️ Yahoo API timed out or refused connection for '{ticker}'. Falling back to secure asset data engine (AAPL).")
                ticker = "AAPL"
                stock_obj = yf.Ticker(ticker)
                data = stock_obj.history(period="2y")

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            # Strategy Logic
            data['Short_MA'] = data['Close'].rolling(window=5).mean()
            data['Long_MA'] = data['Close'].rolling(window=20).mean()
            clean_data = data.dropna(subset=['Short_MA', 'Long_MA']).copy()

            # Returns Backtesting
            clean_data['Market_Returns'] = clean_data['Close'].pct_change()
            clean_data['Signal'] = np.where(clean_data['Short_MA'] > clean_data['Long_MA'], 1.0, -1.0)
            clean_data['Strategy_Returns'] = clean_data['Market_Returns'] * clean_data['Signal'].shift(1)
            
            cumulative_market = (1 + clean_data['Market_Returns'].dropna()).cumprod() - 1
            cumulative_strategy = (1 + clean_data['Strategy_Returns'].dropna()).cumprod() - 1
            
            mkt_ret = cumulative_market.iloc[-1].item() * 100 if not cumulative_market.empty else 0
            str_ret = cumulative_strategy.iloc[-1].item() * 100 if not cumulative_strategy.empty else 0
            
            # Live Data metrics setup
            latest_row = clean_data.iloc[-1]
            live_price = latest_row['Close'].item()
            current_short_ma = latest_row['Short_MA'].item()
            current_long_ma = latest_row['Long_MA'].item()

            # --- FRONTEND INTERFACE GRID ---
            st.markdown(f"### 🎯 Real-Time Execution Intelligence for **{ticker}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class="card-market">
                        <h4 style="margin:0; color: #b2bec3; font-size:14px; text-transform:uppercase;">Asset Benchmark Return</h4>
                        <h1 style="margin:5px 0 0 0; color:white; font-size:36px;">{mkt_ret:.2f}%</h1>
                        <p style="margin:5px 0 0 0; color:#dfe6e9; font-size:12px;">Standard Buy-and-Hold strategy over 24 months.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="card-strategy">
                        <h4 style="margin:0; color: #e1f5fe; font-size:14px; text-transform:uppercase;">⚡ Quant Strategy Return</h4>
                        <h1 style="margin:5px 0 0 0; color:white; font-size:36px;">{str_ret:.2f}%</h1>
                        <p style="margin:5px 0 0 0; color:#e8f5e9; font-size:12px;">Moving Average Crossover simulation alpha output.</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                if current_short_ma > current_long_ma:
                    signal_html = "<div style='background-color: #1e4620; padding: 15px; border-radius: 8px; border-left: 5px solid #38ef7d; margin-top:15px;'><h3 style='margin:0; color:#38ef7d;'>🟢 STRONGLY SUGGEST TO BUY</h3><p style='margin:5px 0 0 0; color: white; font-size:12px;'>Bullish momentum breakout detected. Short-term average leads asset pricing indicators.</p></div>"
                elif current_short_ma < current_long_ma:
                    signal_html = "<div style='background-color: #611f1f; padding: 15px; border-radius: 8px; border-left: 5px solid #ff4d4d; margin-top:15px;'><h3 style='margin:0; color:#ff4d4d;'>🔴 STRONGLY SUGGEST TO SELL</h3><p style='margin:5px 0 0 0; color: white; font-size:12px;'>Bearish momentum drop detected. High exposure risk identified. Liquidation recommended.</p></div>"
                else:
                    signal_html = "<div style='background-color: #4d4d1f; padding: 15px; border-radius: 8px; border-left: 5px solid #ffeb3b; margin-top:15px;'><h3 style='margin:0; color:#ffeb3b;'>🟡 HOLD / MARKET NEUTRAL</h3><p style='margin:5px 0 0 0; color: white; font-size:12px;'>Sideways market movement. Wait for clearer vector indicators.</p></div>"

                # Fixed text visibility using inline color styles
                st.markdown(f"""
                    <div class="telemetry-box">
                        <h3 style="margin-top:0; color: #ffffff !important;">🚨 LIVE SIGNAL TELEMETRY</h3>
                        <p style="font-size:18px; margin: 10px 0; color: #ffffff !important;"><b>Current Price:</b> <span style="color:#38ef7d; font-weight:bold; font-size:20px;">${live_price:.2f}</span></p>
                        <p style="font-size:14px; color: #e0e0e0 !important; margin: 5px 0;"><b>5-Day Fast Momentum:</b> <span style="color:#ff4d4d;">${current_short_ma:.2f}</span> | <b>20-Day Trend Baseline:</b> <span style="color:#4A90E2;">${current_long_ma:.2f}</span></p>
                        <hr style="border-color:#30363d; margin: 15px 0;">
                        {signal_html}
                    </div>
                """, unsafe_allow_html=True)

            # --- ADVANCED MATPLOTLIB CHART ---
            st.markdown("---")
            st.subheader("📊 Interactive High-Density Analytical Chart")
            
            clean_data['Position'] = clean_data['Signal'].diff()
            
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(15, 6))
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#161b22')
            
            ax.plot(clean_data['Close'], label='Asset Close Price', color='#4A90E2', alpha=0.6, linewidth=2)
            ax.plot(clean_data['Short_MA'], label='5-Day Short MA (Fast)', color='#ff4d4d', linestyle='--', alpha=0.9)
            ax.plot(clean_data['Long_MA'], label='20-Day Long MA (Slow)', color='#38ef7d', linestyle='--', alpha=0.9)
            
            ax.scatter(clean_data[clean_data['Position'] == 2.0].index, clean_data['Short_MA'][clean_data['Position'] == 2.0], marker='^', s=150, color='#38ef7d', label='QUANT BUY TRIGGER', zorder=5)
            ax.scatter(clean_data[clean_data['Position'] == -2.0].index, clean_data['Short_MA'][clean_data['Position'] == -2.0], marker='v', s=150, color='#ff4d4d', label='QUANT SELL TRIGGER', zorder=5)
            
            ax.set_title(f"Quantitative Vector Map: {ticker} (24-Month Timeline)", fontsize=14, color='white', pad=15)
            ax.grid(True, color='#30363d', alpha=0.5, linestyle=':')
            ax.legend(loc='upper left', facecolor='#0e1117', edgecolor='#30363d')
            
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Execution Exception Core: {e}")