import streamlit as st
import requests
import pandas as pd
import re
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"

UPLOAD_URL = f"{API_BASE_URL}/upload/"
ANALYZE_URL = f"{API_BASE_URL}/api/analyze/analyze"

ALLOWED_EXTENSIONS = {".log", ".txt", ".csv"}

st.set_page_config(
    page_title="AI Log Analyzer & RCA",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM UI
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #777;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1.5rem;
        margin-bottom: 0.7rem;
    }

    .severity-critical {
        background: #ffebee;
        padding: 12px 18px;
        border-radius: 10px;
        border-left: 6px solid #d32f2f;
        font-size: 1.15rem;
        font-weight: 700;
    }

    .severity-high {
        background: #fff3e0;
        padding: 12px 18px;
        border-radius: 10px;
        border-left: 6px solid #ef6c00;
        font-size: 1.15rem;
        font-weight: 700;
    }

    .severity-medium {
        background: #fffde7;
        padding: 12px 18px;
        border-radius: 10px;
        border-left: 6px solid #fbc02d;
        font-size: 1.15rem;
        font-weight: 700;
    }

    .severity-low {
        background: #e8f5e9;
        padding: 12px 18px;
        border-radius: 10px;
        border-left: 6px solid #388e3c;
        font-size: 1.15rem;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🔎 AI Log Analyzer & RCA Tool</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Contact Center Log Analysis & Root Cause Analysis'
    '</div>',
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

# ============================================================
# FILE UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">📁 Upload Log File</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload your contact center log file",
    type=["log", "txt", "csv"],
    help="Supported formats: .log, .txt, .csv",
)

valid_file = False

if uploaded_file is not None:

    file_ext = Path(uploaded_file.name).suffix.lower()
    raw_bytes = uploaded_file.getvalue()

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if file_ext not in ALLOWED_EXTENSIONS:

        st.error(
            "❌ Invalid file type. Please upload a .log, .txt or .csv file."
        )

    elif not raw_bytes:

        st.error("❌ The uploaded file is empty.")

    elif b"\x00" in raw_bytes[:4096]:

        st.error(
            "❌ Invalid file content. Please upload a valid text/log file."
        )

    else:

        valid_file = True

        st.success(
            f"✅ Valid file selected: **{uploaded_file.name}**"
        )

        # ----------------------------------------------------
        # Upload Button
        # ----------------------------------------------------

        if st.button(
            "📤 Upload File",
            type="secondary",
            width="stretch",
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        raw_bytes,
                        uploaded_file.type or "text/plain",
                    )
                }

                with st.spinner("Uploading log file..."):

                    response = requests.post(
                        UPLOAD_URL,
                        files=files,
                        timeout=30,
                    )

                if response.status_code == 200:

                    upload_data = response.json()

                    if upload_data.get("success"):

                        st.session_state.uploaded = True

                        st.session_state.uploaded_filename = (
                            upload_data.get(
                                "filename",
                                uploaded_file.name,
                            )
                        )

                        st.session_state.analysis = None

                        st.success(
                            "✅ File uploaded successfully. "
                            "You can now analyze the logs."
                        )

                    else:

                        st.error(
                            upload_data.get(
                                "message",
                                "File upload failed.",
                            )
                        )

                else:

                    st.error(
                        f"❌ Upload failed. HTTP {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to FastAPI backend. "
                    "Make sure Uvicorn is running on port 8000."
                )

            except Exception as e:

                st.error(f"❌ Upload error: {str(e)}")

# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.session_state.uploaded:

    st.markdown(
        f"**Uploaded file:** "
        f"`{st.session_state.uploaded_filename}`"
    )

    st.markdown("---")

    if st.button(
        "🚀 ANALYZE LOG",
        type="primary",
        width="stretch",
    ):

        try:

            with st.spinner(
                "🔍 Analyzing logs and generating RCA..."
            ):

                response = requests.get(
                    ANALYZE_URL,
                    timeout=120,
                )

            if response.status_code == 200:

                result = response.json()

                if result.get("success"):

                    st.session_state.analysis = result

                    st.success(
                        "✅ Log analysis completed successfully!"
                    )

                else:

                    st.error(
                        result.get(
                            "message",
                            "Analysis failed.",
                        )
                    )

                    if result.get("error_details"):
                        with st.expander("🔍 Backend Error Details"):
                            st.json(result.get("error_details"))

            else:

                st.error(
                    f"❌ Analysis failed. HTTP {response.status_code}"
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.code(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI backend. "
                "Make sure Uvicorn is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Analysis timed out. Please try again."
            )

        except Exception as e:

            st.error(f"❌ Analysis error: {str(e)}")

# ============================================================
# RESULTS
# ============================================================

result = st.session_state.analysis

if result:

    statistics = result.get("statistics", {})

    total_logs = int(
        statistics.get("total_logs", 0) or 0
    )

    errors = int(
        statistics.get("errors", 0) or 0
    )

    warnings = int(
        statistics.get("warnings", 0) or 0
    )

    severity = statistics.get(
        "severity",
        "UNKNOWN",
    )

    incidents = result.get(
        "incidents",
        [],
    ) or []

    rca_records = result.get(
        "root_cause_analysis",
        [],
    ) or []

    total_incidents = result.get(
        "total_incidents",
        len(incidents),
    )

    overall_status = result.get(
        "overall_status",
        "Unknown",
    )

    # ========================================================
    # DASHBOARD METRICS
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 System Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Logs",
            f"{total_logs:,}",
        )

    with col2:
        st.metric(
            "Errors",
            f"{errors:,}",
        )

    with col3:
        st.metric(
            "Warnings",
            f"{warnings:,}",
        )

    with col4:
        st.metric(
            "Incidents",
            f"{int(total_incidents):,}",
        )

    # ========================================================
    # SEVERITY
    # ========================================================

    st.markdown(
        '<div class="section-title">🚨 Severity Assessment</div>',
        unsafe_allow_html=True,
    )

    severity_upper = str(
        severity or "UNKNOWN"
    ).upper()

    if severity_upper == "CRITICAL":

        severity_class = "severity-critical"
        icon = "🔴"

    elif severity_upper == "HIGH":

        severity_class = "severity-high"
        icon = "🟠"

    elif severity_upper == "MEDIUM":

        severity_class = "severity-medium"
        icon = "🟡"

    else:

        severity_class = "severity-low"
        icon = "🟢"

    st.markdown(
        f"""
        <div class="{severity_class}">
            {icon} Overall Severity: {severity_upper}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.info(
        f"Overall System Status: **{overall_status}**"
    )

    # ========================================================
    # HEALTH SCORE
    # ========================================================

    # IMPORTANT:
    # Always initialize these before using them.

    error_percentage = 0.0
    warning_percentage = 0.0
    health_score = 100.0

    if total_logs > 0:

        error_percentage = (
            errors / total_logs
        ) * 100

        warning_percentage = (
            warnings / total_logs
        ) * 100

        health_score = max(
            0,
            100 - error_percentage,
        )

    st.markdown(
        '<div class="section-title">💚 System Health</div>',
        unsafe_allow_html=True,
    )

    health_col1, health_col2, health_col3 = st.columns(3)

    with health_col1:

        st.metric(
            "Health Score",
            f"{health_score:.2f}%",
        )

    with health_col2:

        st.metric(
            "Error Rate",
            f"{error_percentage:.2f}%",
        )

    with health_col3:

        st.metric(
            "Warning Rate",
            f"{warning_percentage:.2f}%",
        )

    st.progress(
        min(
            max(health_score / 100, 0),
            1.0,
        )
    )

    # ========================================================
    # COLORFUL PLOTLY DASHBOARD
    # ========================================================

    st.markdown(
        '<div class="section-title">📈 Visual Analytics Dashboard</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # DATA PREPARATION
    # --------------------------------------------------------

    other_logs = max(
        0,
        total_logs - errors - warnings,
    )

    log_data = pd.DataFrame(
        {
            "Type": [
                "Errors",
                "Warnings",
                "Other Logs",
            ],
            "Count": [
                errors,
                warnings,
                other_logs,
            ],
        }
    )

    # ========================================================
    # ROW 1 — BAR + DONUT
    # ========================================================

    chart_col1, chart_col2 = st.columns(2)

    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with chart_col1:

        st.markdown("### 📊 Log Distribution")

        fig_bar = px.bar(
            log_data,
            x="Type",
            y="Count",
            color="Type",
            text="Count",
            color_discrete_map={
                "Errors": "#EF4444",
                "Warnings": "#F59E0B",
                "Other Logs": "#22C55E",
            },
        )

        fig_bar.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
        )

        fig_bar.update_layout(
            height=420,
            showlegend=False,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20,
            ),
            yaxis_title="Number of Logs",
            xaxis_title="",
        )

        st.plotly_chart(
            fig_bar,
            width="stretch",
        )

    # --------------------------------------------------------
    # DONUT CHART
    # --------------------------------------------------------

    with chart_col2:

        st.markdown("### 🥧 Log Health Distribution")

        pie_data = log_data[
            log_data["Count"] > 0
        ]

        if not pie_data.empty:

            fig_pie = px.pie(
                pie_data,
                names="Type",
                values="Count",
                hole=0.48,
                color="Type",
                color_discrete_map={
                    "Errors": "#EF4444",
                    "Warnings": "#F59E0B",
                    "Other Logs": "#22C55E",
                },
            )

            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Count: %{value:,}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                ),
            )

            fig_pie.update_layout(
                height=420,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20,
                ),
                legend_title_text="Log Type",
            )

            st.plotly_chart(
                fig_pie,
                width="stretch",
            )

        else:

            st.info(
                "No log distribution data available."
            )

    # ========================================================
    # ROW 2 — SEVERITY + PRIORITY
    # ========================================================

    chart_col3, chart_col4 = st.columns(2)

    # --------------------------------------------------------
    # INCIDENT SEVERITY PIE
    # --------------------------------------------------------

    with chart_col3:

        st.markdown(
            "### 🚨 Incident Severity Distribution"
        )

        if rca_records:

            rca_df = pd.DataFrame(rca_records)

            if "severity" in rca_df.columns:

                severity_series = (
                    rca_df["severity"]
                    .fillna("UNKNOWN")
                    .astype(str)
                    .str.upper()
                    .value_counts()
                )

            else:

                severity_series = pd.Series(
                    dtype=int
                )

            if not severity_series.empty:

                severity_df = pd.DataFrame(
                    {
                        "Severity": severity_series.index,
                        "Count": severity_series.values,
                    }
                )

                fig_severity = px.pie(
                    severity_df,
                    names="Severity",
                    values="Count",
                    hole=0.42,
                    color="Severity",
                    color_discrete_map={
                        "CRITICAL": "#DC2626",
                        "HIGH": "#F97316",
                        "MEDIUM": "#FACC15",
                        "LOW": "#22C55E",
                    },
                )

                fig_severity.update_traces(
                    textposition="inside",
                    textinfo="percent+label",
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Incidents: %{value}<br>"
                        "Percentage: %{percent}"
                        "<extra></extra>"
                    ),
                )

                fig_severity.update_layout(
                    height=420,
                    margin=dict(
                        l=20,
                        r=20,
                        t=30,
                        b=20,
                    ),
                )

                st.plotly_chart(
                    fig_severity,
                    width="stretch",
                )

            else:

                st.info(
                    "No severity distribution available."
                )

        else:

            st.info(
                "No RCA severity data available."
            )

    # --------------------------------------------------------
    # INCIDENT PRIORITY
    # --------------------------------------------------------

    with chart_col4:

        st.markdown(
            "### 🎯 Incident Priority Distribution"
        )

        if incidents:

            incident_df_temp = pd.DataFrame(
                incidents
            )

            if "priority" in incident_df_temp.columns:

                priority_series = (
                    incident_df_temp["priority"]
                    .fillna("UNKNOWN")
                    .astype(str)
                    .str.upper()
                    .value_counts()
                )

            else:

                priority_series = pd.Series(
                    dtype=int
                )

            if not priority_series.empty:

                priority_df = pd.DataFrame(
                    {
                        "Priority": priority_series.index,
                        "Count": priority_series.values,
                    }
                )

                fig_priority = px.bar(
                    priority_df,
                    x="Priority",
                    y="Count",
                    color="Priority",
                    text="Count",
                    color_discrete_sequence=(
                        px.colors.qualitative.Bold
                    ),
                )

                fig_priority.update_traces(
                    textposition="outside",
                )

                fig_priority.update_layout(
                    height=420,
                    showlegend=False,
                    margin=dict(
                        l=20,
                        r=20,
                        t=30,
                        b=20,
                    ),
                    yaxis_title="Number of Incidents",
                    xaxis_title="Priority",
                )

                st.plotly_chart(
                    fig_priority,
                    width="stretch",
                )

            else:

                st.info(
                    "No priority data available."
                )

        else:

            st.info(
                "No incidents detected."
            )

    # ========================================================
    # ROW 3 — ERROR/WARNING COMPARISON
    # ========================================================

    st.markdown("### 📉 Error vs Warning Rate")

    rate_data = pd.DataFrame(
        {
            "Metric": [
                "Error Rate",
                "Warning Rate",
            ],
            "Percentage": [
                error_percentage,
                warning_percentage,
            ],
        }
    )

    fig_rate = px.bar(
        rate_data,
        x="Metric",
        y="Percentage",
        color="Metric",
        text="Percentage",
        color_discrete_map={
            "Error Rate": "#EF4444",
            "Warning Rate": "#F59E0B",
        },
    )

    fig_rate.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    fig_rate.update_layout(
        height=350,
        showlegend=False,
        yaxis_title="Percentage (%)",
        xaxis_title="",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20,
        ),
    )

    st.plotly_chart(
        fig_rate,
        width="stretch",
    )

    # ========================================================
    # INCIDENTS
    # ========================================================

    st.markdown(
        '<div class="section-title">🚨 Detected Incidents</div>',
        unsafe_allow_html=True,
    )

    if incidents:

        incident_rows = []

        for incident in incidents:

            incident_rows.append(
                {
                    "Incident": incident.get(
                        "incident",
                        "N/A",
                    ),
                    "Priority": incident.get(
                        "priority",
                        "N/A",
                    ),
                    "Severity": incident.get(
                        "severity",
                        "N/A",
                    ),
                }
            )

        incident_table = pd.DataFrame(
            incident_rows
        )

        st.dataframe(
            incident_table,
            width="stretch",
            hide_index=True,
        )

    else:

        st.success(
            "✅ No incidents detected."
        )

    # ========================================================
    # ROOT CAUSE ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-title">🤖 Root Cause Analysis</div>',
        unsafe_allow_html=True,
    )

    if rca_records:

        for index, rca in enumerate(
            rca_records,
            start=1,
        ):

            rca_severity = str(
                rca.get(
                    "severity",
                    "UNKNOWN",
                )
            ).upper()

            with st.expander(
                f"Incident {index} — {rca_severity}"
            ):

                st.markdown(
                    f"**Timestamp:** "
                    f"`{rca.get('timestamp', 'N/A')}`"
                )

                st.markdown(
                    f"**Error:** "
                    f"{rca.get('error', 'N/A')}"
                )

                st.markdown(
                    "### Root Cause"
                )

                st.write(
                    rca.get(
                        "root_cause",
                        "N/A",
                    )
                )

                reasons = rca.get(
                    "possible_reasons",
                    [],
                )

                if isinstance(reasons, str):
                    reasons = [reasons]

                if reasons:

                    st.markdown(
                        "### 🔍 Possible Reasons"
                    )

                    for reason in reasons:

                        st.markdown(
                            f"- {reason}"
                        )

                recommendations = rca.get(
                    "recommendations",
                    [],
                )

                if isinstance(
                    recommendations,
                    str,
                ):
                    recommendations = [
                        recommendations
                    ]

                if recommendations:

                    st.markdown(
                        "### 💡 Recommended Actions"
                    )

                    for recommendation in recommendations:

                        st.markdown(
                            f"- ✅ {recommendation}"
                        )

    else:

        st.info(
            "No root cause records available."
        )

    # ========================================================
    # AI EXECUTIVE REPORT
    # ========================================================

    st.markdown(
        '<div class="section-title">🧠 AI Executive Report</div>',
        unsafe_allow_html=True,
    )

    summary = result.get(
        "summary",
        "",
    )

    if summary:

        with st.expander(
            "View AI Generated Executive Report",
            expanded=True,
        ):

            st.markdown(
                str(summary)
            )

    else:

        st.info(
            "AI executive report is not available."
        )

    # ========================================================
    # RAW / PARSED LOG VIEW
    # ========================================================

    st.markdown(
        '<div class="section-title">📋 Uploaded Log Preview</div>',
        unsafe_allow_html=True,
    )

    if uploaded_file is not None:

        try:

            raw_text = uploaded_file.getvalue().decode(
                "utf-8",
                errors="replace",
            )

            lines = [
                line.strip()
                for line in raw_text.splitlines()
                if line.strip()
            ]

            parsed_rows = []

            preview_lines = lines[:1000]

            for line in preview_lines:

                timestamp = ""
                level = "INFO"

                timestamp_match = re.search(
                    r"\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}",
                    line,
                )

                if timestamp_match:

                    timestamp = timestamp_match.group()

                level_match = re.search(
                    r"\b(ERROR|WARNING|WARN|INFO|DEBUG|CRITICAL)\b",
                    line,
                    re.IGNORECASE,
                )

                if level_match:

                    level = (
                        level_match.group()
                        .upper()
                    )

                parsed_rows.append(
                    {
                        "Timestamp": timestamp,
                        "Level": level,
                        "Message": line,
                    }
                )

            if parsed_rows:

                logs_df = pd.DataFrame(
                    parsed_rows
                )

                st.caption(
                    f"Showing first "
                    f"{len(parsed_rows):,} log lines."
                )

                st.dataframe(
                    logs_df,
                    width="stretch",
                    hide_index=True,
                    height=400,
                )

            else:

                st.info(
                    "No readable log lines found."
                )

        except Exception as e:

            st.warning(
                f"Could not display log preview: {e}"
            )

    # ========================================================
    # DEBUG RESPONSE
    # ========================================================

    with st.expander("🔧 Debug: Backend Response"):

        st.json(result)

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("---")

    st.caption(
        "AI Log Analyzer & RCA Tool • "
        "Contact Center Intelligence"
    )