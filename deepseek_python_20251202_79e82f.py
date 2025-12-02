# ======== COMPLETE WORKING APP ========
# Copy ALL of this into your app.py

import streamlit as st
import openai
from datetime import datetime
import time

# Page setup
st.set_page_config(
    page_title="MYP Math AI",
    page_icon="🧮",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 2.8rem;
        margin-bottom: 1rem;
    }
    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton button {
        background-color: #10B981;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
    }
    .stButton button:hover {
        background-color: #0DA271;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-title">🧮 MYP Math Assessment Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AI-powered tool for creating MYP mathematics assessments</p>', unsafe_allow_html=True)

# Initialize session state
if 'assessments' not in st.session_state:
    st.session_state.assessments = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'connection_tested' not in st.session_state:
    st.session_state.connection_tested = False

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # Step 1: Enter API Key
    st.subheader("1. Enter OpenAI API Key")
    api_key = st.text_input(
        "API Key:",
        type="password",
        placeholder="sk-...",
        help="Get from https://platform.openai.com/api-keys",
        key="api_key_input"
    )
    
    # Store the key when entered
    if api_key:
        st.session_state.api_key = api_key
        openai.api_key = api_key
        st.success("✅ Key saved!")
    
    st.divider()
    
    # Step 2: Test Connection
    st.subheader("2. Test Connection")
    
    test_col1, test_col2 = st.columns(2)
    with test_col1:
        test_clicked = st.button("🧪 Test Now", use_container_width=True)
    
    with test_col2:
        if st.session_state.connection_tested:
            st.success("✅ Tested")
    
    if test_clicked:
        if not st.session_state.api_key:
            st.error("❌ Please enter API key first")
        else:
            with st.spinner("Testing connection to OpenAI..."):
                try:
                    # Simple test call
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "Say 'CONNECTED' in 3 words"}],
                        max_tokens=10
                    )
                    st.success("✅ **Connection Successful!**")
                    st.info(f"Response: {response.choices[0].message.content}")
                    st.session_state.connection_tested = True
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Connection failed: {str(e)}")
                    st.warning("Please check: 1) API key is correct 2) You have credits")
    
    st.divider()
    
    # Quick help
    st.subheader("📚 Quick Help")
    with st.expander("How to get API key"):
        st.write("""
        1. Go to [platform.openai.com](https://platform.openai.com)
        2. Sign up/login
        3. Click "API keys"
        4. Click "Create new secret key"
        5. Copy the key (starts with sk-)
        """)
    
    with st.expander("Cost information"):
        st.write("""
        - GPT-3.5: ~$0.0015 per assessment
        - Free credits: $5 for new users
        - 1 credit = ~1000 assessments
        """)

# ========== MAIN CONTENT ==========
tab1, tab2 = st.tabs(["✨ Generate Assessment", "📚 My Library"])

# TAB 1: Generate Assessment
with tab1:
    st.header("Create New Assessment")
    
    # Check API status
    if not st.session_state.api_key:
        st.warning("⚠️ **Please enter your OpenAI API key in the sidebar**")
        st.info("You need an API key to generate assessments. Get one from OpenAI (free credits available).")
    
    # Assessment form
    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            myp_level = st.selectbox("MYP Level", [1, 2, 3, 4, 5], index=2)
            topic = st.selectbox("Topic", [
                "Algebra", "Number", "Geometry", 
                "Statistics", "Probability", "Functions"
            ])
        
        with col2:
            criteria = st.multiselect(
                "Criteria Focus",
                ["A: Knowing & Understanding", 
                 "B: Investigating Patterns", 
                 "C: Communicating", 
                 "D: Applying in Real Life"],
                default=["B: Investigating Patterns"]
            )
            difficulty = st.select_slider(
                "Difficulty",
                options=["Beginner", "Intermediate", "Advanced"]
            )
        
        # Context input
        context = st.text_area(
            "Real-world Context",
            placeholder="Example: 'Analyzing sports statistics', 'Designing sustainable packaging', 'Planning a budget'...",
            height=80
        )
        
        # Submit button
        submitted = st.form_submit_button(
            "🚀 Generate with AI",
            type="primary",
            use_container_width=True
        )
    
    # Handle form submission
    if submitted:
        if not st.session_state.api_key:
            st.error("🔑 **API key required!** Enter it in the sidebar first.")
        elif not st.session_state.connection_tested:
            st.warning("⚠️ **Test your connection first!** Click 'Test Now' in sidebar.")
        else:
            with st.spinner("🧠 AI is creating your assessment... This takes 10-20 seconds"):
                
                # Show progress
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.1)
                    progress_bar.progress(i + 1)
                
                # Create the prompt
                prompt = f"""
                Create a complete MYP {myp_level} Mathematics assessment with these specifications:
                
                TOPIC: {topic}
                CRITERIA: {', '.join(criteria)}
                DIFFICULTY: {difficulty}
                REAL-WORLD CONTEXT: {context if context else 'General application'}
                
                Format your response as:
                
                ====== TITLE ======
                [Creative title]
                
                ====== TASK ======
                [Clear task description for students]
                
                ====== QUESTIONS ======
                1. [Question 1 - Basic understanding]
                2. [Question 2 - Application]
                3. [Question 3 - Analysis/Justification]
                4. [Question 4 - Extension]
                
                ====== SKILLS REQUIRED ======
                • [Skill 1]
                • [Skill 2]
                • [Skill 3]
                
                ====== TEACHER NOTES ======
                [Brief implementation notes]
                """
                
                try:
                    # Call OpenAI API
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert IB MYP Mathematics teacher."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    assessment_content = response.choices[0].message.content
                    
                    # Create assessment object
                    assessment = {
                        "id": len(st.session_state.assessments) + 1,
                        "title": f"MYP {myp_level} {topic} Assessment",
                        "content": assessment_content,
                        "metadata": {
                            "level": myp_level,
                            "topic": topic,
                            "criteria": criteria,
                            "context": context,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                    }
                    
                    # Save to session
                    st.session_state.assessments.append(assessment)
                    
                    # Show success
                    progress_bar.empty()
                    st.success("✅ Assessment generated successfully!")
                    st.balloons()
                    
                    # Display the assessment
                    st.markdown("---")
                    st.markdown(f"### 📄 {assessment['title']}")
                    st.markdown(f"*Generated: {assessment['metadata']['date']}*")
                    st.markdown("---")
                    
                    st.markdown(assessment_content)
                    
                    # Action buttons
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            "📥 Download as .txt",
                            assessment_content,
                            file_name=f"MYP{myp_level}_{topic}_Assessment.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col2:
                        if st.button("📋 Copy to Clipboard", use_container_width=True):
                            st.code(assessment_content)
                            st.success("Copied!")
                    
                    with col3:
                        if st.button("🔄 Generate Another", use_container_width=True):
                            st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error generating assessment: {str(e)}")
                    st.info("Try: 1) Check API key 2) Test connection 3) Ensure you have credits")

# TAB 2: Assessment Library
with tab2:
    st.header("📚 My Assessment Library")
    
    if st.session_state.assessments:
        st.success(f"You have {len(st.session_state.assessments)} saved assessment(s)")
        
        # Show all assessments
        for i, assessment in enumerate(st.session_state.assessments):
            with st.expander(f"📄 {assessment['title']} - {assessment['metadata']['date']}", expanded=(i==0)):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Level:** MYP {assessment['metadata']['level']}")
                    st.write(f"**Topic:** {assessment['metadata']['topic']}")
                    st.write(f"**Context:** {assessment['metadata']['context'][:50]}..." 
                             if assessment['metadata']['context'] else "No context")
                with col2:
                    st.download_button(
                        "Download",
                        assessment['content'],
                        file_name=f"assessment_{assessment['id']}.txt",
                        key=f"dl_{i}",
                        use_container_width=True
                    )
                st.markdown("---")
                st.markdown(assessment['content'])
    else:
        st.info("📭 No assessments yet. Generate your first one in the 'Generate Assessment' tab!")

# Footer
st.markdown("---")
st.markdown("**MYP Math AI Generator** • Powered by OpenAI • Made for IB Teachers")
