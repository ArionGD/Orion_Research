# Sovereign Architect: Training Sprint Day 1 Checklist
*Beginning the Master Data Collection for Rust & Ada*

To build your "Incorruptible" AI engines, you must begin with the **Gold Data.** You are not looking for "Chat" data; you are looking for **"Binary Truth"** data—code that has already been verified by a compiler or a formal prover.

---

## 🛠️ 1. Hardware & Environment Setup
Before you scrape a single line of code, you need your "Black Box" environment ready to receive it.

*   **Storage Tooling:** Use a **PostgreSQL** database or a simple **JSONL** (JSON Lines) file structure to store your raw code snippets. 
*   **The Model Base:** Pull the latest 7B "Instruct" model into your local environment for testing as you collect data.
    *   **Command:** `ollama run qwen2.5-coder:7b` (This is your "Architect" baseline).

---

## 🏗️ 2. The Rust Gold Mine (Step 1)
**Goal:** Collect 50-100GB of High-Precision Rust.

1.  **Scrape GitHub Rust Projects:** Focus on the top 1,000 crates in the Rust ecosystem (Tokio, Serde, Actix, Axum). These are the most vetted, most "Safe" lines of code on Earth.
2.  **The Standard Library:** Download and tokenize the entire **Rust Standard Library** (`std`). This is the "Pure Logic" of your future AI.
3.  **The "Fix-It" Dataset:** Search GitHub Issues for labels like `bug`, `compiler-error`, or `borrow-checker`. Capture the "Broken Code" and the "Final Fixed Commit." This is how you train the AI to **solve** problems, not just guess.

---

## 🛡️ 3. The Ada/SPARK Gold Mine (Step 1)
**Goal:** Collect 5-10GB of Formally Proved Ada.

1.  **AdaCore Repos:** Scrape everything in the **AdaCore** and **GNAT** GitHub organizations. They are the keepers of the modern Ada flame.
2.  **SPARK Solutions:** Search for projects that use the **SPARK 2014 or SPARK 2005** provers. These contain the "Mathematical Proofs" you need.
3.  **Synthetic Bridging:** Because high-quality SPARK is rare, use your **Qwen2.5-Coder-7B** to translate your small, high-quality Rust codebases into Ada. Then, run the **SPARK Prover** on them. If they pass, you have now created **Professional-Grade Synthetic Training Data.**

---

## 🧬 4. The "Compiler Teacher" Script (Draft)
Start building a simple Python script today that does this:
1.  **Reads** a snippet of Rust code from your database.
2.  **Saves** it to a temporary `main.rs` file.
3.  **Executes** `cargo check --message-format=json`.
4.  **Stores** the result. 
    *   If Result = **Pass**, tag the data as **"Master Logic."**
    *   If Result = **Fail**, tag the data as **"Learning Path"** and include the error code.

**Summary:** 
Your mission for the next 7 days is **Data Aggregation.** By the end of this week, you should have a massive, local, air-gapped database of **Verified Binary Correctness.** 

Are you ready to build the Python "Scraper & Compiler" script that starts filling your database?
