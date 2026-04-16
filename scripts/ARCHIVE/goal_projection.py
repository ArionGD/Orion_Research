import pandas as pd
import numpy as np

def calculate_mint_run():
    print("=== ACE: SOVEREIGN GOLD-MINT PROJECTION (2026-2030) ===")
    print("Strategy: 15X Strike in April 2026 + $500 Monthly DCA + Bull Compounding.")
    
    # Starting Conditions
    initial_cap = 500.0
    monthly_dca = 500.0
    target_cap = 100000.0
    
    # 1. THE STRIKE (April 2026)
    # The SMI 9.9 Fracture triggers a 15X Alpha event.
    month_1_cap = initial_cap * 15.0 # Total: $7,500
    
    print(f"\nMonth 01 (APR 2026): The SMI 9.9 Strike")
    print(f"| Capital Start: ${initial_cap:.2f}")
    print(f"| Alpha Multiplier: 15X (April Reset)")
    print(f"| Capital After Strike: ${month_1_cap:,.2f}")
    
    # 2. THE RECOVERY (Post-Strike Compounding)
    # Average Monthly Bull Return: 2.5% (Golden Era / 30% Annualized)
    bull_rate = 0.025
    
    current_cap = month_1_cap
    month = 1
    
    history = []
    
    while current_cap < target_cap:
        month += 1
        
        # Monthly DCA
        current_cap += monthly_dca
        
        # Monthly Market Growth (Bull Run)
        growth = current_cap * bull_rate
        current_cap += growth
        
        history.append({
            'Month': month,
            'Capital': current_cap,
            'Growth': growth
        })
        
        # Break if it takes too long (Sanity)
        if month > 120: break 

    # Detailed Table
    print("\nMONTH-BY-MONTH PROGRESSION:")
    print(f"{'MONTH':<8} | {'INVESTED':<12} | {'CAPITAL':<15} | {'STATUS'}")
    print("-" * 55)
    
    for h in history[::6]: # Print every 6 months to keep it clean
        invested = 500 + (h['Month']-1)*500
        print(f"Month {h['Month']:<3} | ${invested:<10,.0f} | ${h['Capital']:<14,.2f} | GROWING")
        
    print("-" * 55)
    print(f"TARGET REACHED: Month {month}")
    print(f"TOTAL TIME: {month // 12} Years and {month % 12} Months.")
    print(f"TOTAL CAPITAL: ${current_cap:,.2f}")
    print(f"TOTAL INVESTED: ${500 + (month-1)*500:,.0f}")
    print("="*60)

if __name__ == "__main__":
    calculate_mint_run()
