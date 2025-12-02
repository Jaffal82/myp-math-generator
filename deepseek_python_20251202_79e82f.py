import streamlit as st
import json
from datetime import datetime
import pandas as pd
import requests

# Set page config
st.set_page_config(
    page_title="MYP Math AI Assistant",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .assessment-card {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #3B82F6;
    }
    .stButton button {
        background-color: #10B981;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">🧮 MYP Math Assessment Generator</h1>', unsafe_allow_html=True)
st.markdown("Generate AI-powered MYP mathematics assessments in seconds!")

# Initialize session state
if 'assessments' not in st.session_state:
    st.session_state.assessments = []
if 'use_openai' not in st.session_state:
    st.session_state.use_openai = False

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # AI Provider Selection
    ai_provider = st.radio(
        "Choose AI Provider:",
        ["Free AI (Demo Mode)", "OpenAI (Requires API Key)"],
        index=0
    )
    
    if ai_provider == "OpenAI (Requires API Key)":
        api_key = st.text_input("OpenAI API Key", type="password")
        if api_key:
            st.session_state.use_openai = True
            st.session_state.api_key = api_key
            st.success("✓ API Key saved")
        else:
            st.warning("Enter API key to use OpenAI")
    else:
        st.info("Using free demo mode. Responses are examples.")
    
    st.divider()
    
    # Quick templates
    st.header("🚀 Quick Start")
    if st.button("📈 Sample Statistics Task", use_container_width=True):
        st.session_state.preset = "stats"
    if st.button("📐 Sample Geometry Task", use_container_width=True):
        st.session_state.preset = "geometry"
    if st.button("➗ Sample Algebra Task", use_container_width=True):
        st.session_state.preset = "algebra"
    
    st.divider()
    
    # Curriculum guide
    st.header("📚 MYP Guide")
    with st.expander("Command Terms"):
        st.write("""
        - **Describe**: Give a detailed account
        - **Explain**: Give reasons or causes
        - **Investigate**: Observe, study, examine
        - **Justify**: Give valid reasons
        - **Verify**: Confirm truth
        """)

# Main content
tab1, tab2, tab3 = st.tabs(["✨ Generate", "📚 Library", "📊 Analytics"])

# Tab 1: Generate Assessments
with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Assessment parameters
        st.subheader("Assessment Details")
        
        # Form
        with st.form("assessment_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                myp_level = st.selectbox("MYP Level", [1, 2, 3, 4, 5], index=2)
                topic = st.selectbox("Topic", [
                    "Algebra", "Number", "Geometry", 
                    "Statistics", "Probability"
                ])
            with col_b:
                criteria = st.multiselect(
                    "Criteria Focus",
                    ["Criterion A", "Criterion B", "Criterion C", "Criterion D"],
                    default=["Criterion B"]
                )
                difficulty = st.select_slider(
                    "Difficulty",
                    options=["Low", "Medium", "High"]
                )
            
            # Context
            context = st.text_area(
                "Real-world Context (Optional)",
                placeholder="e.g., Analyzing sports data, Designing a park, Budget planning...",
                height=60
            )
            
            # Submit button
            submitted = st.form_submit_button(
                "🚀 Generate Assessment",
                use_container_width=True,
                type="primary"
            )
    
    with col2:
        # Preview
        st.subheader("Example Output")
        with st.expander("Click to see example"):
            st.write("""
            **Title**: Sustainable Packaging Design
            
            **Task**: Investigate optimal dimensions for a shipping box...
            
            **Questions**:
            1. Calculate surface area...
            2. Optimize dimensions...
            3. Justify your design...
            
            **Skills**: Measurement, optimization, justification
            """)
        
        # Stats
        st.divider()
        st.metric("Assessments Generated", len(st.session_state.assessments))
        if st.session_state.assessments:
            latest = st.session_state.assessments[-1]
            st.caption(f"Latest: {latest['metadata']['topic']} (MYP {latest['metadata']['myp_level']})")
    
    # Handle form submission
    if submitted:
        with st.spinner("✨ Creating your assessment..."):
            # Simulate processing time
            import time
            time.sleep(1)
            
            # Create sample assessment (in real app, this would call AI)
            sample_assessments = {
                "stats": {
                    "title": "Sports Statistics Analysis",
                    "content": """**Title: Basketball Performance Analysis**

**Global Context:** Identities and Relationships (Sports and personal achievement)

**Task:** Analyze player statistics to determine the most valuable player for a tournament.

**Questions:**
1. Calculate mean, median, and mode for points scored by each player.
2. Create a comparative bar graph showing each player's performance.
3. Investigate which statistical measure best represents consistency. Justify your choice.
4. Propose a new way to calculate "player value" using multiple statistics.

**Mathematical Skills:** 
- Measures of central tendency
- Data representation
- Comparative analysis
- Justification

**Materials Needed:** Calculator, graph paper"""
                },
                "geometry": {
                    "title": "Playground Design Project",
                    "content": """**Title: Designing an Inclusive Playground**

**Global Context:** Fairness and Development

**Task:** Design a playground that is accessible to all children while maximizing space usage.

**Questions:**
1. Calculate the area of available land (composite shapes).
2. Design three different playground layouts using geometric shapes.
3. Investigate which design provides the best area-to-perimeter ratio.
4. Justify why your chosen design is most accessible.

**Mathematical Skills:**
- Area and perimeter calculations
- Geometric shape properties
- Optimization
- Spatial reasoning"""
                },
                "algebra": {
                    "title": "Smartphone Pricing Strategy",
                    "content": """**Title: Mobile Plan Comparison**

**Global Context:** Globalization and Sustainability

**Task:** Compare different mobile phone plans to find the most cost-effective option.

**Questions:**
1. Write linear equations representing three different pricing plans.
2. Graph the equations to find break-even points.
3. Investigate which plan is best for light, medium, and heavy users.
4. Create your own optimal pricing model with justification.

**Mathematical Skills:**
- Linear equations
- Graphing
- Systems of equations
- Problem-solving"""
                }
            }
            
            # Get preset or generate new
            if hasattr(st.session_state, 'preset') and st.session_state.preset:
                preset_key = st.session_state.preset
                assessment_content = sample_assessments[preset_key]["content"]
                assessment_title = sample_assessments[preset_key]["title"]
                del st.session_state.preset
            else:
                # Use topic to select appropriate sample
                topic_map = {
                    "Statistics": "stats",
                    "Geometry": "geometry", 
                    "Algebra": "algebra",
                    "Number": "algebra",
                    "Probability": "stats"
                }
                key = topic_map.get(topic, "algebra")
                assessment_content = sample_assessments[key]["content"]
                assessment_title = f"{topic} Assessment - MYP {myp_level}"
            
            # Create assessment object
            assessment = {
                "id": len(st.session_state.assessments) + 1,
                "title": assessment_title,
                "content": assessment_content,
                "metadata": {
                    "myp_level": myp_level,
                    "topic": topic,
                    "criteria": criteria,
                    "difficulty": difficulty,
                    "context": context if context else "General",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "ai_provider": ai_provider
                }
            }
            
            # Save to session
            st.session_state.assessments.append(assessment)
            
            # Display success
            st.success("✅ Assessment generated successfully!")
            st.balloons()
            
            # Show the assessment
            st.markdown(f"""
            <div class="assessment-card">
                <h3>{assessment['title']}</h3>
                <p><small>Generated: {assessment['metadata']['date']}</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(assessment_content)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    "📥 Download as .txt",
                    assessment_content,
                    file_name=f"MYP{myp_level}_{topic}.txt",
                    mime="text/plain"
                )
            with col2:
                if st.button("📋 Copy to Clipboard"):
                    st.code(assessment_content)
                    st.success("Copied to clipboard!")
            with col3:
                if st.button("💾 Save"):
                    st.success("Saved to library!")

# Tab 2: Library
with tab2:
    st.subheader("Your Assessment Library")
    
    if st.session_state.assessments:
        for i, assessment in enumerate(st.session_state.assessments):
            with st.expander(f"📄 {assessment['title']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Level:** MYP {assessment['metadata']['myp_level']}")
                    st.write(f"**Topic:** {assessment['metadata']['topic']}")
                    st.write(f"**Date:** {assessment['metadata']['date']}")
                with col2:
                    st.download_button(
                        "Download",
                        assessment['content'],
                        file_name=f"assessment_{i+1}.txt",
                        key=f"dl_{i}"
                    )
                st.divider()
                st.write(assessment['content'])
    else:
        st.info("No assessments yet. Generate one in the first tab!")

# Tab 3: Analytics
with tab3:
    st.subheader("Usage Analytics")
    
    if st.session_state.assessments:
        # Create simple dataframe
        import pandas as pd
        data = []
        for a in st.session_state.assessments:
            data.append({
                "Topic": a['metadata']['topic'],
                "Level": f"MYP {a['metadata']['myp_level']}",
                "Date": a['metadata']['date'],
                "Difficulty": a['metadata']['difficulty']
            })
        
        df = pd.DataFrame(data)
        
        # Show metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Generated", len(df))
        with col2:
            st.metric("Topics Covered", df['Topic'].nunique())
        with col3:
            st.metric("Most Used Level", df['Level'].mode()[0])
        
        # Show data
        st.dataframe(df, use_container_width=True)
        
        # Simple chart
        chart_data = df['Topic'].value_counts()
        st.bar_chart(chart_data)
    else:
        st.info("Generate assessments to see analytics here")

# Footer
st.divider()
st.caption("MYP Math Assessment Generator v1.0 | Made for IB Teachers")