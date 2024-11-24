import streamlit as st
import google.generativeai as genai


genai.configure(api_key="generate your api")




st.set_page_config(
    page_title="AI Python Code Reviewer",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("👨‍💻 AI Python Code Reviewer 🔍")
st.markdown("""
    ### :green[Review your Python code for errors, bugs, and improvements instantly!]
    **How it works:** 
    - Paste your Python code in the text area below. 
    - Click the **Generate Review** button to receive detailed feedback and suggestions.  
""")

user_prompt = st.text_area(
    label="Enter your Python code here:",
    placeholder="Paste your Python code here...",
    height=200
)


sys_prompt = (
    """
    You are a friendly AI assistant.
    Given a Python code to review, analyze the submitted code and identify bugs, errors, or areas of improvement.
    Provide fixed code snippets along with explanations.
    If the code is not in Python, politely remind the user that you specialize in Python code reviews.
    Use the format:
    ## Bug Report
    - List of identified issues here.
    ## Fixed Code
    Corrected code here.
    """
)


model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash", system_instruction=sys_prompt
)


st.sidebar.header("Options")
show_example = st.sidebar.checkbox("Show Example Code")

if show_example:
    st.sidebar.markdown("""
    ```python
    def example_function(x):
        return x + 1
    ```
    """)


if st.button("🚀 Generate Review"):
    if user_prompt.strip() == "":
        st.error("Please enter some Python code to review!")
    else:
        with st.spinner("Analyzing your code..."):
            try:
                response = model.generate_content([user_prompt, sys_prompt])
                ai_output = response.text  # Get the AI output as text

                
                bug_report = "No bugs or issues were identified in the code."  
                fixed_code = "No fixes or modifications needed for the code."  

               
                if "## Bug Report" in ai_output and "## Fixed Code" in ai_output:
                    sections = ai_output.split("## Fixed Code")
                    bug_report = sections[0].replace("## Bug Report", "").strip()
                    fixed_code = sections[1].strip()
                else:
                   
                    bug_report = ai_output.strip()
                    fixed_code = "No structured fixes provided. Check the bug report for details."

                
                st.success("Analysis Complete!")
                st.subheader(":red[🐞 Bug Report]")
                st.markdown("**Identified issues in your code:**")
                st.code(bug_report, language="text")

                
                st.subheader(":green[✅ Fixed Code]")
                st.markdown("**Suggested corrections to your code:**")
                st.code(fixed_code, language="python")

            except Exception as e:
                st.error(f"An error occurred: {e}")


st.markdown("""
    ---
    Developed by Joydeb Pal
""")