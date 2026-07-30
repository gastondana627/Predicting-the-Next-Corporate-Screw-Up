# Benchmark Results & Corpus Summary: Predict Emerging Data Misappropriation Targets

This document outlines the empirical findings, consensus company rankings, and model execution metrics across the 15 frontier models that successfully cleared the 300-point soft-grading adversarial evaluation.

---

## 📊 Evaluation Corpus Metrics
* **Total Passing Models:** 15 Frontier Models
* **Total Structured Prediction Logs:** 150 Enterprise Records (15 models $\times$ 10 targets each)
* **Evaluation Architecture:** 300-Point Soft-Grading Rubric across 84 granular constraints (including dynamic hexadecimal checksums, vocabulary exclusion, and quad-jurisdictional statutory mapping).

---

## 🏆 Top Consensus Target Companies
Aggregating predictions across all passing runs reveals strong cross-architecture convergence on high-risk industry targets:

| Rank | Company Name | Model Vote Count | Primary Exposure / Risk Vector |
| :--- | :--- | :---: | :--- |
| **1** | **Figma** | **7 Models** | Collaborative design asset harvesting, workspace training telemetry use, and file-origin compliance risks. |
| **2** | **ByteDance** | **5 Models** | Biometric telemetry capture, video processing pipelines, and behavioral pattern mining. |
| **3** | **Canva** | **5 Models** | Unconsented template design aggregation, content indexing bypass, and visual asset appropriation. |
| **4** | **Hugging Face** | **5 Models** | Open repository weight distribution and unverified training corpus aggregation. |
| **5 (Tie)** | **Instacart** | **5 Models** | Automated pricing indexation, inventory reconnaissance, and consumer consumption profiling. |
| **5 (Tie)** | **Jasper** | **5 Models** | Automated copywriting extraction, paywall bypass, and blog text scraping. |

---

## 🤖 Passing Model Lineages
The evaluation corpus successfully validated outputs from the following architectural families:
* **Gemini Family:** `gemini-3-flash-preview`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite-preview`, `gemini-3.6-flash`, `gemini-2.5-flash`, `gemini-3.1-pro-preview`, `gemini-2.5-pro`
* **OpenAI Family:** `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-5.4-2026-03-05`
* **Claude Family:** `claude-sonnet-4-20250514`, `claude-sonnet-4-5-20250929`
* **Gemma Lineage:** `gemma-4-26b-a4b-it`, `gemma-4-31b-it`
