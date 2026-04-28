# LLM Hiring Bias Analysis

This project analyzes whether large language models exhibit racial bias in hiring decisions by evaluating identical resumes with different candidate names.

## Setup

1. **Clone and navigate to the project directory**
   ```bash
   cd LLM-Bias-In-Hiring
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`

## Data Preparation

1. **Generate name combinations** (optional - CSV already exists)
   - Open `names_processing.ipynb` in Jupyter
   - Run all cells to create `data/final_name_combinations.csv`

## Running the Analysis

1. **Run batch processing**
   ```bash
   python main.py --start 0 --end 100  # Process first 100 name combinations
   ```

   Options:
   - `--start`: Starting index (0-based)
   - `--end`: Ending index (exclusive)

2. **Merge results** (after all batches complete)
   ```bash
   python merge.py
   ```

## Analysis

- Open `data_analysis.ipynb` in Jupyter
- Run cells to analyze results in `results/merged_results_final.csv`
- View statistical summaries and visualizations

## Output

- Individual batch results: `results/hiring_bias_results_START_END.csv`
- Final merged results: `results/merged_results_final.csv`
- Analysis notebook: `data_analysis.ipynb`

## Requirements

- Python 3.8+
- Groq API key
- Jupyter Notebook (for analysis)</content>
<parameter name="filePath">c:\Users\josep\Documents\ethics\LLM-Bias-In-Hiring\README.md