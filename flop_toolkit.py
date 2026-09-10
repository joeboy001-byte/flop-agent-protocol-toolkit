#!/usr/bin/env python3

"""
FLOP Agent & Protocol Toolkit

A single command-line entry point for:

1. Compute Request Analysis
2. Yellow Paper Review Analysis

This is an independent developer/research tool.
It does not submit FLOP transactions, choose miners,
perform formal proofs, or provide security verdicts.
"""

import argparse
import sys

from compute_analyzer import ComputeRequest, analyze_request, print_report
from review_analyzer import ReviewItem, analyze, print_report as print_review_report


def build_parser():
    parser = argparse.ArgumentParser(
        description="FLOP Agent & Protocol Toolkit"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    compute = subparsers.add_parser(
        "compute",
        help="Analyze a FLOP inference session request"
    )

    compute.add_argument(
        "--model-hash",
        required=True,
        help="Model-weight hash"
    )

    compute.add_argument(
        "--latency",
        required=True,
        type=float,
        help="Maximum latency in seconds"
    )

    compute.add_argument(
        "--flops",
        required=True,
        type=float,
        help="Compute required in FLOPs"
    )

    compute.add_argument(
        "--fee",
        required=True,
        type=float,
        help="Session fee in FLOP"
    )

    compute.add_argument(
        "--confidential",
        action="store_true",
        help="Request confidential execution"
    )

    review = subparsers.add_parser(
        "review",
        help="Analyze a FLOP Yellow Paper review item"
    )

    review.add_argument(
        "--section",
        required=True,
        help="Yellow Paper section or review area"
    )

    review.add_argument(
        "--requirement",
        required=True,
        help="Requirement or claim being reviewed"
    )

    review.add_argument(
        "--evidence",
        required=True,
        choices=[
            "artifact",
            "conditional",
            "empirical",
            "unavailable",
        ],
        help="Evidence category"
    )

    review.add_argument(
        "--implementation",
        required=True,
        choices=[
            "implemented",
            "partial",
            "designed-not-wired",
        ],
        help="Implementation status"
    )

    review.add_argument(
        "--assumption",
        default="",
        help="Key assumption behind the claim"
    )

    review.add_argument(
        "--question",
        required=True,
        help="Question a reviewer should investigate"
    )

    return parser


def run_compute(args):
    request = ComputeRequest(
        model_hash=args.model_hash,
        latency_seconds=args.latency,
        flops=args.flops,
        confidential=args.confidential,
        fee_flop=args.fee,
    )

    analysis = analyze_request(request)
    print_report(request, analysis)


def run_review(args):
    item = ReviewItem(
        section=args.section,
        requirement=args.requirement,
        evidence_type=args.evidence,
        implementation_status=args.implementation,
        assumption=args.assumption,
        reviewer_question=args.question,
    )

    assessment = analyze(item)
    print_review_report(item, assessment)


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "compute":
            run_compute(args)

        elif args.command == "review":
            run_review(args)

        else:
            parser.print_help()
            return 1

    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())