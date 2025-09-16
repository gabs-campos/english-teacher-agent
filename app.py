import streamlit as st
import time
from english_teacher import EnglishTeacher
from config import Config
import os

# Page configuration
st.set_page_config(
    page_title="English Teacher Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .teacher-response {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .analysis-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
    .mode-selector {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'teacher' not in st.session_state:
        try:
            st.session_state.teacher = EnglishTeacher()
        except ValueError as e:
            st.error(f"Configuration Error: {e}")
            st.stop()
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "conversation"
    
    if 'current_level' not in st.session_state:
        st.session_state.current_level = "intermediate"

def display_conversation_history():
    """Display the conversation history."""
    if st.session_state.conversation_history:
        st.markdown("### 💬 Conversation History")
        
        for i, exchange in enumerate(st.session_state.conversation_history):
            with st.expander(f"Exchange {i+1} - {exchange['mode'].title()}", expanded=False):
                st.markdown(f"**You:** {exchange['user_input']}")
                st.markdown(f"**Teacher:** {exchange['response']}")
                
                if exchange.get('analysis', {}).get('feedback'):
                    st.markdown("**Analysis:**")
                    st.markdown(f"<div class='analysis-box'>{exchange['analysis']['feedback']}</div>", 
                              unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 English Teacher Agent</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Learning level selection
        st.markdown("**Your English Level:**")
        level = st.selectbox(
            "Select your level",
            options=list(Config.LEVELS.keys()),
            format_func=lambda x: Config.LEVELS[x],
            index=list(Config.LEVELS.keys()).index(st.session_state.current_level)
        )
        st.session_state.current_level = level
        
        # Learning mode selection
        st.markdown("**Learning Mode:**")
        mode = st.selectbox(
            "Choose your learning mode",
            options=list(Config.MODES.keys()),
            format_func=lambda x: Config.MODES[x],
            index=list(Config.MODES.keys()).index(st.session_state.current_mode)
        )
        st.session_state.current_mode = mode
        
        st.markdown("---")
        
        # Mode descriptions
        st.markdown("### 📖 Mode Descriptions")
        mode_descriptions = {
            "conversation": "Practice natural conversation with gentle corrections",
            "grammar": "Focus on grammar corrections and explanations",
            "vocabulary": "Improve your vocabulary with better word choices",
            "writing": "Get feedback on your writing style and structure"
        }
        st.info(mode_descriptions[mode])
        
        st.markdown("---")
        
        # Session controls
        st.markdown("### 🎛️ Session Controls")
        if st.button("🗑️ Clear Conversation", help="Clear the current conversation history"):
            st.session_state.teacher.clear_conversation()
            st.session_state.conversation_history = []
            st.success("Conversation cleared!")
            st.rerun()
        
        if st.button("📊 Get Session Summary", help="Get a summary of your learning session"):
            if st.session_state.conversation_history:
                with st.spinner("Generating summary..."):
                    summary = st.session_state.teacher.get_conversation_summary()
                st.markdown("### Session Summary")
                st.write(summary)
            else:
                st.info("No conversation history to summarize.")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💭 Start Learning!")
        
        # Display current mode and level
        st.markdown(f"""
        <div class="mode-selector">
            <strong>Current Mode:</strong> {Config.MODES[mode]}<br>
            <strong>Your Level:</strong> {Config.LEVELS[level]}
        </div>
        """, unsafe_allow_html=True)
        
        # User input
        user_input = st.text_area(
            "Type your message here:",
            placeholder="Ask a question, start a conversation, or share something you'd like me to help you with!",
            height=100,
            key="user_input"
        )
        
        # Submit button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            submit_button = st.button("🚀 Send", type="primary", use_container_width=True)
        
        with col_btn2:
            if st.button("💡 Get Example", use_container_width=True):
                examples = {
                    "conversation": "Hi! I'm learning English. Can we talk about your favorite hobby?",
                    "grammar": "I have went to the store yesterday and buyed some apples.",
                    "vocabulary": "The weather is very good today. I feel happy.",
                    "writing": "I want to write a letter to my friend about my vacation."
                }
                st.session_state.example_text = examples[mode]
                st.rerun()
        
        # Display example if available
        if 'example_text' in st.session_state:
            st.info(f"💡 Example: {st.session_state.example_text}")
            if st.button("Use Example"):
                user_input = st.session_state.example_text
                del st.session_state.example_text
                submit_button = True
        
        # Process user input
        if submit_button and user_input.strip():
            with st.spinner("Teacher is thinking..."):
                try:
                    # Get teacher response
                    result = st.session_state.teacher.get_teacher_response(
                        user_input, 
                        mode=st.session_state.current_mode,
                        level=st.session_state.current_level
                    )
                    
                    # Store in conversation history
                    st.session_state.conversation_history.append({
                        'user_input': user_input,
                        'response': result['response'],
                        'analysis': result['analysis'],
                        'mode': result['mode'],
                        'timestamp': time.time()
                    })
                    
                    # Clear input
                    st.session_state.user_input = ""
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    with col2:
        st.markdown("### 📈 Learning Tips")
        
        tips = {
            "conversation": [
                "💬 Don't worry about making mistakes - they're part of learning!",
                "🔄 Try to use new vocabulary you've learned",
                "❓ Ask questions to keep the conversation flowing",
                "🎯 Focus on expressing your ideas clearly"
            ],
            "grammar": [
                "📝 Pay attention to verb tenses",
                "🔍 Look for patterns in your mistakes",
                "📚 Practice with similar sentences",
                "✅ Review corrections carefully"
            ],
            "vocabulary": [
                "📖 Learn words in context",
                "🔄 Use new words in different sentences",
                "📝 Keep a vocabulary notebook",
                "🎯 Focus on words you use often"
            ],
            "writing": [
                "✍️ Plan your ideas before writing",
                "📝 Use varied sentence structures",
                "🔍 Check for clarity and flow",
                "📚 Read your writing aloud"
            ]
        }
        
        for tip in tips[mode]:
            st.markdown(tip)
        
        st.markdown("---")
        st.markdown("### 🏆 Progress")
        st.metric("Conversations", len(st.session_state.conversation_history))
        
        if st.session_state.conversation_history:
            recent_modes = [ex['mode'] for ex in st.session_state.conversation_history[-5:]]
            mode_counts = {mode: recent_modes.count(mode) for mode in set(recent_modes)}
            st.markdown("**Recent Activity:**")
            for mode_name, count in mode_counts.items():
                st.markdown(f"• {Config.MODES[mode_name]}: {count}")
    
    # Display conversation history
    if st.session_state.conversation_history:
        st.markdown("---")
        display_conversation_history()

if __name__ == "__main__":
    main()
