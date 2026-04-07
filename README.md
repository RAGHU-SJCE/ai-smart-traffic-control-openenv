---
title: AI-Powered Smart Intersection Control System
emoji: 🚦
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
  - reinforcement-learning
  - traffic-control
---

# 🚦 AI-Powered Smart Intersection Control System

An intelligent traffic signal control system built using **Reinforcement Learning + LLM + OpenEnv**, designed to simulate and optimize real-world urban traffic flow.

---

## 🌍 Problem Statement

Urban traffic congestion leads to:
- Increased travel time ⏱️
- Fuel wastage ⛽
- Delayed emergency response 🚑

This project simulates a **smart traffic intersection** where an AI agent dynamically controls signals to:
- Minimize vehicle wait times
- Maximize traffic throughput
- Prioritize emergency vehicles

---

## 🧠 Approach

We model the intersection as a **Reinforcement Learning (RL) environment**:

### 🔹 State (Observation)
- Vehicle queues: North, South, East, West
- Wait times for each lane
- Emergency vehicle presence

### 🔹 Action
- Signal direction: `NS` or `EW`
- Signal duration: 5–60 seconds

### 🔹 Reward Function
- ✅ Reward for clearing vehicles
- 🚨 Bonus for handling emergency vehicles
- ❌ Penalty for long waiting times
- ❌ Penalty for traffic imbalance
- ❌ Penalty for repeating same direction continuously

---

## 🤖 AI Control System

The system uses a **hybrid intelligence approach**:

- 🧠 LLM-based reasoning (via HuggingFace router)
- ⚙️ Rule-based optimization for stability

This ensures:
- Smart decisions
- Consistent performance
- Safe traffic control behavior

---

## 🎮 Features

### 🚦 Interactive Simulation UI (Gradio)
- Real-time traffic visualization
- Animated moving vehicles 🚗
- Traffic signals (🟢 / 🔴)
- Emergency alerts 🚨
- Manual + Auto AI control

---

### 🤖 Auto AI Simulation
- Fully autonomous traffic management
- Dynamic decision-making at each step
- Continuous environment interaction

---

### 📊 Performance Monitoring
- Step-by-step reward tracking
- Traffic flow graph
- Final evaluation metrics

---

## 🏁 Final Output Example

[END] 🚦 AI-Powered Smart Intersection Control System
success=false
steps=20
score=0.185

rewards=[0.42, 0.44, 0.13, 0.07, 0.09, 0.13, 0.08, 0.34, ...]


---

## 📊 Evaluation Criteria

The system performance is measured using a normalized score:

| Score Range | Interpretation |
|------------|---------------|
| 0.0 – 0.3 | Poor traffic management |
| 0.3 – 0.5 | Moderate optimization |
| 0.5 – 0.8 | Good traffic balance |
| 0.8 – 1.0 | Optimal performance |

### 🔍 Current Performance
- Achieved Score: **~0.15 – 0.20**
- Indicates moderate optimization with scope for improvement

---

## 🏗️ Project Structure

RL_DEMO/
├── models.py # RL environment logic
├── inference.py # AI agent + evaluation loop
├── gradio_app.py # Interactive dashboard UI
├── server/ # OpenEnv FastAPI backend
├── openenv.yaml # Environment config
├── Dockerfile # Deployment setup


---

## 🚀 How to Run

### 1️⃣ Setup Environment

```bash
uv venv
.venv\Scripts\activate
uv pip install openenv openai gradio matplotlib

2️⃣ Run AI Simulation
uv run inference.py

3️⃣ Launch UI Dashboard
uv run gradio_app.py