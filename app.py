import streamlit as st

from flop_toolkit import analyze_compute
from review_analyzer import ReviewItem, analyze as analyze_review


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="FLOP Agent & Protocol Toolkit",
    page_icon="⚡",
    layout="wide",
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem 0 1rem 0;
    }

    .hero h1 {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.1rem;
        color: #5c6670;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    .result-box {
        padding: 1.25rem;
        border-radius: 12px;
        background: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .small-label {
        color: #5c6670;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }

    .small-value {
        font-size: 1.15rem;
        font-weight: 600;
    }

    .footer {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>⚡ FLOP Agent & Protocol Toolkit</h1>
        <p>
            Analyze FLOP inference requests and structure protocol reviews
            with lightweight decision-support tools.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# --------------------------------------------------
# Main workflows
# --------------------------------------------------

compute_tab, review_tab = st.tabs(
    ["⚡ Compute Analysis", "🔎 Protocol Review"]
)


# ==================================================
# COMPUTE ANALYSIS
# ==================================================

with compute_tab:

    st.markdown(
        '<div class="section-title">Inference Request</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        model_hash = st.text_input(
            "Model-weight hash",
            placeholder="Enter model hash",
            key="compute_model_hash",
        )

        flops = st.number_input(
            "Compute required (FLOPs)",
            min_value=1.0,
            value=12_500_000_000_000.0,
            step=1_000_000_000.0,
            format="%.0f",
            key="compute_flops",
        )

    with right:
        latency = st.number_input(
            "Maximum latency (seconds)",
            min_value=0.01,
            value=5.0,
            step=0.5,
            key="compute_latency",
        )

        fee = st.number_input(
            "Session fee (FLOP)",
            min_value=0.0,
            value=0.08,
            step=0.01,
            key="compute_fee",
        )

    confidential = st.checkbox(
        "Confidential execution required",
        key="compute_confidential",
    )

    st.write("")

    analyze_button = st.button(
        "⚡ Analyze Request",
        type="primary",
        use_container_width=True,
        key="analyze_compute_button",
    )

    if analyze_button:

        if not model_hash.strip():
            st.warning("Please enter a model-weight hash.")

        else:

            result = analyze_compute(
                flops=flops,
                fee=fee,
                latency=latency,
                confidential=confidential,
            )

            st.divider()

            st.markdown(
                '<div class="section-title">Analysis</div>',
                unsafe_allow_html=True,
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Compute scale",
                    result["compute_scale"],
                )

            with col2:
                st.metric(
                    "Latency sensitivity",
                    result["latency_sensitivity"],
                )

            with col3:
                st.metric(
                    "Risk level",
                    result["risk"],
                )

            with col4:
                st.metric(
                    "Fee / billion FLOPs",
                    f"{result['fee_efficiency']:.8f}",
                )

            st.write("")

            st.markdown(
                '<div class="section-title">Execution Recommendation</div>',
                unsafe_allow_html=True,
            )

            st.info(result["execution"])

            st.markdown(
                '<div class="section-title">Request Profile</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="small-label">Profile</div>
                    <div class="small-value">{result["profile"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-title">Request Summary</div>',
                unsafe_allow_html=True,
            )

            summary_left, summary_right = st.columns(2)

            with summary_left:
                st.write(f"**Model hash:** `{model_hash}`")
                st.write(f"**Compute:** {flops:,.0f} FLOPs")
                st.write(f"**Maximum latency:** {latency:g} seconds")

            with summary_right:
                st.write(f"**Session fee:** {fee:g} FLOP")
                st.write(
                    "**Confidentiality:** "
                    + ("Required" if confidential else "Not required")
                )

            st.divider()

            st.markdown(
                """
                <div class="footer">
                    This toolkit provides heuristic decision support.
                    It does not measure live miner capacity, live market
                    clearing, or guarantee request acceptance.
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==================================================
# PROTOCOL REVIEW
# ==================================================

with review_tab:

    st.markdown(
        '<div class="section-title">Protocol Review Item</div>',
        unsafe_allow_html=True,
    )

    section = st.text_input(
        "Review section",
        placeholder="Example: Effective-FLOP metering",
    )

    requirement = st.text_area(
        "Requirement or claim",
        placeholder="What should the protocol or implementation demonstrate?",
    )

    left, right = st.columns(2)

    with left:

        evidence = st.selectbox(
            "Evidence type",
            [
                "artifact",
                "conditional",
                "empirical",
                "unavailable",
            ],
        )

    with right:

        implementation = st.selectbox(
            "Implementation status",
            [
                "implemented",
                "partial",
                "designed-not-wired",
            ],
        )

    assumption = st.text_area(
        "Key assumption",
        placeholder="What assumption must hold for the claim?",
    )

    question = st.text_area(
        "Reviewer question",
        placeholder="What should a reviewer investigate?",
    )

    st.write("")

    review_button = st.button(
        "🔎 Analyze Review Item",
        type="primary",
        use_container_width=True,
        key="analyze_review_button",
    )

    if review_button:

        if not section.strip():
            st.warning("Please enter a review section.")

        elif not requirement.strip():
            st.warning("Please enter a requirement or claim.")

        elif not question.strip():
            st.warning("Please enter a reviewer question.")

        else:

            item = ReviewItem(
                section=section,
                requirement=requirement,
                evidence_type=evidence,
                implementation_status=implementation,
                assumption=assumption,
                reviewer_question=question,
            )

            result = analyze_review(item)

            st.divider()

            st.markdown(
                '<div class="section-title">Review Assessment</div>',
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Risk level",
                    result.risk_level,
                )

            with col2:
                st.metric(
                    "Review priority",
                    result.review_priority,
                )

            st.markdown(
                '<div class="section-title">Evidence Interpretation</div>',
                unsafe_allow_html=True,
            )

            st.info(result.evidence_interpretation)

            st.markdown(
                '<div class="section-title">Implementation Interpretation</div>',
                unsafe_allow_html=True,
            )

            st.info(result.implementation_interpretation)

            st.markdown(
                '<div class="section-title">Review Notes</div>',
                unsafe_allow_html=True,
            )

            for note in result.notes:
                st.write(f"• {note}")

            st.markdown(
                '<div class="section-title">Review Item Summary</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="small-label">Section</div>
                    <div class="small-value">{section}</div>
                    <br>
                    <div class="small-label">Requirement</div>
                    <div>{requirement}</div>
                    <br>
                    <div class="small-label">Reviewer question</div>
                    <div>{question}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.divider()

            st.markdown(
                """
                <div class="footer">
                    This tool is a review aid, not an official FLOP audit,
                    formal proof system, or security verdict.
                </div>
                """,
                unsafe_allow_html=True,
            )