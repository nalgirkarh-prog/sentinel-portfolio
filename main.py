import sys
import os
import subprocess
import onboard
import database
import fetchers
import brain
import yfinance as yf

def push_alert(title, text):
    subprocess.run(["notify-send", "-u", "normal", "-a", "PortfolioAgent", title, text])

def get_nifty_state():
    try:
        n = yf.Ticker("^NSEI").history(period="1d")
        return f"Nifty 50: {n['Close'].iloc[-1]:.2f} ({((n['Close'].iloc[-1]-n['Open'].iloc[-1])/n['Open'].iloc[-1])*100:+.2f}%)"
    except:
        return "Nifty 50 Tracking Active"

def main():
    onboard.run_onboarding() # Enforce check
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [opening_30m | recommend | midday | closing]")
        sys.exit(1)
        
    mode = sys.argv[1]
    portfolio_data = database.get_portfolio()
    live_portfolio_str = fetchers.fetch_live_portfolio(portfolio_data)
    nifty_str = get_nifty_state()

    if mode == "opening_30m":
        decision = brain.query_agent("opening_30m", nifty_str, live_portfolio_str)
        push_alert("📊 Market Analysis (30m Post-Open)", decision)
    elif mode == "recommend":
        screened = fetchers.screen_cap_segments()
        decision = brain.query_agent("recommend", str(screened), live_portfolio_str)
        push_alert("💡 Cap-Segment Recommendations (<₹1000)", decision)
    elif mode == "midday":
        decision = brain.query_agent("midday", nifty_str, live_portfolio_str)
        push_alert("⚡ Midday Portfolio Action Plan", decision)
    elif mode == "closing":
        decision = brain.query_agent("closing", nifty_str, live_portfolio_str)
        push_alert("🔔 EOD Closing Bell Allocation", decision)

if __name__ == "__main__":
    main()
