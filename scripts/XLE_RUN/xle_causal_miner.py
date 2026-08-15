import pandas as pd
import numpy as np
import os
import sys
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.GraphUtils import GraphUtils

# Root Path
ROOT = r"d:\ANTI-GRAVITY\MEDINI BASE\v2\ORION-V5-ACE-5.5"

def run_causal_miner():
    print("=== ACE: ELITE CAUSAL MINER (PC ALGORITHM) ===")
    
    file_path = os.path.join(ROOT, 'data/enriched/US/ENERGY_MasterV70.csv')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    
    # 1. Variable Selection (Focus on Causality)
    # We want to see if Cosmic Dimensions CAUSE the price move.
    cols = ['Close', 'SMI_Base', 'Ketu_Deg', 'Saturn_Deg', 'Mars_Speed', 'Nakshatra', 'Tithi']
    data = df[cols].dropna().values
    
    # 2. PC Algorithm: Finding the Directed Acyclic Graph (DAG)
    print("Executing PC Algorithm (Fisher-Z Independence Testing)...")
    cg = pc(data, 0.05, "fisherz")
    
    # 3. Interpret Results
    nodes = cols
    edges = []
    
    from causallearn.utils.GraphUtils import GraphUtils
    
    for edge in cg.G.get_graph_edges():
        u_node = edge.get_node1()
        v_node = edge.get_node2()
        
        # Mapping back to our names
        # causal-learn nodes are X1, X2...
        u_idx = int(u_node.get_name()[1:]) - 1
        v_idx = int(v_node.get_name()[1:]) - 1
        u_name = nodes[u_idx]
        v_name = nodes[v_idx]
        
        # Check direction
        endpoint1 = edge.get_endpoint1().name
        endpoint2 = edge.get_endpoint2().name
        
        if endpoint1 == 'CIRCLE' or endpoint2 == 'CIRCLE': direction = "<->"
        elif endpoint1 == 'TAIL' and endpoint2 == 'ARROW': direction = "-->"
        else: direction = "---"
        
        edges.append(f"{u_name} {direction} {v_name}")

    # 4. Save Discovery Report
    report_path = os.path.join(ROOT, 'scripts/XLE_RUN/docs/CAUSAL_DISCOVERIES.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 🏛️ Elite Discovery: Causal Market Mechanics 🏹\n\n")
        f.write("**Algorithm:** PC (Peter-Clark) Causal Discovery\n")
        f.write("**Dataset:** XLE Master V70\n\n")
        f.write("## 🎯 The Causal Graph\n")
        f.write("The following directed relationships were found mathematically:\n\n")
        for e in edges:
            f.write(f"- {e}\n")
        f.write("\n\n## 🛡️ Strategic Interpretation\n")
        f.write("Unlike correlation, these arrows prove the **Flow of Karma.** If Saturn --> Close is found, it means Saturn's position is a physical cause of the price move.\n")

    print(f"Successfully generated: {report_path}")
    print("\nCausal Relationships Found:")
    for e in edges: print(e)

if __name__ == "__main__":
    run_causal_miner()
