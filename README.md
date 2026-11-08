# TOON vs JSON Experiment

These Python scripts measure how many LLM tokens the TOON format saves compared to JSON.

## What it does

- The scripts make test data for many scenarios, for example tables, logs, product catalogs, and image prompts.
- The scripts encode each data set in compact JSON and in TOON.
- The scripts count the tokens of each version with the Gemini API `count_tokens` method.
- The scripts calculate the saved tokens and the percentage reduction.
- The scripts write the results to JSON files.
- A web dashboard shows the results.
- A stability benchmark compares five formats (JSON, TOON, YAML, CSV, XML). It checks that Gemini gives the same answer for each format.

The repository contains the results of an earlier run. You can see these results without an API key.

## Requirements

- macOS, Linux, or Windows.
- Python 3.10 or later.
- A Google Gemini API key. Get a key at <https://aistudio.google.com/apikey>.
- A web browser for the dashboard.

## Install

1. Get the code.

   ```bash
   git clone https://github.com/Ikarus0013/toon-vs-json-experiment.git
   cd toon-vs-json-experiment
   ```

2. Make a virtual environment.

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment.

   ```bash
   source venv/bin/activate
   ```

4. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

## Configure

The scripts read the API key from the environment. They do not read a `.env` file.

| Variable | Required | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | Yes, for the experiment scripts | Your Google Gemini API key. |

Set the variable in your shell.

```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

The model is `gemini-2.5-flash`. To use a different model, change `GEMINI_MODEL` at the top of each script.

## Use

### Show the saved results

1. Start the dashboard server.

   ```bash
   python view_results.py
   ```

2. Your browser opens `http://localhost:8000/results_dashboard.html`. If it does not open, type this address.
3. Push `Ctrl+C` in the terminal to stop the server.

### Run the experiments

1. Run all 15 experiment types (31 scenarios).

   ```bash
   python all_experiments.py
   ```

   The script writes `all_experiments_results.json`.

2. Optionally, run the data analysis experiments only.

   ```bash
   python toon_vs_json_experiment.py
   ```

   The script writes `experiment_results.json`.

3. Optionally, run the image prompt experiments only.

   ```bash
   python image_generation_experiment.py
   ```

   The script writes `image_generation_results.json`.

4. Start the dashboard again to see the new results.

   ```bash
   python view_results.py
   ```

### Compare simple and nested records (no API key)

1. Run this script. It shows JSON and TOON side by side.

   ```bash
   python explain_complex_records.py
   ```

### Run the stability benchmark

**CAUTION:** This script sends `generate_content` requests to Gemini. These requests use your quota and can cost money.

**CAUTION:** This script replaces `all_experiments_results.json` with a summary. Make a copy of the file first if you want to keep it.

1. Run the benchmark.

   ```bash
   python stability-benchmark.py
   ```

2. Open `stability_dashboard.html` through the dashboard server to see the results.

## How it works

1. Each script makes test data with Python functions.
2. JSON uses `json.dumps` with compact separators.
3. TOON uses `encode()` from the `toon_py` package.
4. The scripts put each version into the same prompt text.
5. `client.models.count_tokens()` gives the token count of each prompt.
6. The scripts calculate `tokens_saved = json_tokens - toon_tokens` and the reduction in percent.

Result of the saved run (`all_experiments_results.json`): 31 scenarios, 92,600 tokens saved, 25.4 % overall reduction, 20.3 % average reduction.

## Files

| File | Description |
| --- | --- |
| `all_experiments.py` | All 15 experiment types in one script. |
| `toon_vs_json_experiment.py` | Data analysis experiments: scale, nesting, and special cases. |
| `image_generation_experiment.py` | Image prompt experiments: batches, styles, and scene layouts. |
| `stability-benchmark.py` | Token count and answer stability for JSON, TOON, YAML, CSV, and XML. |
| `explain_complex_records.py` | Shows simple and nested records in JSON and TOON. No API calls. |
| `view_results.py` | Local web server for the dashboard on port 8000. |
| `results_dashboard.html` | Dashboard that reads the result JSON files. |
| `*_results.json` | Results of the earlier run. |
| `EXPERIMENT_IDEAS.md` | More experiment ideas. |
| `requirements.txt` | Python dependencies. |

## Limits

- The token counts come from the Gemini tokenizer. Other LLMs can give different counts.
- The test data is synthetic. Real data can give different results.
- TOON saves the most tokens for flat data with repeated keys. It saves fewer tokens, or none, for deeply nested data.
- The token count measures only the input size. It does not measure answer quality, except in the stability benchmark.
- `view_results.py` stops if `experiment_results.json` does not exist.

## License

This project uses the MIT license. Refer to the `LICENSE` file.
