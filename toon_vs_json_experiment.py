import os
import json
from datetime import datetime
from google import genai
from google.genai.errors import APIError
from toon_py import encode
from typing import List, Dict, Any

# --- CONFIGURATION ---
GEMINI_MODEL = 'gemini-2.5-flash'

# 2. Define the Prompt Components
system_instruction = "You are an expert data analyst. The following data is a list of customer records in [FORMAT]. Analyze the data and report any anomalies. Use the data provided only."
user_query = "Please calculate the total number of orders from active users in NYC."

# --- DATA GENERATION FUNCTIONS ---
def generate_simple_records(count: int) -> List[Dict[str, Any]]:
    """Generate simple flat records (best case for TOON - highly repetitive)."""
    return [
        {"id": i, "user_name": f"User_{i}", "city": ["NYC", "LA", "Chicago", "Boston"][i % 4], 
         "status": "Active" if i % 3 != 0 else "Inactive", "orders": i * 5}
        for i in range(count)
    ]

def generate_complex_records(count: int) -> List[Dict[str, Any]]:
    """Generate complex nested records with arrays and objects."""
    cities = ["NYC", "LA", "Chicago", "Boston", "Seattle", "Miami", "Austin", "Denver"]
    statuses = ["Active", "Inactive", "Pending", "Suspended"]
    products = ["Widget", "Gadget", "Tool", "Device", "Appliance"]
    
    return [
        {
            "id": i,
            "user_name": f"User_{i}",
            "profile": {
                "city": cities[i % len(cities)],
                "state": ["NY", "CA", "IL", "MA", "WA", "FL", "TX", "CO"][i % 8],
                "zipcode": f"{10000 + (i * 123) % 90000}",
                "age": 25 + (i % 50)
            },
            "status": statuses[i % len(statuses)],
            "orders": [
                {"order_id": f"ORD-{i}-{j}", "product": products[j % len(products)], "quantity": (i + j) % 10 + 1, "price": round((i + j) * 12.5, 2)}
                for j in range((i % 5) + 1)
            ],
            "metadata": {
                "created_at": f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
                "last_login": f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
                "tags": [f"tag_{j}" for j in range(i % 3)]
            }
        }
        for i in range(count)
    ]

def generate_unique_records(count: int) -> List[Dict[str, Any]]:
    """Generate records with mostly unique values (worst case for TOON)."""
    return [
        {
            "id": i,
            "user_name": f"UniqueUser_{i}_Company_{i * 7}",
            "city": f"City_{i % 50}",
            "status": f"Status_{i % 10}",
            "orders": i * 7 + (i % 13),
            "description": f"Unique description for user {i} with special characteristics {i * 3}"
        }
        for i in range(count)
    ]

def generate_tabular_records(count: int) -> List[Dict[str, Any]]:
    """Generate highly repetitive tabular data (best case for TOON - like CSV/database)."""
    categories = ["Electronics", "Clothing", "Food", "Books", "Toys"]
    regions = ["North", "South", "East", "West"]
    statuses = ["Pending", "Shipped", "Delivered"]
    
    return [
        {
            "product_id": f"PROD-{(i % 1000):04d}",
            "category": categories[i % len(categories)],
            "region": regions[i % len(regions)],
            "status": statuses[i % len(statuses)],
            "quantity": (i % 20) + 1,
            "price": round(10.99 + (i % 100), 2),
            "discount": 0.1 if i % 5 == 0 else 0.0
        }
        for i in range(count)
    ]

def generate_api_response_records(count: int) -> List[Dict[str, Any]]:
    """Generate API response-like data with common fields."""
    status_codes = [200, 201, 400, 404, 500]
    methods = ["GET", "POST", "PUT", "DELETE"]
    content_types = ["application/json", "text/html", "application/xml"]
    
    return [
        {
            "timestamp": f"2024-01-{(i % 28) + 1:02d}T10:{(i % 60):02d}:00Z",
            "method": methods[i % len(methods)],
            "endpoint": f"/api/v1/users/{i % 100}",
            "status_code": status_codes[i % len(status_codes)],
            "content_type": content_types[i % len(content_types)],
            "response_time_ms": (i % 1000) + 50,
            "success": status_codes[i % len(status_codes)] < 400
        }
        for i in range(count)
    ]

def generate_mixed_types_records(count: int) -> List[Dict[str, Any]]:
    """Generate records with various data types including nulls, booleans, dates."""
    return [
        {
            "id": i,
            "name": f"Item_{i}" if i % 10 != 0 else None,  # Some nulls
            "active": i % 2 == 0,  # Booleans
            "score": round((i * 1.5) % 100, 2) if i % 3 != 0 else None,  # Null numbers
            "tags": ["tag1", "tag2"] if i % 2 == 0 else [],  # Empty arrays
            "metadata": {"key": "value"} if i % 5 == 0 else None,  # Null objects
            "created_at": f"2024-{(i % 12) + 1:02d}-15T00:00:00Z"
        }
        for i in range(count)
    ]

def generate_large_field_records(count: int) -> List[Dict[str, Any]]:
    """Generate records with large text fields (like descriptions, content)."""
    return [
        {
            "id": i,
            "title": f"Document {i}",
            "content": f"This is a long document content for item {i}. " * 10,  # Repeated text
            "author": f"Author_{i % 10}",  # Some repetition
            "category": ["Tech", "Science", "Art", "History"][i % 4],
            "word_count": (i * 100) % 5000
        }
        for i in range(count)
    ]

# --- FUNCTIONS ---
def prepare_prompt(data_format: str, data_payload: str) -> str:
    """Combines the instruction, query, and data into a single prompt string."""
    instruction = system_instruction.replace("[FORMAT]", data_format)
    return f"{instruction}\n\n[START_DATA_{data_format}]\n{data_payload}\n[END_DATA_{data_format}]\n\n{user_query}"

def count_tokens(client: genai.Client, prompt_text: str) -> int:
    """Counts the tokens for a given prompt string using the Gemini API."""
    try:
        response = client.models.count_tokens(
            model=GEMINI_MODEL,
            contents=[prompt_text]
        )
        return response.total_tokens
    except APIError as e:
        print(f"An API error occurred: {e}")
        return 0

def run_experiment(client: genai.Client, data: list, scenario_name: str = "Experiment") -> Dict[str, Any]:
    """Encodes data, counts tokens, and reports savings. Returns results dict."""
    
    # --- JSON ENCODING (Baseline) ---
    json_data = json.dumps(data, separators=(',', ':'))
    json_prompt = prepare_prompt("JSON", json_data)
    t_json = count_tokens(client, json_prompt)

    # --- TOON ENCODING (Optimized) ---
    toon_data = encode(data)
    toon_prompt = prepare_prompt("TOON", toon_data)
    t_toon = count_tokens(client, toon_prompt)

    # Calculate metrics
    tokens_saved = t_json - t_toon if t_json > 0 and t_toon > 0 else 0
    percentage_reduction = (tokens_saved / t_json * 100) if t_json > 0 else 0
    
    results = {
        "scenario": scenario_name,
        "record_count": len(data),
        "json_tokens": t_json,
        "toon_tokens": t_toon,
        "tokens_saved": tokens_saved,
        "percentage_reduction": percentage_reduction,
        "json_size": len(json_data),
        "toon_size": len(toon_data)
    }
    
    return results

def print_experiment_results(results: Dict[str, Any], show_payloads: bool = False):
    """Prints formatted results for a single experiment."""
    print(f"\n{'='*70}")
    print(f"Scenario: {results['scenario']}")
    print(f"{'='*70}")
    print(f"Records: {results['record_count']}")
    print(f"JSON Tokens: {results['json_tokens']:,}")
    print(f"TOON Tokens: {results['toon_tokens']:,}")
    print(f"Tokens Saved: {results['tokens_saved']:,}")
    print(f"Percentage Reduction: {results['percentage_reduction']:.2f}%")
    print(f"JSON Size (bytes): {results['json_size']:,}")
    print(f"TOON Size (bytes): {results['toon_size']:,}")
    print(f"Size Reduction: {results['json_size'] - results['toon_size']:,} bytes ({((results['json_size'] - results['toon_size']) / results['json_size'] * 100):.2f}%)")

def run_comprehensive_tests(client: genai.Client):
    """Runs multiple test scenarios with different data sizes and types."""
    
    print("\n" + "="*70)
    print("COMPREHENSIVE TOON vs JSON TOKEN EFFICIENCY EXPERIMENT")
    print(f"Model: {GEMINI_MODEL}")
    print("="*70)
    
    all_results = []
    
    # Test configurations: (size, data_type, name)
    test_configs = [
        # Scalability tests - Simple records
        (20, "simple", "Small Dataset - Simple Records"),
        (100, "simple", "Medium Dataset - Simple Records"),
        (500, "simple", "Large Dataset - Simple Records"),
        (1000, "simple", "Very Large Dataset - Simple Records"),
        
        # Complexity tests
        (50, "complex", "Medium Dataset - Complex Nested Records"),
        (200, "complex", "Large Dataset - Complex Nested Records"),
        
        # Edge cases
        (100, "unique", "Medium Dataset - Unique Records (Worst Case)"),
        (150, "tabular", "Medium Dataset - Tabular/CSV-like Data (Best Case)"),
        (100, "api_response", "Medium Dataset - API Response Data"),
        (80, "mixed_types", "Medium Dataset - Mixed Types (Nulls, Booleans)"),
        (60, "large_fields", "Medium Dataset - Large Text Fields"),
    ]
    
    for size, data_type, name in test_configs:
        print(f"\n⏳ Running: {name} ({size} records)...")
        
        # Generate data based on type
        if data_type == "simple":
            data = generate_simple_records(size)
        elif data_type == "complex":
            data = generate_complex_records(size)
        elif data_type == "unique":
            data = generate_unique_records(size)
        elif data_type == "tabular":
            data = generate_tabular_records(size)
        elif data_type == "api_response":
            data = generate_api_response_records(size)
        elif data_type == "mixed_types":
            data = generate_mixed_types_records(size)
        elif data_type == "large_fields":
            data = generate_large_field_records(size)
        else:
            data = generate_simple_records(size)
        
        results = run_experiment(client, data, name)
        all_results.append(results)
        print_experiment_results(results)
    
    # Summary Analysis
    print("\n" + "="*70)
    print("SUMMARY ANALYSIS")
    print("="*70)
    
    print("\n--- Token Savings by Dataset Size (Simple Records) ---")
    simple_results = [r for r in all_results if "Simple Records" in r['scenario']]
    for r in sorted(simple_results, key=lambda x: x['record_count']):
        print(f"  {r['record_count']:4d} records: {r['tokens_saved']:6,} tokens saved ({r['percentage_reduction']:5.2f}%)")
    
    print("\n--- Token Savings by Data Complexity (Medium Size ~100 records) ---")
    medium_results = [r for r in all_results if r['record_count'] in [50, 100]]
    for r in sorted(medium_results, key=lambda x: x['scenario']):
        print(f"  {r['scenario']:50s}: {r['tokens_saved']:6,} tokens ({r['percentage_reduction']:5.2f}%)")
    
    print("\n--- Scalability Analysis ---")
    if len(simple_results) >= 2:
        first = simple_results[0]
        last = simple_results[-1]
        size_ratio = last['record_count'] / first['record_count']
        savings_ratio = last['tokens_saved'] / first['tokens_saved'] if first['tokens_saved'] > 0 else 0
        print(f"  Size increase: {size_ratio:.1f}x ({first['record_count']} → {last['record_count']} records)")
        print(f"  Savings increase: {savings_ratio:.1f}x ({first['tokens_saved']:,} → {last['tokens_saved']:,} tokens)")
        print(f"  Savings scale linearly: {'✓ YES' if abs(savings_ratio - size_ratio) < size_ratio * 0.2 else '✗ NO (may indicate overhead)'}")
    
    print("\n--- Best and Worst Cases ---")
    best = max(all_results, key=lambda x: x['percentage_reduction'])
    worst = min([r for r in all_results if r['tokens_saved'] > 0], key=lambda x: x['percentage_reduction'], default=None)
    print(f"  Best savings: {best['scenario']} - {best['percentage_reduction']:.2f}% reduction")
    if worst:
        print(f"  Worst savings: {worst['scenario']} - {worst['percentage_reduction']:.2f}% reduction")
    
    total_saved = sum(r['tokens_saved'] for r in all_results)
    print(f"\n  Total tokens saved across all tests: {total_saved:,}")
    
    # Save results to JSON file for UI
    output_data = {
        "model": GEMINI_MODEL,
        "timestamp": datetime.now().isoformat(),
        "total_tokens_saved": total_saved,
        "results": all_results
    }
    
    results_file = "experiment_results.json"
    with open(results_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    print(f"🌐 Open 'results_dashboard.html' in your browser to view the results!")
    
    return all_results

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Set it with: export GEMINI_API_KEY='your-key-here'")
    else:
        client = genai.Client()
        # Run comprehensive tests with multiple scenarios
        results = run_comprehensive_tests(client)
        print("\n✅ Experiment complete!")

