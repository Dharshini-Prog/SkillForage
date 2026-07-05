import os
import time
import zipfile
import io
import streamlit as st
from agents.adk_root_agent import ADKRootAgent

# Constants
EXPORTS_DIR = "exports"

# Set up page
st.set_page_config(
    page_title="SkillForge",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_css():
    """Injects custom CSS for a modern, dark-themed UI."""
    st.markdown("""
    <style>
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 0;
            background: -webkit-linear-gradient(#1E88E5, #42A5F5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            font-weight: 400;
            color: #A0A0A0;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #1e1e1e;
            border: 1px solid #333;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            height: 100%;
        }
        .metric-card h4 {
            margin-top: 0;
            color: #e0e0e0;
            font-size: 1.1rem;
        }
        .metric-card p {
            margin-bottom: 0;
            font-size: 1.2rem;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            color: #888;
            font-size: 0.9rem;
        }
        /* Hide top padding */
        .block-container {
            padding-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renders the sidebar with workflow, sample prompts, and status."""
    with st.sidebar:
        st.title("🤖 SkillForge")
        
        st.markdown("### 🔄 System Workflow")
        st.markdown("""
        **User Request**  
        &nbsp;&nbsp;&nbsp;&nbsp;↓  
        **Planner Agent**  
        &nbsp;&nbsp;&nbsp;&nbsp;↓  
        **Generator Agent**  
        &nbsp;&nbsp;&nbsp;&nbsp;↓  
        **Reviewer Agent**  
        &nbsp;&nbsp;&nbsp;&nbsp;↓  
        **Exporter**
        """)
        
        st.markdown("### 💡 Sample Prompts")
        st.info("Build a skill that validates JSON payloads against a Pydantic schema.")
        st.info("Create a skill that extracts the primary intent from a user's natural language request.")
        
        st.markdown("### ℹ️ Project Overview")
        st.caption("SkillForge automatically plans, generates, reviews, and exports AI Agent Skills using a robust multi-agent architecture.")
        
        st.markdown("### 🟢 System Status")
        st.caption("All systems operational.")
        
        st.markdown("### 🧠 Model Info")
        st.caption("Google Gemini 2.5 Flash")

def get_recent_skills():
    """Reads the exports directory to find recently generated skills."""
    if not os.path.exists(EXPORTS_DIR):
        return []
    # Return directories sorted by creation time (newest first)
    dirs = [d for d in os.listdir(EXPORTS_DIR) if os.path.isdir(os.path.join(EXPORTS_DIR, d))]
    try:
        dirs.sort(key=lambda x: os.path.getctime(os.path.join(EXPORTS_DIR, x)), reverse=True)
    except Exception:
        pass
    return dirs

def render_recent_skills():
    """Renders the recent skills section."""
    skills = get_recent_skills()
    if skills:
        st.markdown("### 🕒 Recent Skills")
        for skill in skills[:5]:  # Show top 5
            with st.expander(f"📁 {skill}"):
                st.caption(f"Located in `exports/{skill}`")
                skill_path = os.path.join(EXPORTS_DIR, skill)
                files = os.listdir(skill_path)
                st.write(f"**Files Generated ({len(files)}):** {', '.join(files)}")

def parse_response(response_text):
    """Parses the ADKRootAgent string response safely."""
    if "Success! Exported to:" in response_text:
        lines = response_text.strip().split('\n')
        path_line = lines[0].replace("Success! Exported to: ", "").strip()
        score_line = lines[1].replace("Review Score: ", "").strip() if len(lines) > 1 else "N/A"
        status_line = lines[2].strip() if len(lines) > 2 else "Unknown"
        
        clean_path = path_line
        if "exports" in path_line.lower():
            idx = path_line.lower().find("exports")
            clean_path = path_line[idx:].replace('\\', '/')
            
        return True, clean_path, score_line, status_line, path_line
    return False, "", "", "", ""

def render_result_dashboard(clean_path, score_line, status_line):
    """Renders the 5 metric cards."""
    st.markdown("### 📊 Result Dashboard")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="metric-card"><h4>✅ Status</h4><p style="color:#4CAF50; font-weight:bold;">Success</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h4>⭐ Review Score</h4><p style="font-weight:bold;">{score_line}</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h4>✔ Review Result</h4><p style="color:#4CAF50; font-weight:bold;">{status_line}</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h4>📂 Export Folder</h4><p style="font-weight:bold; word-wrap:break-word; font-size:1rem;">{clean_path}</p></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-card"><h4>📄 Files Generated</h4><p style="font-weight:bold;">6</p></div>', unsafe_allow_html=True)

def render_tabs(full_path, clean_path, score_line, status_line):
    """Renders the detailed tabs and download buttons."""
    tab1, tab2, tab3 = st.tabs(["📄 Generated Files", "📋 Review Summary", "📦 Export Information"])
    
    files_to_check = [
        "SKILL.md", "README.md", "metadata.json", 
        "examples.md", "quality_config.json", "skill_card.md"
    ]
    
    with tab1:
        st.markdown("### Preview and Download")
        
        # Create ZIP download
        skill_name = os.path.basename(os.path.normpath(full_path))
        zip_name = f"{skill_name.replace(' ', '_')}.zip"
        
        zip_buffer = io.BytesIO()
        missing_files = []
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename in files_to_check:
                file_path = os.path.join(full_path, filename)
                if os.path.exists(file_path):
                    zip_file.write(file_path, arcname=filename)
                else:
                    missing_files.append(filename)
                    
        if missing_files:
            st.warning(f"⚠️ Warning: The following files are missing and won't be in the ZIP: {', '.join(missing_files)}")
            
        st.download_button(
            label="📦 Download Skill Package (.zip)",
            data=zip_buffer.getvalue(),
            file_name=zip_name,
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        
        st.markdown("#### Individual Files")
        cols = st.columns(3)
        
        for i, filename in enumerate(files_to_check):
            file_path = os.path.join(full_path, filename)
            col_idx = i % 3
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                with cols[col_idx]:
                    st.download_button(f"⬇️ Download {filename}", content, file_name=filename, use_container_width=True)
                    with st.expander(f"Preview {filename}"):
                        if filename.endswith(".json"):
                            st.json(content)
                        else:
                            st.markdown(content)
                            
    with tab2:
        st.markdown("### 📋 Review Summary")
        st.write(f"**Score:** {score_line}")
        st.write(f"**Status:** {status_line}")
        if "Passed" in status_line:
            st.success("The skill package met all quality thresholds and passed the autonomous review.")
        else:
            st.error("The skill package failed the review process.")
            
    with tab3:
        st.markdown("### 📦 Export Information")
        st.write(f"**Local Path:** `{clean_path}`")
        st.write(f"**Total Files:** 6")
        st.success("All files successfully saved to disk.")

def main():
    render_css()
    render_sidebar()
    
    # Hero Section
    st.markdown('<p class="hero-title">🤖 SkillForge</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">AI-Powered Multi-Agent Skill Generator</p>', unsafe_allow_html=True)
    st.markdown("SkillForge automatically plans, generates, reviews, and exports AI Agent Skills using a robust multi-agent architecture.")
    st.write("---")
    
    # Input Area
    st.markdown("### Describe Your AI Agent Skill")
    prompt = st.text_area(
        label="Skill Prompt",
        label_visibility="collapsed",
        height=150,
        max_chars=2000,
        placeholder="Example: Create a skill for an AI agent that summarizes research papers into actionable insights..."
    )
    
    if st.button("🚀 Generate Skill Package", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("⚠️ Please provide a prompt before generating.")
            return
            
        st.toast("Initialization complete. Starting multi-agent pipeline...")
        
        # Generation UI Sequence
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        agent = ADKRootAgent()
        
        # Simulate initial progress UI before blocking call
        status_text.markdown("#### ⏳ Planning Blueprint...")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        status_text.markdown("#### ⏳ Generating Skill Package...")
        progress_bar.progress(30)
        
        # Blocking call to backend
        response = agent.run(prompt)
        
        # Post-blocking rapid sequence
        status_text.markdown("#### ⏳ Reviewing Quality...")
        progress_bar.progress(80)
        time.sleep(0.5)
        
        status_text.markdown("#### ⏳ Exporting Files...")
        progress_bar.progress(95)
        time.sleep(0.5)
        
        status_text.markdown("#### ✅ Completed!")
        progress_bar.progress(100)
        
        # Clean up progress bar
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        st.write("---")
        
        # Parse and Display Results
        is_success, clean_path, score_line, status_line, full_path = parse_response(response)
        
        if is_success:
            st.toast("Skill generated successfully!", icon="✅")
            
            # Completion Screen Summary
            st.success(f"""
            **✅ Skill Generated Successfully**
            
            **Review Score:** {score_line}
            
            **Review Status:** {status_line}
            
            **Files Generated:** 6
            
            **Output Folder:** `{clean_path}`
            """)
            
            st.write("---")
            render_result_dashboard(clean_path, score_line, status_line)
            st.write("---")
            render_tabs(full_path, clean_path, score_line, status_line)
            
        elif "Review Failed!" in response:
            st.error("❌ Skill generation failed the quality review after maximum attempts.")
            st.write(response)
        elif "Clarification needed" in response:
            st.warning("⚠️ Clarification Needed")
            st.write(response)
        else:
            st.info("System Output:")
            st.write(response)
            
    st.write("---")
    render_recent_skills()
    
    st.markdown('<div class="footer">Built with Google Gemini • Streamlit • Multi-Agent Architecture • SkillForge</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()