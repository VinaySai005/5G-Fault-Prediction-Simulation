# AI-Powered Fault Prediction in 5G Testbed 📡

A proactive network maintenance system that uses Machine Learning and Prometheus to predict 5G cell tower faults in real-time.

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run (Step-by-Step)](#how-to-run-step-by-step)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)

## 🧐 Overview
This project moves beyond reactive monitoring by implementing a predictive pipeline. It simulates a 5G network, collects live metrics using **Prometheus**, analyzes them using a **Random Forest Classifier**, and visualizes the health status on a **Dash** dashboard.

## 🏗 Architecture
The system consists of 5 independent components running continuously:
1.  **5g_exporter.py**: Generates synthetic metrics (Latency, Throughput, Signal Strength) and exposes them on Port 8000.
2.  **Prometheus Server**: Scrapes Port 8000 every 15s and stores data.
3.  **fault_predictor_prometheus.py**: Queries Prometheus, runs the ML model, and logs predictions.
4.  **alert_manager.py**: Monitors predictions and serves alerts via a REST API.
5.  **visualize_dashboard.py**: A web-based UI for operators to view live trends.

## ⚙️ Prerequisites
* **OS:** Ubuntu (20.04 or later recommended)
* **Python:** 3.8+
* **Prometheus:** v2.51.1 (Binary installed locally)

## 📦 Installation

### 1. Clone/Setup Project Directory
```bash
mkdir -p ~/ai_fault_prediction_g
cd ~/ai_fault_prediction_g
