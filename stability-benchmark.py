#!/usr/bin/env python3
"""
KATALYST STABILITY AND EFFICIENCY BENCHMARK
===========================================
This script runs a single, highly-tabular dataset (best-case scenario for TOON) 
against five common data formats (JSON, TOON, YAML, CSV, XML).

It measures:
1. Token Efficiency (Token Count for all 5 formats).
2. System Stability (Verifies that the LLM's analytical output is identical 
   across all formats, proving compression does not equal comprehension loss).

Dependencies: google-genai, pyyaml (often built-in to execution environments)
"""
import os
import json
import yaml
from typing import List, Dict, Any, Tuple
from google import genai
from google.genai.errors import APIError
from toon_py import encode # Assuming 'toon_py' is available
from datetime import datetime

# --- CONFIGURATION ---
GEMINI_MODEL = 'gemini-2.5-flash'
TARGET_DATA_SIZE = 25 # Number of records to test

# ============================================================================
# 1. FORMAT CONVERTERS (Minimalist for cross-format comparison)
# ============================================================================

def format_to_json(data: Any) -> str:
    """Converts to compact JSON (lowest JSON token cost)."""
    return json.dumps(data, separators=(',', ':'))

def format_to_yaml(data: Any) -> str:
    """Converts to YAML."""
    try:
        # Use pyyaml's safe dump
        return yaml.safe_dump(data, default_flow_style=False)
    except NameError:
        # Fallback if yaml library is not installed
        return f"YAML_FALLBACK: {json.dumps(data, indent=2)}"

def format_to_csv(data: List[Dict[str, Any]]) -> str:
    """Converts a flat list of dicts to CSV string."""
    if not data: return ""
    
    # Simple, comma-separated header row
    header = ",".join(data[0].keys())
    
    # Simple data rows
    rows = [",".join(str(v) for v in record.values()) for record in data]
    
    return header + "\n" + "\n".join(rows)

def format_to_xml(data: List[Dict[str, Any]]) -> str:
    """Converts a flat list of dicts to a simple XML string."""
    if not data: return "<records/>"
    
    xml_parts = ['<records>']
    for record in data:
        xml_parts.append('  <record>')
        for key, value in record.items():
            xml_parts.append(f'    <{key}>{value}</{key}>')
        xml_parts.append('  </record>')
    xml_parts.append('</records>')
    return "\n".join(xml_parts)

def format_data(data: List[Dict[str, Any]], format_type: str) -> str:
    """Routes data to the correct encoder."""
    if format_type == 'JSON':
        return format_to_json(data)
    elif format_type == 'TOON':
        return encode(data)
    elif format_type == 'YAML':
        return format_to_yaml(data)
    elif format_type == 'CSV':
        return format_to_csv(data)
    elif format_type == 'XML':
        return format_to_xml(data)
    return ""

# ============================================================================
# 2. DATA GENERATION & PROMPT DEFINITION
# ============================================================================

def generate_tabular_records(count: int) -> List[Dict[str, Any]]:
    """Generates highly tabular, best-case data for TOON/CSV."""
    departments = ["Engineering", "Sales", "Marketing", "Support"]
    status = ["Active", "Inactive"]
    
    return [
        {
            "id": i,
            "name": f"Employee {i}",
            "dept": departments[i % len(departments)],
            "status": status[i % len(status)],
            "salary": round(50000 + (i * 123) % 50000, 2),
            "projects": (i % 5) + 1,
            "hire_year": 2020 + (i % 5),
            "remote": i % 2 == 0
        }
        for i in range(count)
    ]

def get_core_prompt(format_type: str) -> Tuple[str, str]:
    """Returns the System Instruction and User Query for the stability test."""
    
    system_instruction = (
        f"You are a stable, deterministic data processing engine. The user will provide employee data in the {format_type} format. "
        f"Your task is to analyze it, provide the requested information, and nothing else."
    )
    
    user_query = (
        "Based on the provided data, calculate the following and output the result ONLY as a JSON dictionary: "
        "1. Total count of 'Active' employees. 2. The average 'salary' of the 'Engineering' department. "
        "3. The count of employees hired in year 2024. "
        "Provide ONLY the final JSON object."
    )
    
    return system_instruction, user_query

def construct_full_prompt(data_payload: str, system_instruction: str, user_query: str) -> str:
    """Assembles the final string sent to the LLM."""
    return f"SYSTEM INSTRUCTION: {system_instruction}\n\nDATA PAYLOAD:\n{data_payload}\n\nUSER QUERY:\n{user_query}"

# ============================================================================
# 3. EXPERIMENT EXECUTION
# ============================================================================

def run_stability_experiment(client: genai.Client, format_a: str, format_b: str, data: List[Dict]) -> Dict[str, Any]:
    """Tests token efficiency and stability between two formats.
    Returns a rich result payload including prompts, tokens, and output snippets."""
    
    results = {"comparison": f"{format_a} vs {format_b}"}
    
    # 1. Prepare Payloads and Count Tokens
    payloads = {}
    for fmt in [format_a, format_b]:
        data_string = format_data(data, fmt)
        system_inst, user_query = get_core_prompt(fmt)
        full_prompt = construct_full_prompt(data_string, system_inst, user_query)
        resp = client.models.count_tokens(model=GEMINI_MODEL, contents=[full_prompt])
        t_count = getattr(resp, "total_tokens", 0)
        payloads[fmt] = {
            "prompt": full_prompt,
            "data_string": data_string,
            "system_instruction": system_inst,
            "user_query": user_query,
            "tokens": t_count
        }

    # 2. Get LLM Responses (Stability Check)
    llm_outputs = {}
    for fmt in [format_a, format_b]:
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[payloads[fmt]["prompt"]],
                config=genai.types.GenerateContentConfig(temperature=0.0) # Ensure deterministic output
            )
            raw_text = response.text or ""
            normalized = raw_text.strip().replace("```json", "").replace("```", "").replace("\n", "").replace(" ", "")
            llm_outputs[fmt] = {"raw": raw_text, "normalized": normalized}
        except APIError as e:
            print(f"Error fetching response for {fmt}: {e}")
            llm_outputs[fmt] = {"raw": "ERROR", "normalized": "ERROR"}
            
    # 3. Analyze Results
    t_a = payloads[format_a]["tokens"]
    t_b = payloads[format_b]["tokens"]
    
    if t_a > t_b:
        token_savings_pct = (t_a - t_b) / t_a * 100
        winner = format_b
    elif t_b > t_a:
        token_savings_pct = (t_b - t_a) / t_b * 100
        winner = format_a
    else:
        token_savings_pct = 0.0
        winner = "TIE"
        
    stability_check = llm_outputs[format_a]["normalized"] == llm_outputs[format_b]["normalized"]
    stability_reason = "MATCH = identical normalized outputs" if stability_check else "FAIL = different outputs after normalization"
    
    results.update({
        "format_a": format_a,
        "format_b": format_b,
        "tokens_A": t_a,
        "tokens_B": t_b,
        "savings_A_vs_B_pct": token_savings_pct if t_a > t_b else -token_savings_pct,
        "efficiency_winner": winner,
        "stability_check": stability_check,
        "stability_reason": stability_reason,
        "output_hash_A": llm_outputs[format_a]["normalized"][:50],
        "output_hash_B": llm_outputs[format_b]["normalized"][:50],
        "output_snippet_A": (llm_outputs[format_a]["raw"] or "")[:400],
        "output_snippet_B": (llm_outputs[format_b]["raw"] or "")[:400],
        "prompt_A": payloads[format_a]["prompt"][:1500],
        "prompt_B": payloads[format_b]["prompt"][:1500],
        "data_A_start": payloads[format_a]["data_string"][:500],
        "data_B_start": payloads[format_b]["data_string"][:500]
    })
    
    return results

def run_all_stability_tests(client: genai.Client):
    """Executes the 9 required comparative stability tests, prints rich context,
    and exports results for a web dashboard."""
    
    print("\n" + "="*90)
    print("KATALYST STABILITY & EFFICIENCY BENCHMARK (9-POINT TEST)")
    print(f"Model: {GEMINI_MODEL} | Records: {TARGET_DATA_SIZE} | Data Type: Highly Tabular")
    print("="*90)
    print("\nLegend:")
    print("- Token A/B: Input tokens for full prompt when using format A/B.")
    print("- Savings (A vs B): Positive = A uses fewer tokens; Negative = B uses fewer.")
    print("- Winner: Format with fewer tokens (input cost).")
    print("- Stability: MATCH means outputs identical (after normalization); FAIL means they differ.\n")
    
    data = generate_tabular_records(TARGET_DATA_SIZE)
    all_formats = ['JSON', 'TOON', 'YAML', 'CSV', 'XML']
    
    # Define the 9 required comparisons
    comparison_pairs = [
        ('TOON', 'JSON'),
        ('TOON', 'CSV'),
        ('TOON', 'YAML'),
        ('TOON', 'XML'),
        ('JSON', 'YAML'),
        ('JSON', 'CSV'),
        ('YAML', 'CSV'),
        ('JSON', 'XML'),
        # Add a full run test to ensure all 5 outputs match a control
        ('JSON', 'XML') # placeholder, will check stability of all 5 against JSON control below
    ]
    
    final_results = []
    toon_json_result = None
    
    header = f"| {'Comparison':<17} | {'Token A':<10} | {'Token B':<10} | {'Savings (A vs B)':<20} | {'Winner':<10} | {'Stability':<10} |"
    print(header)
    print("-" * len(header))
    
    for pair in comparison_pairs:
        fmt_a, fmt_b = pair
        
        # Skip the final pair, will execute the full check
        if fmt_a == 'JSON' and fmt_b == 'XML' and pair == comparison_pairs[-1]:
            continue 

        results = run_stability_experiment(client, fmt_a, fmt_b, data)
        if fmt_a == 'TOON' and fmt_b == 'JSON':
            toon_json_result = results
        
        savings_str = f"{results['savings_A_vs_B_pct']:+.2f}%" if results['savings_A_vs_B_pct'] != 0 else "0.00%"
        stability_str = "MATCH" if results['stability_check'] else "FAIL ❌"
        
        print(f"| {fmt_a} vs {fmt_b:<9} | {results['tokens_A']:<10} | {results['tokens_B']:<10} | {savings_str:<20} | {results['efficiency_winner']:<10} | {stability_str:<10} |")
        print(f"  ├─ Reason: {results['stability_reason']}")
        print(f"  ├─ Output A hash: {results['output_hash_A']}")
        print(f"  ├─ Output B hash: {results['output_hash_B']}")
        print(f"  ├─ Output A snippet: {results['output_snippet_A'][:200]}{'...' if len(results['output_snippet_A'])>200 else ''}")
        print(f"  └─ Output B snippet: {results['output_snippet_B'][:200]}{'...' if len(results['output_snippet_B'])>200 else ''}\n")
        final_results.append(results)
    
    print("-" * len(header))
    
    # 9. Stability Test Across All 5 Formats (The Ultimate Proof)
    print("\n\n*** 9. COMPREHENSIVE OUTPUT STABILITY TEST (All 5 Formats) ***")
    
    control_output = None
    all_match = True
    control_fmt = "JSON"
    
    for fmt in all_formats:
        data_string = format_data(data, fmt)
        system_inst, user_query = get_core_prompt(fmt)
        full_prompt = construct_full_prompt(data_string, system_inst, user_query)
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[full_prompt],
            config=genai.types.GenerateContentConfig(temperature=0.0)
        )
        
        raw_output = (response.text or "").strip().replace("```json", "").replace("```", "").replace("\n", "").replace(" ", "")

        if control_output is None:
            control_output = raw_output
            print(f"[{fmt} Control]: Hash created. (First 50 chars: {control_output[:50]}...)")
            control_fmt = fmt
            continue
        
        is_match = raw_output == control_output
        if not is_match:
            all_match = False

        print(f"[{fmt} Test]: {'MATCH' if is_match else 'FAIL ❌'}")
    
    print("-" * 90)
    print(f"OVERALL STABILITY RESULT: {'PASS ✅ (All 5 formats yielded identical analysis)' if all_match else 'FAIL ❌ (At least one format resulted in different output)'}")
    print("=" * 90)

    # ---- Export a dashboard-compatible summary (TOON vs JSON only) ----
    if toon_json_result is not None:
        json_tokens = toon_json_result['tokens_B']  # JSON is B in TOON vs JSON
        toon_tokens = toon_json_result['tokens_A']  # TOON is A in TOON vs JSON
        tokens_saved = max(0, json_tokens - toon_tokens)
        perc_reduction = (tokens_saved / json_tokens * 100) if json_tokens > 0 else 0.0

        dashboard_payload = {
            "model": GEMINI_MODEL,
            "timestamp": datetime.now().isoformat(),
            "total_tokens_saved": tokens_saved,
            "results": [
                {
                    "scenario": f"Stability Benchmark - TOON vs JSON (N={TARGET_DATA_SIZE})",
                    "record_count": TARGET_DATA_SIZE,
                    "json_tokens": json_tokens,
                    "toon_tokens": toon_tokens,
                    "tokens_saved": tokens_saved,
                    "percentage_reduction": perc_reduction,
                    "json_size": 0,
                    "toon_size": 0,
                    "experiment_type": "stability_benchmark"
                }
            ]
        }
        with open("all_experiments_results.json", "w") as f:
            json.dump(dashboard_payload, f, indent=2)
        print(f"\n📊 Summary saved to: all_experiments_results.json (for existing dashboard)")

    # ---- Export full stability results for a dedicated stability dashboard ----
    full_results = {
        "model": GEMINI_MODEL,
        "timestamp": datetime.now().isoformat(),
        "record_count": TARGET_DATA_SIZE,
        "comparisons": final_results,
        "overall_stability_pass": all_match,
        "control_format": control_fmt
    }
    with open("stability_benchmark_results.json", "w") as f:
        json.dump(full_results, f, indent=2)
    print("🧪 Full results saved to: stability_benchmark_results.json")

    # ---- Emit a simple, self-contained HTML dashboard for stability results ----
    stability_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Stability & Efficiency Benchmark</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:#111827; color:#e5e7eb; margin:0; padding:24px; }
    .container { max-width: 1200px; margin: 0 auto; }
    h1 { margin: 0 0 10px 0; }
    .sub { color:#9ca3af; margin-bottom:20px; }
    .grid { display:grid; gap:16px; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); }
    .card { background:#1f2937; border-radius:10px; padding:16px; border:1px solid #374151; }
    .badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; }
    .ok { background:#065f46; color:#d1fae5; }
    .fail { background:#7f1d1d; color:#fecaca; }
    .row { display:flex; justify-content:space-between; margin:6px 0; font-size:14px; }
    code, pre { background:#111827; color:#e5e7eb; padding:10px; display:block; border-radius:8px; overflow:auto; border:1px solid #374151; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace; }
    .small { font-size:12px; color:#9ca3af; }
    .title { font-weight:600; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Stability & Efficiency Benchmark</h1>
    <div class="sub" id="meta">Loading...</div>
    <div id="summary" class="card" style="margin-bottom:16px;"></div>
    <div id="grid" class="grid"></div>
  </div>
  <script>
    async function load() {
      try {
        const res = await fetch('stability_benchmark_results.json');
        const data = await res.json();
        document.getElementById('meta').textContent = `Model: ${data.model} | Records: ${data.record_count} | ${new Date(data.timestamp).toLocaleString()}`;
        const summary = document.getElementById('summary');
        summary.innerHTML = `
          <div class="row"><span class="title">Overall Stability</span>
            <span><span class="badge ${data.overall_stability_pass ? 'ok' : 'fail'}">${data.overall_stability_pass ? 'PASS' : 'FAIL'}</span></span>
          </div>
          <div class="row"><span class="title">Control Format</span><span>${data.control_format}</span></div>
          <div class="small">MATCH means identical outputs after normalization (stripping fences/whitespace). FAIL means outputs differ.</div>
        `;
        const grid = document.getElementById('grid');
        grid.innerHTML = '';
        data.comparisons.forEach(c => {
          const card = document.createElement('div');
          card.className = 'card';
          card.innerHTML = `
            <div class="row"><span class="title mono">${c.comparison}</span>
              <span class="badge ${c.stability_check ? 'ok' : 'fail'}">${c.stability_check ? 'MATCH' : 'FAIL'}</span>
            </div>
            <div class="row"><span>Tokens (A)</span><span>${c.tokens_A.toLocaleString()}</span></div>
            <div class="row"><span>Tokens (B)</span><span>${c.tokens_B.toLocaleString()}</span></div>
            <div class="row"><span>Savings (A vs B)</span><span>${(c.savings_A_vs_B_pct).toFixed(2)}%</span></div>
            <div class="row"><span>Efficiency Winner</span><span>${c.efficiency_winner}</span></div>
            <div class="row"><span>Output A hash</span><span class="mono small">${c.output_hash_A}</span></div>
            <div class="row"><span>Output B hash</span><span class="mono small">${c.output_hash_B}</span></div>
            <div class="small" style="margin:8px 0;">Output A snippet</div>
            <pre class="mono">${(c.output_snippet_A || '').replace(/</g,'&lt;')}</pre>
            <div class="small" style="margin:8px 0;">Output B snippet</div>
            <pre class="mono">${(c.output_snippet_B || '').replace(/</g,'&lt;')}</pre>
            <div class="small" style="margin:8px 0;">Prompt A (start)</div>
            <pre class="mono">${(c.prompt_A || '').replace(/</g,'&lt;')}</pre>
            <div class="small" style="margin:8px 0;">Prompt B (start)</div>
            <pre class="mono">${(c.prompt_B || '').replace(/</g,'&lt;')}</pre>
          `;
          grid.appendChild(card);
        });
      } catch (e) {
        document.getElementById('meta').textContent = 'Failed to load results. Run stability-benchmark.py first.';
      }
    }
    load();
  </script>
</body>
</html>
"""
    with open("stability_dashboard.html", "w") as f:
        f.write(stability_html)
    print("🌐 Stability dashboard written to: stability_dashboard.html (open in browser)")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Set it with: export GEMINI_API_KEY='your-key-here'")
    else:
        try:
            client = genai.Client()
            run_all_stability_tests(client)
        except Exception as e:
            print(f"\nFatal error during execution: {e}")