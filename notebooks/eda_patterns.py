import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_insights():
    # Load Data
    file_path = 'data/raw/century_master.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    
    # Calculate Retrograde Count
    retro_cols = [c for c in df.columns if 'Retro' in c]
    df['Retro_Count'] = df[retro_cols].sum(axis=1)
    
    # Calculate Simple Return for display (Log Return exists, but users often think in %)
    df['Simple_Return'] = df['Close'].pct_change() * 100

    # Setup the figure
    fig = plt.figure(figsize=(15, 20))
    # Layout: 
    # Row 1: Time Series (Tall)
    # Row 2: Retrograde Bar
    # Row 3: Correlation Heatmap
    gs = fig.add_gridspec(3, 1, height_ratios=[1.5, 1, 1])

    # --- Plot 1: Price vs Aspect ---
    ax1 = fig.add_subplot(gs[0])
    
    # Plot S&P 500 (Left Axis, Log Scale)
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('S&P 500 (Log Scale)', color=color)
    ax1.semilogy(df.index, df['Close'], color=color, label='S&P 500', linewidth=1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_title('100 Years: S&P 500 & Saturn-Neptune Cycle', fontsize=16)

    # Plot Aspect (Right Axis)
    ax2 = ax1.twinx() 
    color = 'tab:orange'
    ax2.set_ylabel('Saturn-Neptune Angle (Degrees)', color=color)
    # Use alpha to not obscure price too much
    ax2.plot(df.index, df['Saturn_Neptune_Angle'], color=color, label='Saturn-Neptune', alpha=0.3, linewidth=1)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Vertical Red Lines for Drawdowns
    crashes = pd.to_datetime([
        '1929-10-01', 
        '1973-01-01', 
        '1987-10-01', 
        '2008-09-01', 
        '2020-03-01'
    ])
    
    for crash in crashes:
        ax1.axvline(x=crash, color='red', linestyle='--', alpha=0.7)
        ax1.text(crash, ax1.get_ylim()[1], crash.year, rotation=90, verticalalignment='bottom', color='red')

    # --- Plot 2: Retrograde Analysis ---
    ax3 = fig.add_subplot(gs[1])
    
    # Group by Retro Count
    retro_stats = df.groupby('Retro_Count')['Simple_Return'].mean()
    
    sns.barplot(x=retro_stats.index, y=retro_stats.values, palette='viridis', ax=ax3)
    ax3.set_title('Average Monthly Return vs. Number of Retrograde Outer Planets', fontsize=14)
    ax3.set_xlabel('Number of Planets Retrograde (Jupiter-Pluto)')
    ax3.set_ylabel('Avg Monthly Return (%)')
    ax3.axhline(0, color='black', linewidth=0.8)
    
    # Add value labels
    for i, v in enumerate(retro_stats.values):
        ax3.text(i, v + (0.05 if v > 0 else -0.15), f'{v:.2f}%', ha='center')

    # --- Plot 3: Correlation Matrix ---
    ax4 = fig.add_subplot(gs[2])
    
    # Select Speed columns and Return
    speed_cols = [c for c in df.columns if 'Speed' in c]
    # Include Returns
    corr_cols = speed_cols + ['Log_Return']
    
    corr_data = df[corr_cols].corr()
    
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, ax=ax4, fmt='.2f')
    ax4.set_title('Correlation: Planetary Speeds vs. Log Returns', fontsize=14)

    # Save
    plt.tight_layout()
    
    output_dir = 'data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'mundane_insights.png')
    
    plt.savefig(output_path)
    print(f"Visualization saved to: {output_path}")

if __name__ == "__main__":
    generate_insights()
