import streamlit as st
import google.generativeai as genai
import requests

# ----------------------------------------
# ✅ HARDCODED CONFIGURATION (EDIT HERE)
# ----------------------------------------
GEMINI_API_KEY = "AIzaSyCbidu_U2Ro7cnuB5aWRfAfswT4Eu-3LR4"  # 🔐 Replace with your actual key
WEBHOOK_URL = "https://mukilan114.app.n8n.cloud/webhook-test/Responsse"  # 🌐 Optional: webhook receiver URL

# ----------------------------------------
# ✅ GEMINI SETUP
# ----------------------------------------
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"❌ Failed to configure Gemini API: {e}")
    st.stop()

# ----------------------------------------
# ✅ STREAMLIT UI
# ----------------------------------------
st.set_page_config(page_title="🧠 Smart To-Do List with AI", layout="centered")
st.title("🧠 Smart To-Do List with AI Suggestions")

st.subheader("📋 Create a High-Impact Task Plan")
task_input = st.text_area("Describe your task or goal:", placeholder="e.g., Launch a personal blog")

# Generate plan using Gemini
if st.button("✨ Analyze Task"):
    if not task_input.strip():
        st.warning("Please enter a task to continue.")
    else:
        with st.spinner("Analyzing your task with Gemini 2.0 Flash..."):
            # Gemini prompt
            prompt = f"""
You are a productivity assistant AI.

Task: "{task_input}"

Give me:
1. A breakdown of subtasks
2. Estimated time for each subtask
3. Dependencies between subtasks (if any)
4. Possible productivity blockers

Respond clearly in Markdown.
Use emojis where helpful.
Keep it under 150 words.
"""

            try:
                # Generate with Gemini Flash
                chat = genai.GenerativeModel("gemini-2.0-flash").start_chat()
                result = chat.send_message(prompt)

                st.success("🧠 Gemini's Smart Plan")
                st.markdown(result.text)

                # Send to webhook if provided
                if WEBHOOK_URL:
                    try:
                        payload = {
                            "original_task": task_input,
                            "gemini_output": result.text
                        }
                        r = requests.post(WEBHOOK_URL, json=payload)
                        if r.status_code == 200:
                            st.info("✅ Sent plan to webhook successfully.")
                        else:
                            st.warning(f"⚠️ Webhook returned status: {r.status_code}")
                    except Exception as e:
                        st.warning(f"⚠️ Failed to send to webhook: {e}")

            except Exception as e:
                st.error(f"❌ Gemini API failed: {e}")

# ----------------------------------------
# ✅ FOOTER
# ----------------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini Flash · Python 3.13.4 · No API input UI")
