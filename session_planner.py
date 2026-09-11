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


def analyze_session(model_hash, latency, flops, fee, confidential):
    compute_scale = classify_compute(flops)
    latency_sensitivity = classify_latency(latency)

    fee_per_billion = fee / (flops / 1_000_000_000)

    if confidential:
        execution = (
            "Confidential execution requested; "
            "the selected miner must support the required confidential tier."
        )
    else:
        execution = "Standard execution is suitable based on the request flags."

    if compute_scale in ("High", "Very High") and latency_sensitivity == "High":
        profile = "Demanding request"
        risk = "High"
    elif compute_scale in ("High", "Very High") or latency_sensitivity == "High":
        profile = "Resource-sensitive request"
        risk = "Medium"
    else:
        profile = "Moderate request"
        risk = "Low"

    print("\n=== FLOP Session Planner ===")
    print(f"Model hash: {model_hash}")
    print(f"Compute scale: {compute_scale}")
    print(f"Latency sensitivity: {latency_sensitivity}")
    print(f"FLOPs: {flops:,.0f}")
    print(f"Fee: {fee:.6f} FLOP")
    print(f"Fee per billion FLOPs: {fee_per_billion:.8f} FLOP")
    print(f"Confidentiality: {'Required' if confidential else 'Not required'}")
    print(f"Request profile: {profile}")
    print(f"Risk level: {risk}")
    print(f"Execution recommendation: {execution}")

    print("\nNext actions:")
    print("1. Verify the model hash before submission.")
    print("2. Benchmark a representative workload.")
    print("3. Compare the request against available miner capabilities.")
    print("4. Confirm that the latency target is realistic.")
    if confidential:
        print("5. Confirm confidential execution support before sending the request.")

    print("\nNote:")
    print(
        "This planner is a heuristic decision aid. "
        "It does not measure live miner capacity, live market clearing, "
        "or guarantee request acceptance."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Plan and assess a FLOP inference session."
    )

    parser.add_argument("--model-hash", required=True)
    parser.add_argument("--latency", type=float, required=True)
    parser.add_argument("--flops", type=float, required=True)
    parser.add_argument("--fee", type=float, required=True)
    parser.add_argument("--confidential", action="store_true")

    args = parser.parse_args()

    analyze_session(
        args.model_hash,
        args.latency,
        args.flops,
        args.fee,
        args.confidential,
    )


if __name__ == "__main__":
    main()