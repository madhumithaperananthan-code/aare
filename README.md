---
title: AARE
emoji: 🛡️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# AARE — Autonomous Application Resilience Environment

## Overview
AARE is an OpenEnv reinforcement learning environment where an AI agent learns to defend a simulated web application from common cyber attacks.

An agent interacts with the environment by selecting security mitigations in response to simulated attacks. The objective is to maximize application resilience by correctly blocking attacks.

## Motivation
Modern web applications face constant security threats such as:

- SQL injection
- cross-site scripting
- privilege escalation

Security engineers typically respond by applying mitigations and patches.

AARE simulates this process, enabling AI agents to learn defensive strategies through reinforcement learning.

## Research Value

AARE is designed as a training environment for autonomous cybersecurity agents.

The environment captures several important properties of real-world security operations:

- Sequential attack progression through multi-step attack chains
- Dynamic system risk modeling through a continuous risk score
- Defensive mitigation strategies with different security effects
- Partial reward signals that encourage proactive defense

This makes AARE suitable for evaluating reinforcement learning agents that must maintain the security posture of a system over time.

The environment can serve as a benchmark for research in:

- Autonomous cyber defense agents
- Security policy learning
- Risk-aware reinforcement learning

## Environment Mechanics

Each step follows the loop:
## Environment Interaction

The interaction between the agent and the environment follows this loop:
Agent
│
│ chooses defense action
▼
Environment (AARE)
│
│ generates cyber attack
▼
System State
│
│ update risk score & defenses
▼
Reward Signal
│
└── informs the agent how effective the defense was

Observation → Action → Environment Update → Reward

The environment generates a cyber attack, and the agent must choose an appropriate defense.

## Observation Space

At each step the agent receives an observation describing the current security state of the system.

The observation includes:

- `attack_type` — type of attack currently targeting the system
- `target_component` — system component under attack
- `severity` — severity level of the attack
- `vulnerabilities` — vulnerabilities currently exposed
- `defense_status` — currently active defensive mitigations
- `failed_attack_streak` — number of consecutive blocked attacks
- `risk_score` — continuous measure of system compromise risk (0.0–1.0)

This information allows the agent to reason about the security posture of the application.

---

## Action Space

At each step the agent selects one defensive action:

- `sanitize_queries`
- `enable_input_validation`
- `add_rate_limiting`
- `patch_authentication`
- `secure_file_upload`
- `enable_waf`
- `block_ip`
- `ignore`

Each action represents a mitigation strategy commonly used in real-world web security.

---


### Example Attack

```
sql_injection
```

### Correct Defense

```
sanitize_queries
```

If the correct defense is applied, the attack is blocked and the agent receives a positive reward.

## Attack Types

- SQL Injection  
- Cross-Site Scripting (XSS)  
- Brute Force Login  
- Privilege Escalation  
- Insecure File Upload  
- Rate Limit Bypass  

## Defense Actions

- sanitize_queries  
- enable_input_validation  
- add_rate_limiting  
- patch_authentication  
- secure_file_upload  
- enable_waf  
- block_ip  
- ignore  

## Reward Structure

| Event | Reward |
|------|------|
| Attack blocked | +1.0 |
| Correct mitigation | +0.5 |
| Partial mitigation | +0.2 |
| Incorrect defense | -0.3 |
| Ignored real attack | -1.0 |

The environment supports both successful and failed defense scenarios. Agents that apply incorrect defenses or ignore attacks will accumulate system risk and may trigger system compromise termination.



## Episode Termination

Episodes terminate when:

- Three attacks are successfully blocked consecutively (system stabilized)
- The system risk score exceeds the compromise threshold
- The maximum step limit is reached

## Tasks

### Easy
Defend against repeated SQL injection attacks.

### Medium
Defend against SQL injection and brute force login attempts.

### Hard
Defend against multiple attack types including XSS, privilege escalation, and file upload attacks.

## Running the Baseline Agent

Run the inference script:

```
python inference.py
```

This executes the baseline defense agent and produces structured logs required by the OpenEnv evaluation system.

## Project Structure

```
env/
models/
tasks/
graders/
openenv.yaml
inference.py
Dockerfile
```

## License

This project is provided for research and experimentation with reinforcement learning environments.