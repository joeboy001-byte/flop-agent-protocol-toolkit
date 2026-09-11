# FLOP Agent & Protocol Toolkit

An independent open-source toolkit for analyzing FLOP inference requests and structuring protocol reviews.

The project combines practical request analysis with a structured review workflow for developers and contributors exploring FLOP-style compute and protocol concepts.

## What it does

The toolkit currently provides three commands:

### 1. Compute Analyzer

Analyzes an inference request using:

- Model hash
- Required FLOPs
- Maximum latency
- FLOP fee
- Confidential execution requirement

It produces a simple assessment of:

- Compute scale
- Latency sensitivity
- Fee per billion FLOPs
- Request profile
- Risk level
- Execution recommendation

### 2. Protocol Review Analyzer

Helps structure reviews of protocol requirements.

It records:

- Protocol section
- Requirement
- Evidence type
- Implementation status
- Assumptions
- Review question

The output is intended to help contributors identify areas that require stronger evidence, testing, or implementation work.

### 3. Session Planner

Combines request-level compute analysis into a higher-level session planning workflow.

It provides:

- Request classification
- Compute and latency assessment
- Fee efficiency
- Confidentiality handling
- Risk assessment
- Recommended next actions

## Project structure

```text
flop-agent-protocol-toolkit/
├── compute_analyzer.py
├── review_analyzer.py
├── session_planner.py
├── flop_toolkit.py
├── architecture.png
├── contribution-proof.json
├── README.md
├── LICENSE
└── .gitignore
Requirements
Python 3
No external Python packages are required for the toolkit itself.
Usage

The recommended entry point is flop_toolkit.py.

View available commands
python flop_toolkit.py --help
Compute analysis
python flop_toolkit.py compute --model-hash example-model-abc123 --latency 2 --flops 12500000000000 --fee 0.08

For confidential execution:

python flop_toolkit.py compute --model-hash example-model-abc123 --latency 2 --flops 12500000000000 --fee 0.08 --confidential
Protocol review
python flop_toolkit.py review --section "Effective-FLOP metering" --requirement "The protocol should correctly meter useful inference work." --evidence conditional --implementation partial --assumption "stated metering assumptions hold under target workload" --question "What tests demonstrate metering accuracy under different workloads and hardware?"
Session planning
python flop_toolkit.py session --model-hash example-model-abc123 --latency 2 --flops 12500000000000 --fee 0.08

For confidential execution:

python flop_toolkit.py session --model-hash example-model-abc123 --latency 2 --flops 12500000000000 --fee 0.08 --confidential
How the toolkit can be used

A typical workflow is:

Inference request
       |
       v
Compute Analyzer
       |
       v
Session Planner
       |
       v
Miner / execution considerations
       |
       v
Protocol Review

The toolkit is designed as a lightweight analysis and contribution aid rather than a replacement for production infrastructure, benchmarking systems, or formal protocol verification.

Design goals
Keep analysis transparent and understandable.
Use explicit inputs rather than hidden assumptions.
Separate heuristic analysis from verified facts.
Help contributors structure protocol questions.
Provide useful tooling that can be extended as FLOP-related infrastructure develops.
Limitations

This project does not provide:

Live miner capacity measurements
Live market clearing
Guaranteed request acceptance
Production inference execution
Formal protocol verification
Security auditing
Official FLOP network data

The compute and session outputs are heuristic decision aids.

The protocol review output is a review aid and should not be treated as an official audit, formal proof, or security verdict.

Contribution

Contributions, suggestions, test cases, and improvements are welcome.

Useful contributions include:

Better analysis heuristics
Additional validation
Representative workload benchmarks
Protocol review templates
Documentation improvements
New analysis modules
Status

The toolkit is an independent open-source project under active development.

Current modules:

Compute Analyzer
Protocol Review Analyzer
Session Planner

Future development may add additional analysis and benchmarking capabilities as the project evolves.