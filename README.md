---
title: AI-Powered Smart Intersection Control System
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

An intelligent traffic signal control system built using **Reinforcement Learning, OpenEnv, and LLM-based decision making** to simulate and optimize real-world urban traffic flow.

---

## 🧠 Motivation

Urban traffic congestion causes:

- 🚗 Increased travel time  
- ⛽ Fuel wastage  
- 🚑 Delayed emergency response  

This project models a **real-world traffic intersection**, where an AI agent dynamically controls signals to:

- Minimize vehicle queues  
- Reduce waiting time  
- Balance traffic across directions  
- Prioritize emergency scenarios  

---

## 🌍 Real-World Utility

This environment simulates **adaptive traffic signal systems** used in:

- Smart cities  
- Intelligent Transportation Systems (ITS)  
- Autonomous traffic management  

It can be used to **train and evaluate RL agents** for real-world deployment.

---

## ⚙️ Environment Design

### 📊 Observation Space

The agent observes:

- `north_queue`, `south_queue`, `east_queue`, `west_queue`
- `emergency_waiting` (boolean)
- `total_queue`

---

### 🎮 Action Space

Discrete actions:

- `0` → North-South Green  
- `1` → East-West Green  

---

### 🔁 Episode

- Fixed horizon: **50 steps**
- Each step simulates traffic flow and signal control

---

## 🏆 Reward Function (0.0 – 1.0)

The reward is a **multi-objective signal**:

- 🚗 Congestion reduction  
- ⚖️ Fairness (avoid starvation)  
- 🔄 Traffic balance  
- 🚑 Emergency handling bonus  

This ensures:

- Continuous feedback  
- No sparse rewards  
- Realistic optimization goals  

---

## 📈 Grader (Evaluation Logic)

Each step produces a score ∈ **[0, 1]**

Final evaluation considers:

- Congestion level  
- Maximum waiting time  
- Directional balance  

```text
Score = (congestion + fairness + balance) / 3

✅ Success Criteria
success = score > 0.7
🧪 Tasks (Difficulty Levels)
🟢 Easy
Low traffic arrival
No emergency vehicles
🟡 Medium
Moderate traffic
Occasional emergencies
🔴 Hard
High congestion
Continuous emergency pressure
🤖 Baseline Agent

The baseline uses:

LLM-based reasoning (via Hugging Face router)
Rule-based fallback policy

It dynamically selects signals based on:

Higher traffic density → prioritize that direction
📊 Example Output
[START]

[STEP] task=easy
...
[STEP] task=easy total_reward=16.57

[STEP] task=medium
...
[STEP] task=medium total_reward=16.26

[STEP] task=hard
...
[STEP] task=hard total_reward=11.98

[END]
🎮 Interactive UI

A custom simulation interface is available at:

/ui
Features:
🚗 Animated traffic flow
🚦 Real-time signal switching
🎮 Step / Reset / State controls
🤖 Autoplay AI simulation
🏗️ Project Structure
RL_DEMO/
├── models.py
├── inference.py
├── gradio_app.py
├── openenv.yaml
├── Dockerfile
├── pyproject.toml
└── server/
    └── app.py
🚀 Run Locally
uv venv
.venv\Scripts\activate
uv pip install -e .
uv run inference.py
🐳 Run with Docker
docker build -t traffic-env .
docker run -p 8000:8000 traffic-env
🌐 Access
OpenEnv UI → /web
Custom UI → /ui
📦 Deployment

This project is deployed as a Hugging Face Space (Docker runtime) and complies with:

OpenEnv specification
Containerized execution
Automated validation pipeline
🏆 Highlights
✅ Real-world traffic simulation
✅ Multi-objective reward design
✅ Deterministic grader (0–1 range)
✅ 3 difficulty levels
✅ LLM + rule-based agent
✅ Interactive animated UI
🔮 Future Improvements
Multi-intersection coordination
Reinforcement learning training integration
Real traffic dataset calibration
Vehicle-type prioritization

🏁 Conclusion

This project demonstrates how AI can optimize real-world infrastructure systems through simulation, reinforcement learning, and intelligent decision-making.