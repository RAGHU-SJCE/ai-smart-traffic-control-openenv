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

# AI-Powered Smart Intersection Control System

An intelligent traffic signal control system built using Reinforcement Learning, OpenEnv, and LLM-based decision making to simulate and optimize real-world urban traffic flow.

---

## Motivation

Urban traffic congestion causes:
- Increased travel time
- Fuel wastage
- Delayed emergency response

This project models a real-world traffic intersection where an AI agent dynamically controls signals to:
- Minimize vehicle queues
- Reduce waiting time
- Balance traffic across directions
- Prioritize emergency scenarios

---

## Real-World Utility

This environment simulates adaptive traffic signal systems used in:
- Smart cities
- Intelligent Transportation Systems
- Autonomous traffic management

---

## Environment Design

### Observation Space
- north_queue, south_queue, east_queue, west_queue
- emergency_waiting
- total_queue

### Action Space
- 0 → North-South Green
- 1 → East-West Green

### Episode
- Fixed horizon: 50 steps

---

## Reward Function (0.0 – 1.0)

Multi-objective reward:
- Congestion reduction
- Fairness
- Traffic balance
- Emergency handling

---

## Grader

Score calculation:

score = (congestion + fairness + balance) / 3


Success condition:


success = score > 0.7


---

## Tasks

### Easy
- Low traffic
- No emergencies

### Medium
- Moderate traffic
- Occasional emergencies

### Hard
- Heavy congestion
- Frequent emergencies

---

## Baseline Agent

Uses:
- LLM via Hugging Face router
- Rule-based fallback

Decision rule:
- Higher traffic direction gets priority

---

## Example Output

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


---

## UI

Available at:

/ui


Features:
- Animated traffic
- Signal control
- Step / Reset / State buttons
- Autoplay

---

## Project Structure


RL_DEMO/
├── models.py
├── inference.py
├── client.py
├── gradio_app.py
├── openenv.yaml
├── Dockerfile
├── pyproject.toml
└── server/
└── app.py


---

## Run Locally


uv venv
.venv\Scripts\activate
uv pip install -e .
uv run inference.py


---

## Docker


docker build -t traffic-env .
docker run -p 8000:8000 traffic-env


---

## Access

- /web → OpenEnv UI
- /ui → Custom UI

---

## Conclusion

This project demonstrates how AI can optimize real-world infrastructure systems using reinforcement learning and simulation.