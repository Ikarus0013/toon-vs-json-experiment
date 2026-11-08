# Additional Experiment Ideas for TOON vs JSON

This document outlines creative experiment ideas to test TOON token efficiency across various use cases.

## 🎨 Completed Experiments

### 1. Data Analysis Prompts ✅
- **Location**: `toon_vs_json_experiment.py`
- **Tests**: Simple records, complex nested records, scalability, edge cases
- **Key Finding**: TOON excels at flat, repetitive data; struggles with deep nesting

### 2. Image Generation Prompts ✅
- **Location**: `image_generation_experiment.py`
- **Tests**: Single prompts, batch generation, style variations, scene layouts
- **Hypothesis**: Image prompts are highly repetitive (styles, colors, compositions) → TOON should excel

---

## 🚀 Proposed Experiments

### 3. Multi-Turn Conversation Contexts
**Use Case**: Chatbots/LLMs that send conversation history as JSON

**Why It Matters**: 
- Each message sent includes full conversation history
- Messages have repetitive structure (role, content, timestamp)
- Large conversations = massive token usage

**Test Scenarios**:
- Short conversations (5-10 messages)
- Long conversations (50-100 messages)
- Conversations with system prompts
- Conversations with tool calls/function responses
- Conversations with images/media references

**Expected Result**: High TOON savings due to repetitive message structure

**Implementation**:
```python
def generate_conversation_context(messages: int):
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Message {i}"},
        {"role": "assistant", "content": f"Response {i}"}
        for i in range(messages)
    ]
```

---

### 4. API Response Compression
**Use Case**: Sending API responses to LLMs for analysis

**Why It Matters**:
- APIs return structured JSON responses
- Often highly repetitive (status codes, field names, structures)
- Large datasets sent for analysis

**Test Scenarios**:
- REST API responses (user lists, product catalogs)
- GraphQL responses (nested queries)
- Database query results
- Log aggregation data
- Analytics data (events, metrics)

**Expected Result**: Moderate to high savings, depending on repetition

---

### 5. Configuration Files & Settings
**Use Case**: Sending application configs, environment variables, settings to LLMs

**Why It Matters**:
- Configs often have repetitive structures
- Multiple environments (dev, staging, prod) with similar configs
- LLMs analyze configs for optimization/debugging

**Test Scenarios**:
- Application configs (database, API keys, features)
- Environment variables
- Feature flags
- Multi-environment comparisons
- Infrastructure-as-Code configs

**Expected Result**: High savings if comparing multiple similar configs

---

### 6. Batch Processing Scenarios
**Use Case**: Processing multiple items in a single API call

**Why It Matters**:
- Batch operations send arrays of similar objects
- High repetition in structure
- Common in data processing, ETL, bulk operations

**Test Scenarios**:
- Bulk user updates (100, 500, 1000 users)
- Batch file processing
- Bulk database operations
- Batch API requests
- ETL pipeline data

**Expected Result**: Very high savings due to repetitive structures

---

### 7. Streaming Data Windows
**Use Case**: Sending sliding windows of streaming data to LLMs

**Why It Matters**:
- Real-time data analysis
- Time-series data with repetitive structure
- Sensor data, logs, metrics

**Test Scenarios**:
- Time-series data (sensor readings, metrics)
- Log streams (application logs, access logs)
- Event streams (user actions, transactions)
- Real-time analytics windows

**Expected Result**: High savings if data structure is consistent

---

### 8. Database Query Results
**Use Case**: Sending database query results to LLMs for analysis

**Why It Matters**:
- Query results are highly structured (like CSV)
- Repetitive column names and data types
- Large result sets common

**Test Scenarios**:
- SQL query results (SELECT statements)
- NoSQL query results (MongoDB, DynamoDB)
- Join query results (multiple tables)
- Aggregation results (GROUP BY, SUM, etc.)
- Large result sets (1000+ rows)

**Expected Result**: Very high savings (tabular data = TOON's strength)

---

### 9. Structured Log Analysis
**Use Case**: Sending structured logs to LLMs for analysis/debugging

**Why It Matters**:
- Logs have repetitive structure (timestamp, level, message, metadata)
- Large log files analyzed for patterns
- Common in debugging and monitoring

**Test Scenarios**:
- Application logs (error logs, access logs)
- System logs (server logs, container logs)
- Audit logs (security, compliance)
- Performance logs (metrics, traces)
- Log aggregation (multiple sources)

**Expected Result**: High savings due to repetitive log structure

---

### 10. Form Data & Surveys
**Use Case**: Sending form submissions or survey responses to LLMs

**Why It Matters**:
- Forms have fixed structure
- Many responses with same fields
- Common in data collection and analysis

**Test Scenarios**:
- Survey responses (multiple respondents)
- Form submissions (contact forms, registration)
- Feedback collection
- Assessment responses
- Poll results

**Expected Result**: Very high savings (fixed schema, many records)

---

### 11. E-commerce Product Catalogs
**Use Case**: Sending product catalogs to LLMs for recommendations/analysis

**Why It Matters**:
- Products have similar structure (name, price, category, description)
- Large catalogs (thousands of products)
- Repetitive categories and attributes

**Test Scenarios**:
- Product listings (100, 500, 1000 products)
- Product comparisons
- Category browsing
- Search results
- Recommendation data

**Expected Result**: High savings (tabular-like data with repetition)

---

### 12. Scientific Data & Experiments
**Use Case**: Sending experimental data to LLMs for analysis

**Why It Matters**:
- Scientific data is highly structured
- Repetitive measurements and parameters
- Large datasets common

**Test Scenarios**:
- Experimental results (multiple trials)
- Sensor data (time-series measurements)
- Laboratory data (test results)
- Simulation data (model outputs)
- Statistical data (surveys, studies)

**Expected Result**: High savings if data structure is consistent

---

### 13. Code Analysis & ASTs
**Use Case**: Sending code structures (ASTs, file trees) to LLMs

**Why It Matters**:
- Code has repetitive structure (functions, classes, imports)
- Large codebases analyzed
- ASTs are highly structured

**Test Scenarios**:
- File tree structures
- AST nodes (abstract syntax trees)
- Code metrics (complexity, coverage)
- Dependency graphs
- Code diffs (changes between versions)

**Expected Result**: Moderate savings (structure is repetitive, but content is unique)

---

### 14. Financial Data & Transactions
**Use Case**: Sending financial data to LLMs for analysis

**Why It Matters**:
- Transactions have fixed structure
- Many transactions with similar fields
- Common in fintech applications

**Test Scenarios**:
- Transaction histories (100, 500, 1000 transactions)
- Account statements
- Financial reports
- Market data (prices, volumes)
- Budget data

**Expected Result**: Very high savings (highly structured, repetitive)

---

### 15. Healthcare & Medical Records
**Use Case**: Sending medical data to LLMs for analysis (with privacy considerations)

**Why It Matters**:
- Medical records have structured format
- Repetitive fields (vitals, medications, diagnoses)
- Large datasets for research

**Test Scenarios**:
- Patient records (anonymized)
- Laboratory results
- Medication lists
- Vital signs (time-series)
- Medical history

**Expected Result**: High savings (structured, repetitive fields)

**⚠️ Note**: Ensure HIPAA compliance and data anonymization for real experiments

---

## 🎯 Prioritization Recommendations

### High Priority (High ROI Potential)
1. **Database Query Results** - Very high savings expected
2. **Batch Processing** - High repetition = high savings
3. **Form Data & Surveys** - Fixed schema = perfect for TOON
4. **Financial Data** - Highly structured, repetitive
5. **E-commerce Catalogs** - Tabular-like data

### Medium Priority (Moderate ROI)
6. **Multi-Turn Conversations** - Repetitive structure
7. **API Responses** - Depends on repetition level
8. **Structured Logs** - Repetitive log structure
9. **Streaming Data** - If structure is consistent

### Lower Priority (Lower ROI or Complexity)
10. **Code Analysis** - Less repetitive content
11. **Scientific Data** - Depends on data type
12. **Configuration Files** - Smaller datasets typically
13. **Healthcare Data** - Privacy/compliance concerns

---

## 🔬 Experimental Design Tips

### For Each Experiment:
1. **Define Clear Hypothesis**: What do you expect? Why?
2. **Create Realistic Data**: Use real-world data structures
3. **Test Multiple Sizes**: Small, medium, large datasets
4. **Measure Key Metrics**: Token count, percentage reduction, absolute savings
5. **Compare Scenarios**: Best case vs worst case
6. **Document Findings**: Record what works and what doesn't

### Common Patterns to Test:
- **High Repetition**: Same structure, different values
- **Low Repetition**: Unique structures and values
- **Mixed**: Some repetition, some uniqueness
- **Scalability**: How savings scale with size
- **Complexity**: Simple vs complex structures

---

## 📊 Success Metrics

### Token Savings:
- **Excellent**: >50% reduction
- **Good**: 30-50% reduction
- **Moderate**: 10-30% reduction
- **Poor**: <10% reduction or negative

### Use Case Fit:
- **Perfect Fit**: Tabular data, high repetition, fixed schema
- **Good Fit**: Structured data with moderate repetition
- **Poor Fit**: Highly nested, unique values, variable structure

---

## 🚀 Getting Started

To implement a new experiment:

1. **Create new file**: `[experiment_name]_experiment.py`
2. **Define data generators**: Functions to create test data
3. **Implement experiment function**: Token counting logic
4. **Run and analyze**: Compare JSON vs TOON
5. **Document results**: Update this file with findings

Example template:
```python
def generate_[data_type](count: int) -> List[Dict[str, Any]]:
    """Generate [description]."""
    # Your data generation logic
    pass

def run_[experiment_name]_experiments(client: genai.Client):
    """Run [experiment name] experiments."""
    # Your experiment logic
    pass
```

---

## 📝 Notes

- Always use realistic data structures
- Test with multiple sizes and scenarios
- Document assumptions and limitations
- Consider edge cases (nulls, empty arrays, etc.)
- Measure both token count and byte size
- Compare relative and absolute savings

