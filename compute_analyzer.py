#!/usr/bin/env python3

"""
FLOP Agent & Protocol Toolkit
Part 1: Compute Request Analyzer

Analyzes the basic parameters of a FLOP inference session request.

This is an educational/developer tool. It does not submit transactions,
choose miners, or estimate a live FLOP market price.
"""

from dataclasses import dataclass
import argparse


@dataclass
class ComputeRequest:
    model_hash: str
    latency_seconds: float
    flops: float
    confidential: bool
    fee_flop: float


@dataclass
class Analysis:
    compute_scale: str
    latency_sensitivity: str
    fee_per_billion_flops: float
    fee_efficiency: str
    request_risk: str
    notes: list[str]


def classify_compute(flops: float) -> str:
    if flops < 1_000_000_000:
        return "Low"
    if flops < 1_000_000_000_000:
        return "Medium"
    if flops < 1_000_000_000_000_000:
        return "High"
    return "Very high"


def classify_latency(seconds: float) -> str:
    if seconds <= 1:
        return "Very high"
    if seconds <= 5:
        return "High"
    if seconds <= 30:
        return "Medium"
    return "Low"


def analyze_request(request: ComputeRequest) -> Analysis:
    compute_scale = classify_compute(request.flops)
    latency_sensitivity = classify_latency(request.latency_seconds)

    if request.flops > 0:
        fee_per_billion_flops = (
            request.fee_flop / request.flops
        ) * 1_000_000_000
    else:
        fee_per_billion_flops = 0.0

    notes = []

    if request.flops <= 0:
        notes.append("Compute amount must be greater than zero.")

    if request.latency_seconds <= 0:
        notes.append("Latency target must be greater than zero.")

    if request.fee_flop < 0:
        notes.append("FLOP fee cannot be negative.")

    if not request.model_hash:
        notes.append("A model-weight hash should be supplied.")

    if request.confidential:
        notes.append(
            "Confidential execution was requested; hardware capability "
            "and execution environment should be checked."
        )
    else:
        notes.append(
            "Standard execution was requested; confidential computing "
            "is not required by this request."
        )

    if latency_sensitivity == "Very high":
        notes.append(
            "A very tight latency target may reduce the set of suitable "
            "miners."
        )

    if compute_scale in {"High", "Very high"}:
        notes.append(
            "Large compute demand may reduce the number of miners capable "
            "of accepting the session."
        )

    if fee_per_billion_flops >= 1:
        fee_efficiency = "Higher fee per billion FLOPs"
    elif fee_per_billion_flops > 0:
        fee_efficiency = "Lower fee per billion FLOPs"
    else:
        fee_efficiency = "Unavailable"

    risk_points = 0

    if latency_sensitivity == "Very high":
        risk_points += 2
    elif latency_sensitivity == "High":
        risk_points += 1

    if compute_scale == "Very high":
        risk_points += 2
    elif compute_scale == "High":
        risk_points += 1

    if request.confidential:
        risk_points += 1

    if request.fee_flop <= 0:
        risk_points += 2

    if risk_points >= 4:
        request_risk = "High"
    elif risk_points >= 2:
        request_risk = "Medium"
    else:
        request_risk = "Low"

    return Analysis(
        compute_scale=compute_scale,
        latency_sensitivity=latency_sensitivity,
        fee_per_billion_flops=fee_per_billion_flops,
        fee_efficiency=fee_efficiency,
        request_risk=request_risk,
        notes=notes,
    )


def print_report(request: ComputeRequest, analysis: Analysis) -> None:
    print()
    print("=" * 64)
    print("FLOP COMPUTE REQUEST ANALYZER")
    print("=" * 64)

    print()
    print("REQUEST")
    print("-" * 64)
    print(f"Model-weight hash: {request.model_hash}")
    print(f"Maximum latency:   {request.latency_seconds:g} seconds")
    print(f"Compute required:  {request.flops:,.0f} FLOPs")
    print(
        f"Confidentiality:   "
        f"{'Required' if request.confidential else 'Not required'}"
    )
    print(f"FLOP fee:          {request.fee_flop:g} FLOP")

    print()
    print("ANALYSIS")
    print("-" * 64)
    print(f"Compute scale:             {analysis.compute_scale}")
    print(f"Latency sensitivity:       {analysis.latency_sensitivity}")
    print(
        "Fee per billion FLOPs:     "
        f"{analysis.fee_per_billion_flops:.8f} FLOP"
    )
    print(f"Fee efficiency indicator:  {analysis.fee_efficiency}")
    print(f"Request risk indicator:    {analysis.request_risk}")

    print()
    print("NOTES")
    print("-" * 64)

    for note in analysis.notes:
        print(f"- {note}")

    print()
    print("IMPORTANT")
    print("-" * 64)
    print(
        "This analyzer does not estimate a live market-clearing price "
        "or guarantee that a miner will accept the request."
    )
    print(
        "Its classifications are heuristic indicators for developers "
        "and agents."
    )
    print()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze a FLOP inference session request."
    )

    parser.add_argument(
        "--model-hash",
        required=True,
        help="Model-weight hash"
    )

    parser.add_argument(
        "--latency",
        required=True,
        type=float,
        help="Maximum latency in seconds"
    )

    parser.add_argument(
        "--flops",
        required=True,
        type=float,
        help="Compute required in FLOPs"
    )

    parser.add_argument(
        "--fee",
        required=True,
        type=float,
        help="Session fee in FLOP"
    )

    parser.add_argument(
        "--confidential",
        action="store_true",
        help="Request confidential execution"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    request = ComputeRequest(
        model_hash=args.model_hash,
        latency_seconds=args.latency,
        flops=args.flops,
        confidential=args.confidential,
        fee_flop=args.fee,
    )

    analysis = analyze_request(request)
    print_report(request, analysis)


if __name__ == "__main__":
    main()