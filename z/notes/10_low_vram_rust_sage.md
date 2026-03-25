# The Low-VRAM Rust Sage (6GB Hardware Guide)
*Running High-Precision Local AI on 4.5GB of VRAM*

If you are currently learning and working with a **6GB VRAM GPU**, you have to be mathematically precise with your "VRAM Budget." To leave room for your OS, your IDE (Zed), and your browser, we must target **~4.5GB of actual VRAM usage** for the AI model.

Here is your exact blueprint for a high-speed, local Rust assistant on lightweight hardware.

---

## 🚀 1. The Base Brain (Model Recommendation)
You cannot run 16B or 34B models. They will crash your system. You need an **SLM (Small Language Model)** that is "Punching above its weight" in Rust.

**The #1 Choice:** **Qwen2.5-Coder-3B-Instruct (GGUF 4-bit / 8-bit).**
*   **Why:** Qwen2.5-Coder is the new world leader for small models. The 3B (3 Billion parameter) version is surprisingly "aware" of Rust's borrow checker and syntax.
*   **VRAM Usage (at 4-bit):** ~2.1 GB.
*   **Headroom:** This leaves you ~2.4 GB of your "target 4.5GB" purely for the **Context Window** (the number of lines of code it can remember) and the OS.

**The "Ultra-Light" Alternative:** **Qwen2.5-Coder-1.5B-Instruct.** 
*   **VRAM Usage (at 8-bit):** ~1.7 GB. 
*   **Benefit:** Incredibly fast. On a 6GB card, this model will feel "instant."

---

## 🛠️ 2. The Setup: Ollama + Zed
To run this with almost zero configuration:

1.  **Install Ollama:** The easiest "local cloud" engine.
2.  **Download the model:** Open your terminal and run:
    *   `ollama run qwen2.5-coder:3b`
3.  **Connect to Zed:** In your Zed settings, point the "Language Model" section to `http://localhost:11434`.

---

## 🧠 3. The "Context Budget" (The Multi-Task Secret)
VRAM isn't just used by the AI's "Brain" (the weights); it is consumed by the **KV Cache** (the "Memory" of the current conversation). 

*   **The Rule:** If you give a 3B model 32,000 lines of context, your 6GB VRAM will fill up and crash.
*   **The Constraint:** Limit the context window to **4,096 tokens** (approx. 4,000 words/lines of code). This keeps the VRAM usage pinned safely around **3GB to 4GB**, leaving you the headroom you requested.

---

## 🎓 4. Current Learning Phase: How to Use It
Since you are a "Junior" learning Rust, do not let the AI write your whole project yet. Use the **"Single Function Proof"** strategy:

1.  **The Task:** Paste one specific function you are struggling with.
2.  **The Prompt:** *"Explain the ownership issue in this function and provide a Clippy-compliant fix in Rust. No markdown chatter."*
3.  **The Learning:** The 3B model is perfect for explaining **why** the Borrow Checker specifically is angry. It won't overthink; it just solves the immediate error.

### Why this works for the 2030s:
By starting on 6GB hardware now, you are learning the **"Efficiency Code."** Most people just throw more RAM at the problem. By learning to tune a 3B model to output perfect Rust code, you are preparing yourself to build the **cheap, low-power Sovereign Appliances** that will run on every factory floor in 2035. 

Would you like the exact Zed settings (`settings.json`) to connect to a local Ollama instance?
