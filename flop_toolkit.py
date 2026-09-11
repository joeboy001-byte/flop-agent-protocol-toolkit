import argparse


def classify_compute(flops):
    if flops < 1_000_000_000_000:
        return "Low"
    elif flops < 10_000_000_000_000:
        return "Medium"
    elif flops < 100_000_000_000_000:
        return "High"
    return "Very High"


def classify_latency(latency):
    if latency <= 2:
        return "High"
    elif latency <= 10:
        return "Medium"
    return "Low"


def fee_per_billion_flops(flops, fee):
    return fee / (flops / 1_000_000_000)


def analyze_compute(flops, fee, latency, confidential):
    compute_scale = classify_compute(flops)
    latency_sensitivity = classify_latency(latency)
    fee_efficiency = fee_per_billion_flops(flops, fee)

    if compute_scale in ("High", "Very High") and latency_sensitivity == "High":
        profile = "Demanding request"
        risk = "High"
    elif compute_scale in ("High", "Very High") or latency_sensitivity == "High":
        profile = "Resource-sensitive request"
        risk = "Medium"
    else:
        profile = "Moderate request"
        risk = "Low"

    if confidential:
        execution = (
            "Confidential execution requested; "
            "the selected miner must support the required confidential tier."
        )
    else:
        execution = "Standard execution is suitable based on the request flags."

    return {
        "compute_scale": compute_scale,
        "latency_sensitivity": latency_sensitivity,
        "fee_efficiency": fee_efficiency,
        "profile": profile,
        "risk": risk,
        "execution": execution,
    }


def run_compute(args):
    result = analyze_compute(
        args.flops,
        args.fee,
        args.latency,
        args.confidential,
    )

    print("\n=== FLOP Agent & Protocol Toolkit: Compute ===")
    print(f"Model hash: {args.model_hash}")
    print(f"Compute scale: {result['compute_scale']}")
    print(f"Latency sensitivity: {result['latency_sensitivity']}")
    print(f"FLOPs: {args.flops:,.0f}")
    print(f"Fee: {args.fee:.6f} FLOP")
    print(
        f"Fee per billion FLOPs: "
        f"{result['fee_efficiency']:.8f} FLOP"
    )
    print(
        f"Confidentiality: "
        f"{'Required' if args.confidential else 'Not required'}"
    )
    print(f"Request profile: {result['profile']}")
    print(f"Risk level: {result['risk']}")
    print(f"Execution recommendation: {result['execution']}")

    print("\nNote:")
    print(
        "This analysis is heuristic. It does not measure live miner "
        "capacity, live market clearing, or guarantee request acceptance."
    )


def run_review(args):
    print("\n=== FLOP Agent & Protocol Toolkit: Protocol Review ===")
    print(f"Section: {args.section}")
    print(f"Requirement: {args.requirement}")
    print(f"Evidence type: {args.evidence}")
    print(f"Implementation status: {args.implementation}")

    if args.assumption:
        print(f"Assumption: {args.assumption}")

    print(f"Review question: {args.question}")

    if args.evidence == "artifact":
        risk = "Lower evidence uncertainty"
    elif args.evidence == "conditional":
        risk = "Medium evidence uncertainty"
    elif args.evidence == "empirical":
        risk = "Evidence requires validation against the target workload"
    else:
        risk = "High evidence uncertainty"

    print(f"Review assessment: {risk}")

    print("\nNote:")
    print(
        "This is a review aid, not an official audit, formal proof, "
        "or security verdict."
    )


def run_session(args):
    result = analyze_compute(
        args.flops,
        args.fee,
        args.latency,
        args.confidential,
    )

    print("\n=== FLOP Agent & Protocol Toolkit: Session Planner ===")
    print(f"Model hash: {args.model_hash}")
    print(f"Compute scale: {result['compute_scale']}")
    print(f"Latency sensitivity: {result['latency_sensitivity']}")
    print(f"FLOPs: {args.flops:,.0f}")
    print(f"Fee: {args.fee:.6f} FLOP")
    print(
        f"Fee per billion FLOPs: "
        f"{result['fee_efficiency']:.8f} FLOP"
    )
    print(
        f"Confidentiality: "
        f"{'Required' if args.confidential else 'Not required'}"
    )
    print(f"Request profile: {result['profile']}")
    print(f"Risk level: {result['risk']}")
    print(f"Execution recommendation: {result['execution']}")

    print("\nPlanner actions:")
    print("1. Verify the model hash before submission.")
    print("2. Benchmark a representative workload.")
    print("3. Compare the request against miner capabilities.")
    print("4. Confirm that the latency target is realistic.")

    if args.confidential:
        print(
            "5. Confirm confidential execution support before "
            "sending the request."
        )

    print("\nNote:")
    print(
        "The planner is a heuristic decision aid. It does not measure "
        "live miner capacity, live market clearing, or guarantee "
        "request acceptance."
    )


def main():
    parser = argparse.ArgumentParser(
        description="FLOP Agent & Protocol Toolkit"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    compute = subparsers.add_parser(
        "compute",
        help="Analyze a FLOP inference request.",
    )
    compute.add_argument("--model-hash", required=True)
    compute.add_argument("--latency", type=float, required=True)
    compute.add_argument("--flops", type=float, required=True)
    compute.add_argument("--fee", type=float, required=True)
    compute.add_argument("--confidential", action="store_true")
    compute.set_defaults(func=run_compute)

    review = subparsers.add_parser(
        "review",
        help="Review a protocol requirement.",
    )
    review.add_argument("--section", required=True)
    review.add_argument("--requirement", required=True)
    review.add_argument(
        "--evidence",
        choices=[
            "artifact",
            "conditional",
            "empirical",
            "unavailable",
        ],
        required=True,
    )
    review.add_argument(
        "--implementation",
        choices=[
            "implemented",
            "partial",
            "designed-not-wired",
        ],
        required=True,
    )
    review.add_argument("--assumption")
    review.add_argument("--question", required=True)
    review.set_defaults(func=run_review)

    session = subparsers.add_parser(
        "session",
        help="Plan a FLOP inference session.",
    )
    session.add_argument("--model-hash", required=True)
    session.add_argument("--latency", type=float, required=True)
    session.add_argument("--flops", type=float, required=True)
    session.add_argument("--fee", type=float, required=True)
    session.add_argument("--confidential", action="store_true")
    session.set_defaults(func=run_session)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()