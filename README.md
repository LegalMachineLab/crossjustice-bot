# ALEXChat: a Generative - Symbolic Approach to Legal eXplainability

This repository contains the support material for the paper *ALEXChat: a Generative - Symbolic Approach to Legal eXplainability*.

A running instance of the application is available at:  **[ALEXChat](https://alexchat.streamlit.app/)**  

⚠ **Note**: This instance runs on [Groq](https://groq.com/). If its shared key is rate-limited, enter your own Groq API key in the sidebar.

The deployed app is built from the `release` branch.

## Repository Structure  

### `test/`  
This directory contains the code for the quantitative evaluation of Task 1.  
- **`facts_extraction.py`**: The main script for evaluation.  
  - Requires a valid [Together AI](https://www.together.ai/) API key to function properly.  

### `res/`  
This directory stores evaluation results and datasets.  
- **`extraction/`**: Contains the dataset used for testing, including both complex and single extraction scenarios.
- **`interaction/`**: Contains  a series of examples illustrating user interactions with the application.  
- **`results_temp_*.json`**: JSON files containing results of the extraction at different temperature settings (0.0, 0.3, 0.6, 0.9).

### `src/`  
Contains the main source code.  
- **`prolog/`**: Stores the CrossJustice Prolog sources.  
- **`argumentation/`**: Contains the `arg2p` executable used for conformity evaluation.  
- **`input_facts.py`**: Defines the list of Prolog facts for the CrossJustice system.  
- **`swi_interface.py`**: A Python interface for interacting with the CrossJustice Prolog system.  
- **`app.py`**: The main application containing all the prompts detailed in the paper.

  - To launch the application, run:  
    ```bash
    streamlit run src/app.py
    ```  
  - Enter a [Groq](https://groq.com/) API key and model in the sidebar. The default model is `openai/gpt-oss-120b`; see the [Groq models list](https://console.groq.com/docs/models) for the ones currently available.
  - Alternatively, set a shared key as `GROQ_API_KEY` in `.streamlit/secrets.toml` (never commit it) or in the environment. On Streamlit Community Cloud, put it in the app's *Secrets* settings.

## Setup and Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/LegalMachineLab/crossjustice-bot.git
   cd crossjustice-bot
   ```  
2. Install system dependencies (tested with Debian Bullseye):  
   ```bash
   xargs sudo apt install -y < packages.txt
   ```  
3. Install Python dependencies (tested with Python 3.12):  
   ```bash
   pip install -r requirements.txt
   ```  
4. Set up API keys (**Optional**):
   - Enter your Groq API key in the app sidebar, or set `GROQ_API_KEY` as described above.
   - Add a valid Together AI API key for evaluation (`test/facts_extraction.py`).

5. Run the application:  
   ```bash
   streamlit run src/app.py
   ```  
