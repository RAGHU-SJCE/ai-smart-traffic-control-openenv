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
- Increased travel time
- Fuel wastage
- Delayed emergency response 🚑

This project simulates a **smart traffic intersection** where an AI agent dynamically controls signals to:
- Minimize wait times
- Maximize throughput
- Prioritize emergency vehicles

---

## 🧠 Approach

We model the intersection as a **reinforcement learning environment**:

### 🔹 State (Observation)
- Vehicle queues (N, S, E, W)
- Wait times per lane
- Emergency vehicle presence

### 🔹 Action
- Select signal direction: `NS` or `EW`
- Set signal duration (5–60 seconds)

### 🔹 Reward Function
- ✅ Reward for clearing vehicles
- 🚨 Bonus for handling emergencies
- ❌ Penalty for long wait times
- ❌ Penalty for traffic imbalance

---

## 🤖 AI Control System

The system uses a **hybrid approach**:

- LLM-based reasoning (via HuggingFace router)
- Rule-based optimization for stability

This ensures:
- Intelligent decisions
- Safe and consistent behavior

---

## 🎮 Features

### 🚦 Interactive Simulation UI (Gradio)
- Real-time traffic visualization
- Animated vehicle movement 🚗
- Signal indicators (🟢 / 🔴)
- Emergency alerts 🚨
- Manual + Auto AI control

---

### 🤖 Auto AI Simulation
- Fully autonomous traffic control
- Dynamic decision-making
- Continuous environment interaction

---

### 📊 Performance Monitoring
- Step-by-step rewards
- Traffic trend graph
- Final evaluation score

---

## 🏁 Final Output Example
