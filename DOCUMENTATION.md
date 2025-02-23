# Project Documentation

## 1. Project Overview
This project is an AI-supported literature research and analysis system. Its objective is to automatically retrieve and extract information from scientific publications (using the arXiv API) and then use AI to analyze the abstracts to identify the research question, objective, and scientific contribution of each paper. The analyzed data is stored in a CSV file.

## 2. Installation & Setup

### Prerequisites
- **Python Version:** Python 3.11
- **Virtual Environment:** Virtual environment for dependency management.

### Setup Steps

1. **Clone the Repository and Navigate to the Project Folder:**
   ```bash
   git clone https://github.com/abbykabraham/euonair-assessment.git
   cd euonair-assessment
   ```

2. **Create and Activate a Virtual Environment (Windows):**
   ```bash
   python -m venv euenv
   euenv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the API Key**
   - Create a file named `.env` in the project root.
   - Add your OpenAI API key in the following format:
     ```dotenv
     OPENAI_API_KEY=sk-<your_openai_api_key_here>
     ```

5. **Run the Project:**
   ```bash
   python find_lit_source.py
   ```

## 3. Code Structure

- **`find_lit_source.py`**:  
  This module handles literature research and metadata extraction from the arXiv API. It filters results by publication year and saves the raw and analyzed data as CSV files in the `data/` directory.

- **`openai_analysis.py`**:  
  This module uses the OpenAI API (with the GPT-4 model) to analyze research paper abstracts. It extracts the research question, objective, and scientific contribution from the abstract.  
  *Note: Each run using GPT-4 incurs an approximate cost of $0.18.*

- **`tests/`**:  
  This folder contains pytest modules (`test_find.py`) that verify the functionality of the literature search, correct creation of CSV files, and the proper integration of the OpenAI analysis module.

## 4. AI Analysis

- **Model Used**:  
  GPT-4 model

- **Prompt Design**:  
  It instructs the model to extract the research question, objective, and contribution from each abstract.

- **Cost Consideration**:  
  Each run using the GPT-4 model incurs an approximate cost of $0.18.

## 5. Notes

### Version Control
The project is maintained in a dedicated branch on GitHub.

### Dependencies
All dependencies are listed in the `requirements.txt` file.

### Documentation
This documentation, along with the instructor’s README, provides a full overview of the project’s objectives and implementation details.

