#!/usr/bin/env python3

"""
FLOP Agent & Protocol Toolkit
Part 2: Yellow Paper Review Analyzer

This tool organizes a protocol review item using the evidence
categories and implementation-status concepts described in the
FLOP Yellow Paper research draft.

It does not perform a security audit or claim to prove a protocol
property. It produces a structured reviewer-oriented assessment.
"""

from dataclasses import dataclass
import argparse


@dataclass
class ReviewItem:
    section: str
    requirement: str
    evidence_type: str
    implementation_status: str
    assumption: str
    reviewer_question: str


@dataclass
class ReviewAssessment:
    evidence_interpretation: str
    implementation_interpretation: str
    risk_level: str
    review_priority: str
    notes: list[str]


EVIDENCE_TYPES = {
    "artifact": (
        "An artifact exists, but that alone does not establish that "
        "the assumptions hold or that the implementation enforces the claim."
    ),
    "conditional": (
        "The result is conditional on the stated assumptions. "
        "Those assumptions should be checked separately."
    ),
    "empirical": (
        "Recorded experimental evidence supports the claim for its "
        "specified workload, hardware, model, precision, sample, "
        "and uncertainty."
    ),
    "unavailable": (
        "The cited evidence is not publicly available in the material "
        "being reviewed, so the claim should be treated as unverified here."
    ),
}

IMPLEMENTATION_STATUSES = {
    "implemented": "The mechanism is reported as implemented.",
    "partial": "The mechanism is reported as partially implemented.",
    "designed-not-wired": (
        "The mechanism is designed but not yet wired into the implementation."
    ),
}


def normalize(value: str) -> str:
    return value.strip().lower()


def assess_risk(item: ReviewItem) -> tuple[str, str]:
    evidence = normalize(item.evidence_type)
    implementation = normalize(item.implementation_status)

    points = 0

    if evidence == "unavailable":
        points += 3
    elif evidence == "conditional":
        points += 2
    elif evidence == "artifact":
        points += 1

    if implementation == "designed-not-wired":
        points += 3
    elif implementation == "partial":
        points += 2

    if not item.assumption.strip():
        points += 1

    if points >= 5:
        return "High", "Immediate review"
    if points >= 3:
        return "Medium", "Focused review"

    return "Low", "Routine review"


def analyze(item: ReviewItem) -> ReviewAssessment:
    evidence = normalize(item.evidence_type)
    implementation = normalize(item.implementation_status)

    evidence_interpretation = EVIDENCE_TYPES.get(
        evidence,
        "Unknown evidence category. Review the source classification manually.",
    )

    implementation_interpretation = IMPLEMENTATION_STATUSES.get(
        implementation,
        "Unknown implementation status. Review the source classification manually.",
    )

    risk_level, review_priority = assess_risk(item)

    notes = []

    if evidence == "conditional":
        notes.append(
            "Check whether the assumptions required by the conditional result "
            "are actually discharged."
        )

    if evidence == "artifact":
        notes.append(
            "Existence of an artifact is not the same as proof of correctness."
        )

    if evidence == "empirical":
        notes.append(
            "Check whether the reported workload, hardware, model, precision, "
            "sample, and uncertainty match the claim being reviewed."
        )

    if evidence == "unavailable":
        notes.append(
            "Treat the claim as unverified from the public material unless "
            "the source provides another public evidence path."
        )

    if implementation in {"partial", "designed-not-wired"}:
        notes.append(
            "Implementation status does not by itself establish formal proof "
            "coverage or empirical validation."
        )

    if item.assumption.strip():
        notes.append(
            "Review the stated assumption directly before drawing a conclusion."
        )

    return ReviewAssessment(
        evidence_interpretation=evidence_interpretation,
        implementation_interpretation=implementation_interpretation,
        risk_level=risk_level,
        review_priority=review_priority,
        notes=notes,
    )


def print_report(item: ReviewItem, assessment: ReviewAssessment) -> None:
    print()
    print("=" * 68)
    print("FLOP YELLOW PAPER REVIEW ANALYZER")
    print("=" * 68)

    print()
    print("REVIEW ITEM")
    print("-" * 68)
    print(f"Section:                 {item.section}")
    print(f"Requirement / claim:     {item.requirement}")
    print(f"Evidence type:           {item.evidence_type}")
    print(f"Implementation status:   {item.implementation_status}")
    print(f"Assumption:              {item.assumption}")
    print(f"Reviewer question:       {item.reviewer_question}")

    print()
    print("INTERPRETATION")
    print("-" * 68)
    print(f"Evidence:                {assessment.evidence_interpretation}")
    print(
        "Implementation:          "
        f"{assessment.implementation_interpretation}"
    )

    print()
    print("REVIEW PRIORITY")
    print("-" * 68)
    print(f"Risk indicator:          {assessment.risk_level}")
    print(f"Priority:                {assessment.review_priority}")

    print()
    print("REVIEW NOTES")
    print("-" * 68)

    for note in assessment.notes:
        print(f"- {note}")

    print()
    print("IMPORTANT")
    print("-" * 68)
    print(
        "This tool is a review aid, not an official FLOP audit, "
        "formal proof system, or security verdict."
    )
    print()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze a FLOP Yellow Paper review item."
    )

    parser.add_argument(
        "--section",
        required=True,
        help="Yellow Paper section or review area"
    )

    parser.add_argument(
        "--requirement",
        required=True,
        help="Requirement or claim being reviewed"
    )

    parser.add_argument(
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

    parser.add_argument(
        "--implementation",
        required=True,
        choices=[
            "implemented",
            "partial",
            "designed-not-wired",
        ],
        help="Implementation status"
    )

    parser.add_argument(
        "--assumption",
        default="",
        help="Key assumption behind the claim"
    )

    parser.add_argument(
        "--question",
        required=True,
        help="Question a reviewer should investigate"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    item = ReviewItem(
        section=args.section,
        requirement=args.requirement,
        evidence_type=args.evidence,
        implementation_status=args.implementation,
        assumption=args.assumption,
        reviewer_question=args.question,
    )

    assessment = analyze(item)
    print_report(item, assessment)


if __name__ == "__main__":
    main()