import openai
from typing import List, Dict, Optional
from config import Config
import json

class EnglishTeacher:
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
        
        try:
            # Initialize OpenAI client with explicit parameters
            self.client = openai.OpenAI(
                api_key=Config.OPENAI_API_KEY,
                timeout=30.0
            )
            self.conversation_history = []
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}. Please check your API key and internet connection.")
        
    def get_teacher_response(self, user_input: str, mode: str = "conversation", level: str = "intermediate") -> Dict:
        """
        Get a response from the English teacher based on user input and learning mode.
        
        Args:
            user_input: The student's input text
            mode: Learning mode (conversation, grammar, vocabulary, writing)
            level: Student's English level (beginner, intermediate, advanced)
            
        Returns:
            Dictionary containing the teacher's response and analysis
        """
        
        # Create mode-specific prompt
        mode_prompt = self._get_mode_prompt(mode, level)
        
        # Build conversation context
        messages = [
            {"role": "system", "content": Config.TEACHER_SYSTEM_PROMPT + "\n\n" + mode_prompt}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-6:])  # Keep last 3 exchanges
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            teacher_response = response.choices[0].message.content
            
            # Analyze the user input for corrections and feedback
            analysis = self._analyze_user_input(user_input, mode)
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": teacher_response})
            
            return {
                "response": teacher_response,
                "analysis": analysis,
                "mode": mode,
                "level": level
            }
            
        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                "analysis": {"error": str(e)},
                "mode": mode,
                "level": level
            }
    
    def _get_mode_prompt(self, mode: str, level: str) -> str:
        """Generate mode-specific instructions for the teacher."""
        
        level_context = {
            "beginner": "The student is a beginner. Use simple vocabulary and short sentences. Focus on basic grammar and common words.",
            "intermediate": "The student is at an intermediate level. Use varied vocabulary and explain more complex grammar concepts.",
            "advanced": "The student is advanced. Focus on nuanced language, idioms, and sophisticated expressions."
        }
        
        mode_instructions = {
            "conversation": f"""
            Mode: Conversation Practice
            {level_context[level]}
            - Engage in natural conversation
            - Gently correct mistakes when they occur
            - Ask follow-up questions to keep the conversation flowing
            - Provide explanations for corrections
            """,
            
            "grammar": f"""
            Mode: Grammar Check
            {level_context[level]}
            - Focus specifically on grammar corrections
            - Explain grammar rules clearly
            - Provide examples of correct usage
            - Identify patterns in the student's mistakes
            """,
            
            "vocabulary": f"""
            Mode: Vocabulary Building
            {level_context[level]}
            - Suggest better word choices
            - Explain word meanings and usage
            - Provide synonyms and antonyms
            - Give examples of how to use new words
            """,
            
            "writing": f"""
            Mode: Writing Practice
            {level_context[level]}
            - Review the student's writing
            - Suggest improvements for clarity and style
            - Focus on sentence structure and flow
            - Provide constructive feedback
            """
        }
        
        return mode_instructions.get(mode, mode_instructions["conversation"])
    
    def _analyze_user_input(self, user_input: str, mode: str) -> Dict:
        """Analyze user input for specific feedback based on mode."""
        
        analysis_prompts = {
            "grammar": "Analyze this text for grammar mistakes. List any errors and provide corrections with explanations.",
            "vocabulary": "Analyze this text for vocabulary improvements. Suggest better word choices and explain why.",
            "writing": "Analyze this text for writing quality. Suggest improvements for clarity, style, and structure.",
            "conversation": "Analyze this text for any language issues. Provide gentle corrections and suggestions."
        }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a language analysis assistant. Provide concise, helpful feedback."},
                    {"role": "user", "content": f"{analysis_prompts[mode]}\n\nText: {user_input}"}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return {"feedback": response.choices[0].message.content}
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation session."""
        if not self.conversation_history:
            return "No conversation history available."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Provide a brief summary of this English learning conversation, highlighting key topics and improvements."},
                    {"role": "user", "content": f"Conversation history: {json.dumps(self.conversation_history, indent=2)}"}
                ],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Could not generate summary: {str(e)}"
