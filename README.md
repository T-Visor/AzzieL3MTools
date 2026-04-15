# AzzieL3MTools

LLM evaluation and batch processing framework for comparing language models.

## Overview

AzzieL3MTools provides a web-based interface and command-line tools for running inference tasks against multiple language models with configurable prompts, settings, and batch processing capabilities. Designed for systematic LLM comparison and evaluation.

## Prerequisites

- Python 3.8 or higher
- Ollama (for local model execution) or Ollama API credentials (for cloud models)
- 5GB free disk space minimum

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/davehillman/AzzieL3MTools.git
cd AzzieL3MTools
pip install -r requirements.txt
```

Set up environment variables for cloud model access:

```bash
export OLLAMA_API_KEY="your_api_key_here"
```

## Quick Start

### Web Interface

Launch the web server on port 15000:

```bash
python app.py
```

Access the interface at http://localhost:15000

### Command Line

For single query execution:

```python
from runl3m import rundata
results = rundata(model="llama2", qry="your query", pp="prompt_profile", llmset="settings")
```

## Batch Analysis

Batch analysis enables comparing multiple models against standardized test cases with consistent metrics collection.

### Create a Batch Configuration File


Create the **batch** directory in the root of the project.

```sh
mkdir batch
```

Create a JSON file in the **batch** directory with the batch specification:

```json
{
  "llm": ["model1", "model2", "all_local"],
  "llmsettings": ["Baseline", "HighTemp"],
  "batchrun": [
    {
      "active": "True",
      "type": "definition",
      "qryid": "def_simple",
      "payload": "Your test query here"
    },
    {
      "active": "True",
      "type": "classification",
      "qryid": "class_milintel",
      "payload": "file:path/to/document.txt"
    }
  ],
  "savestats": "True",
  "results": "batchres/batch_results.json"
}
```

### Run Batch Processing

Execute via the web interface:
1. Navigate to http://localhost:15000
2. Select batch configuration file
3. Click "Run Batch"

Or run programmatically:

```python
from runl3m import runproc
results = runproc(llm="", qry="", pp="", llmset="", batch="batchfile.json")
```

### Output

Batch results are saved to the specified results file with metrics including:
- Execution time per model and configuration
- Token counts for input and output
- Full response data
- Payload and result sizes

## Configuration

### Model Settings

Edit `config/llminit.json` to configure:
- Model temperature and context window
- Output format (JSON, text)
- Keep-alive duration

### Prompts and Templates

Modify `config/llmprompts.json` to define:
- System prompts
- Processing types (word, line, document, json)
- Query identifiers for batch operations

## Project Structure

- `app.py` - Flask web application
- `runl3m.py` - Core LLM execution and batch processing
- `llmproc.py` - Model management and lifecycle
- `parse.py` - Text parsing utilities
- `utils.py` - File I/O and helper functions
- `jsonfix.py` - JSON parsing and repair
- `config/` - Configuration files for models, settings, and prompts
- `batchres/` - Batch result outputs
- `templates/` - HTML interface templates
- `static/` - Client-side assets

## Key Features

- Multi-model evaluation framework
- Configurable preprocessing and prompt templates
- Batch processing with statistical collection
- Cloud and local model support
- Web interface and programmatic API
- JSON output formatting and repair
- Token counting and performance metrics
