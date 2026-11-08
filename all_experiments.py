#!/usr/bin/env python3
"""
COMPREHENSIVE TOON vs JSON EXPERIMENT SUITE
===========================================

This file contains ALL experiment scenarios from EXPERIMENT_IDEAS.md:
1. Data Analysis Prompts (existing)
2. Image Generation Prompts
3. Multi-Turn Conversation Contexts
4. API Response Compression
5. Configuration Files & Settings
6. Batch Processing Scenarios
7. Streaming Data Windows
8. Database Query Results
9. Structured Log Analysis
10. Form Data & Surveys
11. E-commerce Product Catalogs
12. Scientific Data & Experiments
13. Code Analysis & ASTs
14. Financial Data & Transactions
15. Healthcare & Medical Records

Run this to test TOON efficiency across all use cases!
"""
import os
import json
from datetime import datetime
from google import genai
from google.genai.errors import APIError
from toon_py import encode
from typing import List, Dict, Any, Union

# --- CONFIGURATION ---
GEMINI_MODEL = 'gemini-2.5-flash'

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

# --- 1. DATA ANALYSIS PROMPTS ---

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

# --- 2. IMAGE GENERATION PROMPTS ---

def generate_image_prompts_batch(count: int) -> List[Dict[str, Any]]:
    """Generate batch image generation prompts."""
    styles = ["photorealistic", "anime", "oil painting", "watercolor", "3D render"]
    aspect_ratios = ["16:9", "4:3", "1:1", "9:16"]
    subjects = ["cityscape", "portrait", "landscape", "abstract", "wildlife"]
    times = ["sunset", "sunrise", "noon", "night", "dawn"]
    
    return [
        {
            "prompt": f"A {subjects[i % len(subjects)]} at {times[i % len(times)]}",
            "style": styles[i % len(styles)],
            "aspect_ratio": aspect_ratios[i % len(aspect_ratios)],
            "quality": "high" if i % 2 == 0 else "standard",
            "seed": 1000 + i
        }
        for i in range(count)
    ]

def generate_style_variation_prompts(count: int) -> List[Dict[str, Any]]:
    """Generate prompts with same content but different styles (high repetition)."""
    base_content = "A serene mountain landscape with a lake"
    styles = ["photorealistic", "oil painting", "watercolor", "anime", "pencil sketch", "digital art", "impressionist", "abstract"]
    
    return [
        {
            "content": base_content,
            "style": styles[i % len(styles)],
            "aspect_ratio": "16:9",
            "quality": "high"
        }
        for i in range(count)
    ]

# --- 3. MULTI-TURN CONVERSATION CONTEXTS ---

def generate_conversation_context(messages: int) -> List[Dict[str, Any]]:
    """Generate conversation history with repetitive structure."""
    topics = ["weather", "technology", "science", "travel", "food", "sports", "music", "movies"]
    
    conv = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    for i in range(messages):
        topic = topics[i % len(topics)]
        conv.append({
            "role": "user",
            "content": f"Tell me about {topic}",
            "timestamp": f"2024-01-{(i % 28) + 1:02d}T10:{(i % 60):02d}:00Z"
        })
        conv.append({
            "role": "assistant",
            "content": f"Here's information about {topic}...",
            "timestamp": f"2024-01-{(i % 28) + 1:02d}T10:{(i % 60) + 1:02d}:00Z"
        })
    
    return conv

# --- 4. API RESPONSE COMPRESSION ---

def generate_rest_api_responses(count: int) -> List[Dict[str, Any]]:
    """Generate REST API response data."""
    status_codes = [200, 201, 400, 404, 500]
    methods = ["GET", "POST", "PUT", "DELETE"]
    
    return [
        {
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "status": "active" if i % 3 != 0 else "inactive",
            "created_at": f"2024-01-{(i % 28) + 1:02d}T00:00:00Z",
            "method": methods[i % len(methods)],
            "status_code": status_codes[i % len(status_codes)]
        }
        for i in range(count)
    ]

def generate_graphql_response(count: int) -> Dict[str, Any]:
    """Generate GraphQL nested response."""
    return {
        "data": {
            "users": [
                {
                    "id": i,
                    "name": f"User {i}",
                    "posts": [
                        {
                            "id": f"{i}-{j}",
                            "title": f"Post {j}",
                            "comments": [
                                {"id": f"{i}-{j}-{k}", "text": f"Comment {k}"}
                                for k in range((i + j) % 3)
                            ]
                        }
                        for j in range((i % 5) + 1)
                    ]
                }
                for i in range(count)
            ]
        }
    }

# --- 5. CONFIGURATION FILES & SETTINGS ---

def generate_app_configs(count: int) -> List[Dict[str, Any]]:
    """Generate application configuration files."""
    environments = ["development", "staging", "production"]
    db_types = ["postgresql", "mysql", "mongodb"]
    
    return [
        {
            "environment": environments[i % len(environments)],
            "database": {
                "type": db_types[i % len(db_types)],
                "host": f"db-{environments[i % len(environments)]}.example.com",
                "port": 5432 if i % 3 == 0 else 3306,
                "name": f"app_{environments[i % len(environments)]}"
            },
            "api": {
                "base_url": f"https://api-{environments[i % len(environments)]}.example.com",
                "timeout": 30,
                "retries": 3
            },
            "features": {
                "feature_a": i % 2 == 0,
                "feature_b": i % 3 == 0,
                "feature_c": True
            }
        }
        for i in range(count)
    ]

# --- 6. BATCH PROCESSING SCENARIOS ---

def generate_batch_user_updates(count: int) -> List[Dict[str, Any]]:
    """Generate batch user update operations."""
    statuses = ["active", "inactive", "pending", "suspended"]
    roles = ["user", "admin", "moderator", "guest"]
    
    return [
        {
            "user_id": i,
            "action": "update",
            "fields": {
                "status": statuses[i % len(statuses)],
                "role": roles[i % len(roles)],
                "last_modified": f"2024-01-{(i % 28) + 1:02d}T00:00:00Z"
            }
        }
        for i in range(count)
    ]

# --- 7. STREAMING DATA WINDOWS ---

def generate_time_series_data(count: int) -> List[Dict[str, Any]]:
    """Generate time-series sensor data."""
    sensor_types = ["temperature", "humidity", "pressure", "light", "motion"]
    locations = ["room1", "room2", "room3", "outdoor", "basement"]
    
    return [
        {
            "timestamp": f"2024-01-01T{(i % 24):02d}:{(i % 60):02d}:00Z",
            "sensor_type": sensor_types[i % len(sensor_types)],
            "location": locations[i % len(locations)],
            "value": round(20 + (i % 30) + (i * 0.1) % 10, 2),
            "unit": "celsius" if i % 5 == 0 else "percent"
        }
        for i in range(count)
    ]

def generate_log_stream(count: int) -> List[Dict[str, Any]]:
    """Generate application log stream."""
    levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    components = ["auth", "api", "database", "cache", "worker"]
    
    return [
        {
            "timestamp": f"2024-01-01T{(i % 24):02d}:{(i % 60):02d}:{(i % 60):02d}Z",
            "level": levels[i % len(levels)],
            "component": components[i % len(components)],
            "message": f"Processing request {i}",
            "request_id": f"req-{i:06d}",
            "duration_ms": (i % 1000) + 10
        }
        for i in range(count)
    ]

# --- 8. DATABASE QUERY RESULTS ---

def generate_sql_query_results(count: int) -> List[Dict[str, Any]]:
    """Generate SQL query result set (highly tabular)."""
    departments = ["Engineering", "Sales", "Marketing", "Support", "HR"]
    statuses = ["Active", "On Leave", "Terminated"]
    
    return [
        {
            "employee_id": i,
            "name": f"Employee {i}",
            "department": departments[i % len(departments)],
            "status": statuses[i % len(statuses)],
            "salary": round(50000 + (i % 100000), 2),
            "hire_date": f"202{(i % 4)}-01-{(i % 28) + 1:02d}"
        }
        for i in range(count)
    ]

def generate_join_query_results(count: int) -> List[Dict[str, Any]]:
    """Generate JOIN query results with related data."""
    return [
        {
            "order_id": i,
            "customer_name": f"Customer {i % 50}",
            "product_name": f"Product {i % 20}",
            "quantity": (i % 10) + 1,
            "price": round(10.99 + (i % 100), 2),
            "order_date": f"2024-01-{(i % 28) + 1:02d}",
            "shipping_address": f"{i % 100} Main St, City {i % 10}"
        }
        for i in range(count)
    ]

# --- 9. STRUCTURED LOG ANALYSIS ---

def generate_structured_logs(count: int) -> List[Dict[str, Any]]:
    """Generate structured application logs."""
    levels = ["INFO", "WARNING", "ERROR"]
    services = ["api-service", "auth-service", "db-service", "cache-service"]
    endpoints = ["/api/users", "/api/products", "/api/orders", "/api/auth"]
    
    return [
        {
            "timestamp": f"2024-01-01T{(i % 24):02d}:{(i % 60):02d}:{(i % 60):02d}Z",
            "level": levels[i % len(levels)],
            "service": services[i % len(services)],
            "endpoint": endpoints[i % len(endpoints)],
            "status_code": 200 if i % 10 != 0 else 500,
            "response_time_ms": (i % 500) + 50,
            "user_id": i % 1000,
            "ip_address": f"192.168.1.{i % 255}"
        }
        for i in range(count)
    ]

# --- 10. FORM DATA & SURVEYS ---

def generate_survey_responses(count: int) -> List[Dict[str, Any]]:
    """Generate survey response data (fixed schema, many records)."""
    ages = ["18-25", "26-35", "36-45", "46-55", "55+"]
    genders = ["Male", "Female", "Other", "Prefer not to say"]
    ratings = [1, 2, 3, 4, 5]
    
    return [
        {
            "respondent_id": i,
            "age_group": ages[i % len(ages)],
            "gender": genders[i % len(genders)],
            "satisfaction_rating": ratings[i % len(ratings)],
            "recommend_to_friend": i % 2 == 0,
            "comments": f"Response {i} comments" if i % 3 == 0 else None,
            "submitted_at": f"2024-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00Z"
        }
        for i in range(count)
    ]

# --- 11. E-COMMERCE PRODUCT CATALOGS ---

def generate_product_catalog(count: int) -> List[Dict[str, Any]]:
    """Generate e-commerce product catalog."""
    categories = ["Electronics", "Clothing", "Home & Garden", "Books", "Toys"]
    brands = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE"]
    conditions = ["New", "Used", "Refurbished"]
    
    return [
        {
            "product_id": f"PROD-{i:06d}",
            "name": f"Product {i}",
            "category": categories[i % len(categories)],
            "brand": brands[i % len(brands)],
            "price": round(9.99 + (i % 1000), 2),
            "currency": "USD",
            "condition": conditions[i % len(conditions)],
            "in_stock": i % 3 != 0,
            "rating": round(3.0 + (i % 20) / 10, 1),
            "review_count": (i % 1000)
        }
        for i in range(count)
    ]

# --- 12. SCIENTIFIC DATA & EXPERIMENTS ---

def generate_experimental_results(count: int) -> List[Dict[str, Any]]:
    """Generate scientific experimental data."""
    experiments = ["Experiment A", "Experiment B", "Experiment C"]
    conditions = ["Control", "Treatment 1", "Treatment 2"]
    
    return [
        {
            "experiment_id": i,
            "experiment_name": experiments[i % len(experiments)],
            "condition": conditions[i % len(conditions)],
            "trial": (i % 10) + 1,
            "measurement": round(10.5 + (i % 20) + (i * 0.1) % 5, 3),
            "timestamp": f"2024-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00Z",
            "researcher": f"Researcher {(i % 5) + 1}"
        }
        for i in range(count)
    ]

# --- 13. CODE ANALYSIS & ASTs ---

def generate_file_tree_structure(count: int) -> List[Dict[str, Any]]:
    """Generate file tree structure data."""
    file_types = [".py", ".js", ".ts", ".json", ".md"]
    directories = ["src", "tests", "docs", "config", "scripts"]
    
    return [
        {
            "path": f"{directories[i % len(directories)]}/file_{i}{file_types[i % len(file_types)]}",
            "type": "file",
            "size_bytes": (i % 100000) + 100,
            "lines": (i % 1000) + 10,
            "language": file_types[i % len(file_types)][1:].upper(),
            "last_modified": f"2024-01-{(i % 28) + 1:02d}T00:00:00Z"
        }
        for i in range(count)
    ]

# --- 14. FINANCIAL DATA & TRANSACTIONS ---

def generate_transactions(count: int) -> List[Dict[str, Any]]:
    """Generate financial transaction data."""
    types = ["debit", "credit", "transfer", "payment", "refund"]
    categories = ["Groceries", "Transportation", "Entertainment", "Bills", "Shopping"]
    merchants = ["MerchantA", "MerchantB", "MerchantC", "MerchantD", "MerchantE"]
    
    return [
        {
            "transaction_id": f"TXN-{i:08d}",
            "account_id": f"ACC-{(i % 100):04d}",
            "type": types[i % len(types)],
            "category": categories[i % len(categories)],
            "amount": round(abs((i * 12.5) % 1000 - 500), 2),
            "currency": "USD",
            "merchant": merchants[i % len(merchants)],
            "timestamp": f"2024-01-{(i % 28) + 1:02d}T{(i % 24):02d}:{(i % 60):02d}:00Z",
            "status": "completed" if i % 10 != 0 else "pending"
        }
        for i in range(count)
    ]

def generate_account_statements(count: int) -> List[Dict[str, Any]]:
    """Generate account statement data."""
    return [
        {
            "account_id": f"ACC-{i % 50:04d}",
            "statement_date": f"2024-01-{(i % 28) + 1:02d}",
            "balance": round(1000 + (i % 10000) - (i * 50) % 5000, 2),
            "currency": "USD",
            "transactions_count": (i % 100) + 1,
            "fees": round((i % 50) * 0.1, 2) if i % 10 == 0 else 0.0
        }
        for i in range(count)
    ]

# --- 15. HEALTHCARE & MEDICAL RECORDS ---

def generate_medical_records(count: int) -> List[Dict[str, Any]]:
    """Generate anonymized medical record data."""
    conditions = ["Hypertension", "Diabetes", "Asthma", "Arthritis", "Migraine"]
    medications = ["MedA", "MedB", "MedC", "MedD", "MedE"]
    vitals_ranges = {
        "blood_pressure": (120, 140),
        "heart_rate": (60, 100),
        "temperature": (36.5, 37.5)
    }
    
    return [
        {
            "patient_id": f"PAT-{i:06d}",
            "visit_date": f"2024-01-{(i % 28) + 1:02d}",
            "condition": conditions[i % len(conditions)],
            "medication": medications[i % len(medications)],
            "vitals": {
                "blood_pressure": f"{vitals_ranges['blood_pressure'][0] + (i % 20)}/80",
                "heart_rate": vitals_ranges["heart_rate"][0] + (i % 40),
                "temperature": round(vitals_ranges["temperature"][0] + (i % 10) / 10, 1)
            },
            "notes": f"Routine checkup {i}" if i % 3 == 0 else None
        }
        for i in range(count)
    ]

# ============================================================================
# EXPERIMENT FUNCTIONS
# ============================================================================

def prepare_prompt(data_format: str, data_payload: str, experiment_type: str = "data_analysis") -> str:
    """Prepares prompt based on experiment type."""
    if experiment_type == "data_analysis":
        instruction = f"You are an expert data analyst. The following data is in [FORMAT] format. Analyze the data and report any anomalies."
        query = "Please calculate key statistics from this data."
    elif experiment_type == "image_generation":
        instruction = f"Generate images based on the following {data_format} prompts:"
        query = "Process these image generation requests."
    elif experiment_type == "conversation":
        instruction = f"Continue the conversation based on this {data_format} context:"
        query = "Generate the next response."
    elif experiment_type == "analysis":
        instruction = f"Analyze the following {data_format} data:"
        query = "Provide insights and analysis."
    else:
        instruction = f"Process the following {data_format} data:"
        query = "Analyze and provide results."
    
    instruction = instruction.replace("[FORMAT]", data_format)
    return f"{instruction}\n\n[START_DATA_{data_format}]\n{data_payload}\n[END_DATA_{data_format}]\n\n{query}"

def count_tokens(client: genai.Client, prompt_text: str) -> int:
    """Counts tokens using Gemini API."""
    try:
        response = client.models.count_tokens(
            model=GEMINI_MODEL,
            contents=[prompt_text]
        )
        return response.total_tokens
    except APIError as e:
        print(f"API error: {e}")
        return 0

def run_experiment(client: genai.Client, data: Union[List, Dict], scenario_name: str, experiment_type: str = "data_analysis") -> Dict[str, Any]:
    """Runs experiment and returns results."""
    
    # Calculate record count
    if isinstance(data, dict):
        # For nested structures like GraphQL, try to count actual records
        if "data" in data and "users" in data.get("data", {}):
            record_count = len(data["data"]["users"])
        else:
            record_count = 1
    else:
        record_count = len(data)
    
    # JSON encoding
    json_data = json.dumps(data, separators=(',', ':'))
    json_prompt = prepare_prompt("JSON", json_data, experiment_type)
    t_json = count_tokens(client, json_prompt)
    
    # TOON encoding
    toon_data = encode(data)
    toon_prompt = prepare_prompt("TOON", toon_data, experiment_type)
    t_toon = count_tokens(client, toon_prompt)
    
    # Calculate metrics
    tokens_saved = t_json - t_toon if t_json > 0 and t_toon > 0 else 0
    percentage_reduction = (tokens_saved / t_json * 100) if t_json > 0 else 0
    
    return {
        "scenario": scenario_name,
        "record_count": record_count,
        "json_tokens": t_json,
        "toon_tokens": t_toon,
        "tokens_saved": tokens_saved,
        "percentage_reduction": percentage_reduction,
        "json_size": len(json_data),
        "toon_size": len(toon_data),
        "experiment_type": experiment_type
    }

def print_experiment_results(results: Dict[str, Any]):
    """Prints formatted results."""
    print(f"  {results['scenario']:60s} | JSON: {results['json_tokens']:6,} | TOON: {results['toon_tokens']:6,} | Saved: {results['tokens_saved']:6,} ({results['percentage_reduction']:5.2f}%)")

def run_all_experiments(client: genai.Client):
    """Runs ALL experiments from EXPERIMENT_IDEAS.md."""
    
    print("\n" + "="*80)
    print("COMPREHENSIVE TOON vs JSON EXPERIMENT SUITE")
    print(f"Model: {GEMINI_MODEL}")
    print("="*80)
    
    all_results = []
    
    # Define all test configurations
    # Format: (size, generator_func, scenario_name, experiment_type)
    test_configs = [
        # 1. DATA ANALYSIS PROMPTS
        (100, generate_simple_records, "Data Analysis - Simple Records (100)", "data_analysis"),
        (500, generate_simple_records, "Data Analysis - Simple Records (500)", "data_analysis"),
        (50, generate_complex_records, "Data Analysis - Complex Nested (50)", "data_analysis"),
        (200, generate_tabular_records, "Data Analysis - Tabular/CSV-like (200)", "data_analysis"),
        
        # 2. IMAGE GENERATION PROMPTS
        (20, generate_image_prompts_batch, "Image Generation - Batch Prompts (20)", "image_generation"),
        (100, generate_image_prompts_batch, "Image Generation - Batch Prompts (100)", "image_generation"),
        (50, generate_style_variation_prompts, "Image Generation - Style Variations (50)", "image_generation"),
        
        # 3. MULTI-TURN CONVERSATION CONTEXTS
        (10, generate_conversation_context, "Conversation - Short Context (10 msgs)", "conversation"),
        (50, generate_conversation_context, "Conversation - Long Context (50 msgs)", "conversation"),
        
        # 4. API RESPONSE COMPRESSION
        (100, generate_rest_api_responses, "API - REST Responses (100)", "analysis"),
        (50, generate_graphql_response, "API - GraphQL Nested Response (50)", "analysis"),
        
        # 5. CONFIGURATION FILES
        (10, generate_app_configs, "Config - Application Configs (10)", "analysis"),
        
        # 6. BATCH PROCESSING
        (200, generate_batch_user_updates, "Batch - User Updates (200)", "analysis"),
        (500, generate_batch_user_updates, "Batch - User Updates (500)", "analysis"),
        
        # 7. STREAMING DATA
        (100, generate_time_series_data, "Streaming - Time Series (100)", "analysis"),
        (200, generate_log_stream, "Streaming - Log Stream (200)", "analysis"),
        
        # 8. DATABASE QUERY RESULTS
        (100, generate_sql_query_results, "Database - SQL Results (100)", "analysis"),
        (500, generate_sql_query_results, "Database - SQL Results (500)", "analysis"),
        (200, generate_join_query_results, "Database - JOIN Results (200)", "analysis"),
        
        # 9. STRUCTURED LOGS
        (100, generate_structured_logs, "Logs - Structured Logs (100)", "analysis"),
        (500, generate_structured_logs, "Logs - Structured Logs (500)", "analysis"),
        
        # 10. FORM DATA & SURVEYS
        (200, generate_survey_responses, "Forms - Survey Responses (200)", "analysis"),
        (500, generate_survey_responses, "Forms - Survey Responses (500)", "analysis"),
        
        # 11. E-COMMERCE CATALOGS
        (100, generate_product_catalog, "E-commerce - Product Catalog (100)", "analysis"),
        (500, generate_product_catalog, "E-commerce - Product Catalog (500)", "analysis"),
        
        # 12. SCIENTIFIC DATA
        (100, generate_experimental_results, "Science - Experimental Data (100)", "analysis"),
        
        # 13. CODE ANALYSIS
        (50, generate_file_tree_structure, "Code - File Tree Structure (50)", "analysis"),
        
        # 14. FINANCIAL DATA
        (200, generate_transactions, "Finance - Transactions (200)", "analysis"),
        (500, generate_transactions, "Finance - Transactions (500)", "analysis"),
        (100, generate_account_statements, "Finance - Account Statements (100)", "analysis"),
        
        # 15. HEALTHCARE DATA
        (100, generate_medical_records, "Healthcare - Medical Records (100)", "analysis"),
    ]
    
    print(f"\nRunning {len(test_configs)} experiment scenarios...\n")
    
    for idx, (size, generator_func, name, exp_type) in enumerate(test_configs, 1):
        print(f"[{idx}/{len(test_configs)}] ⏳ {name}...", end=" ", flush=True)
        
        try:
            data = generator_func(size)
            results = run_experiment(client, data, name, exp_type)
            all_results.append(results)
            print(f"✓ ({results['percentage_reduction']:.1f}% reduction)")
        except Exception as e:
            print(f"✗ ERROR: {e}")
            continue
    
    # Summary Analysis
    print("\n" + "="*80)
    print("SUMMARY ANALYSIS")
    print("="*80)
    
    # Group by experiment type
    by_type = {}
    for r in all_results:
        exp_type = r.get('experiment_type', 'unknown')
        if exp_type not in by_type:
            by_type[exp_type] = []
        by_type[exp_type].append(r)
    
    print("\n--- Results by Experiment Type ---")
    for exp_type, results in sorted(by_type.items()):
        avg_reduction = sum(r['percentage_reduction'] for r in results) / len(results)
        total_saved = sum(r['tokens_saved'] for r in results)
        print(f"\n{exp_type.upper()}:")
        print(f"  Scenarios: {len(results)}")
        print(f"  Average Reduction: {avg_reduction:.2f}%")
        print(f"  Total Tokens Saved: {total_saved:,}")
    
    # Best and Worst
    print("\n--- Best Performers (Top 5) ---")
    best = sorted(all_results, key=lambda x: x['percentage_reduction'], reverse=True)[:5]
    for r in best:
        print_experiment_results(r)
    
    print("\n--- Worst Performers (Bottom 3) ---")
    worst = sorted([r for r in all_results if r['tokens_saved'] >= 0], key=lambda x: x['percentage_reduction'])[:3]
    for r in worst:
        print_experiment_results(r)
    
    # Overall stats
    total_saved = sum(r['tokens_saved'] for r in all_results)
    avg_reduction = sum(r['percentage_reduction'] for r in all_results) / len(all_results)
    total_json_tokens = sum(r['json_tokens'] for r in all_results)
    total_toon_tokens = sum(r['toon_tokens'] for r in all_results)
    
    print("\n--- Overall Statistics ---")
    print(f"Total Scenarios: {len(all_results)}")
    print(f"Total JSON Tokens: {total_json_tokens:,}")
    print(f"Total TOON Tokens: {total_toon_tokens:,}")
    print(f"Total Tokens Saved: {total_saved:,}")
    print(f"Average Reduction: {avg_reduction:.2f}%")
    print(f"Overall Reduction: {((total_json_tokens - total_toon_tokens) / total_json_tokens * 100):.2f}%")
    
    # Save results
    output_data = {
        "model": GEMINI_MODEL,
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": len(all_results),
        "total_tokens_saved": total_saved,
        "average_reduction": avg_reduction,
        "overall_reduction": ((total_json_tokens - total_toon_tokens) / total_json_tokens * 100) if total_json_tokens > 0 else 0,
        "results_by_type": {k: {
            "count": len(v),
            "avg_reduction": sum(r['percentage_reduction'] for r in v) / len(v),
            "total_saved": sum(r['tokens_saved'] for r in v)
        } for k, v in by_type.items()},
        "results": all_results
    }
    
    results_file = "all_experiments_results.json"
    with open(results_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    print(f"🌐 Open 'results_dashboard.html' in your browser to view the results!")
    print(f"   (Note: Dashboard will load {results_file} if available)")
    
    return all_results

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Set it with: export GEMINI_API_KEY='your-key-here'")
    else:
        client = genai.Client()
        print("\n🚀 Starting comprehensive experiment suite...")
        print("   This will test TOON across 15+ use cases with 30+ scenarios!")
        print("   Estimated time: 5-10 minutes depending on API response time.\n")
        
        results = run_all_experiments(client)
        print("\n✅ All experiments complete!")
        print(f"   Tested {len(results)} scenarios across all use cases.")

