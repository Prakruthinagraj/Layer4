import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import random
from datetime import datetime

st.set_page_config(page_title="🧠 MindCare", page_icon="🧠", layout="wide")

# 🌸 PASTEL COLOR THEME
st.markdown("""
<style>
    /* PASTEL COLORS */
    :root {
        --pastel-bg: linear-gradient(135deg, #FEF5F7 0%, #F0F8FF 50%, #F5F5F5 100%);
        --pastel-primary: #FFB3BA;
        --pastel-secondary: #A8D5E2; 
        --pastel-accent: #FFE4E1;
        --pastel-text: #5A6377;
    }
    
    [data-testid="stAppViewContainer"] {
        background: var(--pastel-bg) !important;
        padding-top: 2rem;
    }
    
    /* Chat bubbles */
    .stChatMessage {
        background: rgba(255,255,255,0.8) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.8);
    }
    
    /* User messages */
    div[data-testid="messageText"] div:has(span.user) {
        background: linear-gradient(135deg, var(--pastel-primary), #FFCDD2) !important;
        color: #5A6377 !important;
        border-radius: 24px 24px 8px 24px !important;
        padding: 1.2rem !important;
        box-shadow: 0 8px 25px rgba(255,179,186,0.4);
    }
    
    /* Bot messages */
    div[data-testid="messageText"] div:has(span.assistant) {
        background: linear-gradient(135deg, #F8F9FF, #E8F4FD) !important;
        color: var(--pastel-text) !important;
        border-radius: 24px 24px 24px 8px !important;
        border: 1px solid var(--pastel-secondary) !important;
        box-shadow: 0 6px 20px rgba(168,213,226,0.3);
    }
    
    /* Input */
    [data-testid="stChatInput"] input {
        border-radius: 30px !important;
        border: 2px solid var(--pastel-secondary) !important;
        background: rgba(255,255,255,0.9) !important;
        padding: 1.2rem 1.8rem !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Buttons */
    button {
        background: linear-gradient(135deg, var(--pastel-primary), #FFCDD2) !important;
        border-radius: 25px !important;
        height: 50px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(255,179,186,0.4);
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    h1 { color: var(--pastel-text) !important; text-shadow: 0 2px 10px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "🌸 **Hi!** I'm MindCare, your gentle companion. "
                        "💕 I'm here to listen with care. What's on your heart today?", "emotion": "neutral"}]
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []

# Header
st.title("🌸 LAYER 4")
st.markdown("✨ *Your soft space for emotional wellness*")

# EMPATHETIC RESPONSES FUNCTION (COMPLETE WITH BREAKUP + WORKLOAD)
def get_empathetic_response(prompt):
    prompt_lower = prompt.lower().strip()
    
    # 🌟 GREETING DETECTION
    greetings = ['hey', 'hi', 'hello', 'namasthe', 'namaste', 'hai']
    if any(greeting in prompt_lower for greeting in greetings):
        greeting_replies = [
            "🌸 **Namasthe!** 💕 So lovely to hear from you! How's your heart today?",
            "🌟 **Hello there!** ✨ I'm here and ready to listen. What's on your mind?",
            "☀️ **Hey!** 🌼 What a joy to connect with you. How are you feeling?",
            "🙏 **Namasthe!** 🌸 The light in me honors the light in you. What's stirring?",
            "🌈 **Hi beautiful soul!** 💖 I'm all ears. Share what's in your heart.",
            "✨ **Hello!** 🌿 Thank you for reaching out. How can I support you today?"
        ]
        return random.choice(greeting_replies), "joy"
    
    # 🔥 OFFENSIVE/INTENSE ANGER + BREAKUP + WORKLOAD DETECTION
    offensive_keywords = ['kill', 'die', 'hate', 'stupid', 'idiot', 'fuck', 'shit', 'bitch', 'damn', 'asshole']
    workload_keywords = ['workload', 'work load', 'busy', 'overloaded', 'too much work', 'exhausted', 'burnout', 'tired from work']
    breakup_keywords = ['breakup', 'broke up', 'dumped', 'ex', 'split', 'heartbreak', 'single', 'relationship ended']
    
    if any(word in prompt_lower for word in offensive_keywords):
        intense_replies = [
            "🌩️ I hear the raw intensity in your words. What's making you feel this way?",
            "🌩️ That sounds like deep, powerful anger. I'm here to listen safely.",
            "🌩️ Your feelings are valid, even the intense ones. What's behind this?",
            "🌩️ I can feel the storm in your words. Want to share what's fueling it?",
            "🌩️ That anger sounds overwhelming. I'm holding space for you right now.",
            "🌩️ I hear your rage. You don't have to carry it alone. What's hurting?"
        ]
        return random.choice(intense_replies), "anger"
    elif any(word in prompt_lower for word in workload_keywords):
        workload_replies = [
            "💼 That workload sounds overwhelming. What's feeling most heavy right now?",
            "💼 You're carrying a lot. Which part of work is weighing on you most?",
            "💼 Work burnout is real. What would help ease this pressure?",
            "💼 I hear your exhaustion. What's one thing you need right now?",
            "💼 That sounds like too much. How can we break this down together?",
            "💼 Work stress can be crushing. I'm here while you breathe through it."
        ]
        return random.choice(workload_replies), "stress"
    elif any(word in prompt_lower for word in breakup_keywords):
        breakup_replies = [
            "💔 Heartbreak hurts deeply. What's the hardest part of this for you?",
            "💔 Breakups leave such big holes. I'm here while you feel this.",
            "💔 That loss sounds devastating. What do you need most right now?",
            "💔 Your heart is healing through pain. I'm sitting with you in this.",
            "💔 Rejection stings deeply. You're still worthy of love.",
            "💔 That ending feels so final. I'm here in this tender space with you."
        ]
        return random.choice(breakup_replies), "crisis"
    
    # Regular emotion keywords
    keywords = {
        "sadness": ['sad', 'hurt', 'down', 'cry', 'heavy', 'pain', 'tears', 'broken', 'lost', 'depressed', 'empty'],
        "fear": ['scared', 'fear', 'anxious', 'worry', 'afraid', 'panic', 'nervous', 'stress', 'worried'],
        "anger": ['angry', 'mad', 'frustrated', 'rage', 'furious', 'annoyed', 'irritated'],
        "joy": ['happy', 'great', 'excited', 'joy', 'love', 'amazing', 'wonderful', 'good', 'smile'],
        "crisis": ['help', 'alone', 'hopeless', 'end', 'suicide', 'overwhelmed', 'breaking']
    }
    
    # Check for emotion match
    for emotion, words in keywords.items():
        if any(word in prompt_lower for word in words):
            replies = {
                "sadness": [
                    "🌧️ I hear the weight in your words. What feels heaviest right now?",
                    "🌧️ That sounds really painful. I'm here with you through this.",
                    "🌧️ Your heart sounds heavy. What's weighing on you most today?",
                    "🌧️ I feel the sadness in your words. Want to share more about it?"
                ],
                "fear": [
                    "🌫️ That sounds really overwhelming. What's making you feel this way?",
                    "🌫️ I can feel your worry. What's the scariest part for you?",
                    "🌫️ That must feel so uncertain. I'm here to listen.",
                    "🌫️ Your anxiety sounds real. What triggered this feeling?"
                ],
                "anger": [
                    "🌩️ I can feel the intensity behind those words. What's stirring this up?",
                    "🌩️ That sounds frustrating. What's making you feel this way?",
                    "🌩️ I hear your anger. What happened to bring this out?",
                    "🌩️ Your frustration is valid. Want to tell me more?"
                ],
                "joy": [
                    "🌈 That's beautiful to hear! What made your heart light up?",
                    "🌈 Your happiness is contagious! What brought this joy?",
                    "🌈 I'm so glad to hear this! What made you smile today?",
                    "🌈 That sounds wonderful! Tell me more about what made you happy."
                ],
                "crisis": [
                    "💔 I'm right here with you. What's the hardest part you're carrying?",
                    "💔 You don't have to face this alone. I'm listening completely.",
                    "💔 That sounds incredibly tough. You matter to me.",
                    "💔 I'm holding space for you right now. What's most painful?"
                ]
            }
            return random.choice(replies[emotion]), emotion
    
    # DYNAMIC neutral responses
    neutral_replies = [
        "☁️ Thank you for sharing. 🌼 What else is on your mind beneath the surface?",
        "☁️ I appreciate you opening up. What's feeling most present for you now?",
        "☁️ That's helpful to know. What would you like to explore next?",
        "☁️ I'm listening carefully. Is there more you'd like to share?",
        "☁️ Thank you for trusting me. What's stirring in your heart right now?",
        "☁️ I hear you. 🌸 What's the next thing on your mind?",
        "☁️ Your words matter. What else feels important to share?"
    ]
    return random.choice(neutral_replies), "neutral"

# Chat display
st.markdown("---")
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🌸" if message["role"] == "assistant" else "💕"):
        icons = {"neutral": "☁️", "sadness": "🌧️", "anger": "🌩️", "fear": "🌫️", "joy": "🌈", "crisis": "💔", "stress": "💼"}
        icon = icons.get(message.get("emotion", "neutral"), "🌸")
        st.markdown(f"**{icon}** {message['content']}")
        if message["role"] == "assistant":
            st.caption(f"*{message.get('emotion', 'listening').title()}*")

# Chat input
if prompt := st.chat_input("💭 Share your thoughts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🌿 Reflecting..."):
            reply, emotion = get_empathetic_response(prompt)
        
        icons = {"crisis": "💔", "sadness": "🌧️", "fear": "🌫️", "anger": "🌩️", "joy": "🌈", "neutral": "☁️", "stress": "💼"}
        st.markdown(f"{icons.get(emotion, '🌸')} **{reply}**")
        
        st.session_state.messages.append({"role": "assistant", "content": reply, "emotion": emotion})
        st.session_state.emotion_history.append(emotion)

# 🌸 EMOTION DASHBOARD
st.markdown("---")
if st.session_state.emotion_history:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🌸 Mood Flowers")
        emotions_df = pd.DataFrame({
            "Emotion": st.session_state.emotion_history[-20:],
            "Count": [1] * len(st.session_state.emotion_history[-20:])
        }).groupby("Emotion").sum().reset_index()
        st.bar_chart(emotions_df.set_index("Emotion"), height=350)
    
    with col2:
        st.subheader("💫 Wellness")
        total = len(st.session_state.emotion_history)
        primary = max(set(st.session_state.emotion_history), key=st.session_state.emotion_history.count)
        st.metric("💬 Chats", total)
        st.metric("🌺 Main Mood", primary.title())
        positive = sum(1 for e in st.session_state.emotion_history if e in ["joy", "neutral"])
        st.metric("🌈 Positive", f"{positive}/{total}")

# Quick moods
st.markdown("---")
st.markdown("### 🌼 Quick Feelings")
cols = st.columns(5)
for col, (emoji, text) in enumerate([
    ("🌧️ Sad", "I'm feeling sad"), ("🌫️ Anxious", "I'm anxious"),
    ("☁️ Neutral", "Just checking in"), ("🌈 Happy", "I'm happy"),
    ("💼 Stressed", "My workload is too much")
]):
    if cols[col].button(emoji, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": text})
        st.rerun()

# 🎤 VOICE RECOGNITION (Browser-based)
st.markdown("---")
st.markdown("### 🎤 Voice Companion")
components.html("""
<div style='background: linear-gradient(135deg, #FFE4E1, #F8F9FF); padding: 2rem; border-radius: 25px; 
           border: 2px solid rgba(255,179,186,0.4); text-align: center; box-shadow: 0 12px 40px rgba(0,0,0,0.1);'>
    <div style='font-size: 18px; margin-bottom: 1rem; color: #5A6377;'>🌸 Speak your heart</div>
    <button id='voiceBtn' style='width:100%; padding:1.5rem; background:linear-gradient(135deg, #FFB3BA, #FFCDD2); 
                                color:#5A6377; border:none; border-radius:30px; font-size:20px; cursor:pointer; 
                                font-weight:600; box-shadow:0 8px 25px rgba(255,179,186,0.4);'>🎤 Hold & Speak</button>
    <div id='voiceStatus' style='margin-top:1.5rem; font-size:18px; font-weight:500; color:#5A6377; min-height:30px;'></div>
</div>
<script>
let recognition;
const btn = document.getElementById('voiceBtn');
const status = document.getElementById('voiceStatus');

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        status.textContent = `You said: "${transcript}" 🌸`;
        window.parent.postMessage({type: 'streamlit:setChatInput', value: transcript}, '*');
    };
    
    recognition.onerror = () => status.textContent = 'Try again 🌿';
}

btn.onmousedown = btn.ontouchstart = () => {
    if (recognition) {
        status.textContent = 'Listening... 🎤';
        btn.style.background = 'linear-gradient(135deg, #FFCDD2, #FFB3BA)';
        btn.innerHTML = '🗣️ Listening...';
        recognition.start();
    } else {
        status.textContent = 'Voice not supported (use Chrome) 🌸';
    }
};

btn.onmouseup = btn.ontouchend = () => {
    if (recognition) {
        recognition.stop();
        btn.style.background = 'linear-gradient(135deg, #FFB3BA, #FFCDD2)';
        btn.innerHTML = '🎤 Hold & Speak';
    }
};
</script>
""", height=220)

st.markdown("---")
st.markdown("*🌸 For emergencies: 1800-599-0019 | Made with love 💕*")