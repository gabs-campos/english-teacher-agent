# 📚 English Teacher Agent

An intelligent English learning assistant powered by OpenAI's GPT models and built with Streamlit. This agent helps you improve your English through conversation practice, grammar correction, vocabulary building, and writing feedback.

## ✨ Features

- **🤖 AI-Powered Teaching**: Uses OpenAI's GPT-3.5-turbo for intelligent language assistance
- **💬 Conversation Practice**: Natural conversation with gentle corrections
- **📝 Grammar Check**: Detailed grammar analysis and explanations
- **📚 Vocabulary Building**: Word suggestions and usage examples
- **✍️ Writing Practice**: Style and structure feedback
- **📊 Progress Tracking**: Session summaries and learning analytics
- **🎯 Adaptive Learning**: Adjusts to your English level (Beginner, Intermediate, Advanced)
- **💾 Conversation History**: Keep track of your learning journey

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd english-teacher-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python run.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   The app will automatically open at `http://localhost:8501`

## 🎯 How to Use

### Learning Modes

1. **Conversation Practice** 💬
   - Engage in natural conversations
   - Get gentle corrections and explanations
   - Practice speaking and listening skills

2. **Grammar Check** 📝
   - Submit text for grammar analysis
   - Receive detailed explanations of mistakes
   - Learn grammar rules with examples

3. **Vocabulary Building** 📚
   - Get suggestions for better word choices
   - Learn synonyms, antonyms, and usage
   - Expand your vocabulary with context

4. **Writing Practice** ✍️
   - Submit written work for feedback
   - Improve style, clarity, and structure
   - Learn to write more effectively

### English Levels

- **Beginner (A1-A2)**: Basic vocabulary and simple sentences
- **Intermediate (B1-B2)**: Varied vocabulary and complex grammar
- **Advanced (C1-C2)**: Nuanced language and sophisticated expressions

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Customization

You can modify the teacher's behavior by editing `config.py`:

- **System Prompt**: Change how the AI teacher behaves
- **Learning Levels**: Adjust level descriptions
- **Learning Modes**: Add or modify learning modes

## 📁 Project Structure

```
english-teacher-agent/
├── app.py                 # Main Streamlit application
├── english_teacher.py     # Core AI teacher logic
├── config.py             # Configuration and settings
├── run.py                # Application runner script
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables template
└── README.md            # This file
```

## 🔧 Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **OpenAI**: GPT API integration
- **python-dotenv**: Environment variable management
- **Pydantic**: Data validation

### API Usage

The application uses OpenAI's GPT-3.5-turbo model for:
- Generating teacher responses
- Analyzing user input for corrections
- Providing learning feedback
- Creating session summaries

### Cost Considerations

- Each conversation exchange uses approximately 500-1000 tokens
- Estimated cost: $0.001-0.002 per conversation exchange
- Monitor your OpenAI usage in the [OpenAI Dashboard](https://platform.openai.com/usage)

## 🎓 Learning Tips

1. **Be Consistent**: Practice regularly for best results
2. **Don't Fear Mistakes**: The AI teacher is designed to be encouraging
3. **Ask Questions**: The more you engage, the more you'll learn
4. **Use Examples**: Try the example prompts for each mode
5. **Review Feedback**: Pay attention to corrections and explanations
6. **Track Progress**: Use session summaries to see your improvement

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Make sure your `.env` file exists and contains a valid API key
   - Check that the key doesn't have extra spaces or quotes

2. **"Module not found" errors**
   - Run `pip install -r requirements.txt` to install dependencies

3. **App won't start**
   - Check that port 8501 is available
   - Try running `streamlit run app.py` directly

4. **API errors**
   - Verify your OpenAI API key is valid and has credits
   - Check your internet connection

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your OpenAI API key and account status
3. Ensure all dependencies are installed correctly
4. Check that your Python version is 3.8 or higher

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new learning modes
- Improving the UI/UX
- Adding more language levels
- Enhancing the AI prompts
- Adding new features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- Streamlit for the excellent web framework
- The open-source community for inspiration and tools

---

**Happy Learning! 🎉**

Start your English learning journey with your new AI teacher. Remember, practice makes perfect!
