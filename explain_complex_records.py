#!/usr/bin/env python3
"""
Demonstration script to explain complex nested records vs simple records
and why TOON performance differs.
"""
import json
from toon_py import encode
from toon_vs_json_experiment import generate_simple_records, generate_complex_records

print("="*80)
print("COMPARING SIMPLE vs COMPLEX NESTED RECORDS")
print("="*80)

# Generate sample data
simple_data = generate_simple_records(3)
complex_data = generate_complex_records(3)

print("\n" + "="*80)
print("1. SIMPLE RECORDS (Flat Structure)")
print("="*80)
print("\nStructure: Flat dictionary with 5 fields")
print(json.dumps(simple_data, indent=2))

print("\n" + "="*80)
print("2. COMPLEX NESTED RECORDS")
print("="*80)
print("\nStructure: Nested objects + arrays of objects + variable lengths")
print(json.dumps(complex_data, indent=2))

print("\n" + "="*80)
print("KEY DIFFERENCES")
print("="*80)

print("\n📊 SIMPLE RECORDS:")
print("   • Flat structure: 5 fields per record")
print("   • Highly repetitive: Only 4 cities, 2 statuses")
print("   • Fixed schema: Same fields, same types")
print("   • No nesting: All values at root level")
print("   • Best case for TOON: Maximum compression from repetition")

print("\n🏗️ COMPLEX NESTED RECORDS:")
print("   • Nested objects: 'profile' object contains 4 fields")
print("   • Arrays of objects: 'orders' array with 1-5 objects per record")
print("   • Variable lengths: Each record has different number of orders")
print("   • More unique values: Different zipcodes, dates, prices, tags")
print("   • Deep nesting: profile.city, orders[].product, metadata.tags[]")
print("   • Mixed types: Numbers, strings, arrays, objects all nested")

print("\n" + "="*80)
print("WHY TOON MIGHT PERFORM DIFFERENTLY")
print("="*80)

# Encode both
simple_json = json.dumps(simple_data, separators=(',', ':'))
simple_toon = encode(simple_data)

complex_json = json.dumps(complex_data, separators=(',', ':'))
complex_toon = encode(complex_data)

print("\n📏 SIZE COMPARISON (3 records):")
print(f"\nSIMPLE RECORDS:")
print(f"   JSON: {len(simple_json):,} bytes")
print(f"   TOON: {len(simple_toon):,} bytes")
print(f"   Reduction: {((len(simple_json) - len(simple_toon)) / len(simple_json) * 100):.1f}%")

print(f"\nCOMPLEX RECORDS:")
print(f"   JSON: {len(complex_json):,} bytes")
print(f"   TOON: {len(complex_toon):,} bytes")
print(f"   Reduction: {((len(complex_json) - len(complex_toon)) / len(complex_json) * 100):.1f}%")

print("\n" + "="*80)
print("WHY COMPLEX RECORDS ARE HARDER FOR TOON")
print("="*80)

print("""
1. 🎯 STRUCTURAL OVERHEAD
   • TOON needs to encode the structure (nesting levels, array lengths)
   • More nesting = more structural metadata needed
   • Variable array lengths require per-record overhead

2. 🔄 LESS REPETITION
   • Simple records: 4 cities repeated across many records → high compression
   • Complex records: More unique values (zipcodes, dates, prices) → less compression
   • Each order object has unique IDs, quantities, prices

3. 📐 SCHEMA COMPLEXITY
   • Simple: Fixed 5 fields, always the same
   • Complex: Variable structure (1-5 orders, 0-2 tags per record)
   • TOON needs to encode schema variations

4. 🏷️ FIELD NAMES OVERHEAD
   • Simple: 5 field names repeated (id, user_name, city, status, orders)
   • Complex: More field names (profile.city, profile.state, orders[].order_id, etc.)
   • Nested field paths add overhead

5. 🔢 MIXED DATA TYPES
   • Simple: Mostly strings and numbers at root level
   • Complex: Objects within arrays, arrays within objects
   • Type encoding overhead increases with nesting depth
""")

print("\n" + "="*80)
print("TOON ENCODING EXAMPLES")
print("="*80)

print("\nSIMPLE RECORD (TOON):")
print(simple_toon[:200] + "..." if len(simple_toon) > 200 else simple_toon)

print("\nCOMPLEX RECORD (TOON):")
print(complex_toon[:200] + "..." if len(complex_toon) > 200 else complex_toon)

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("""
TOON excels at:
  ✅ Flat, repetitive data (like database tables)
  ✅ Fixed schemas with many repeated values
  ✅ Simple structures with high redundancy

TOON struggles more with:
  ⚠️ Deeply nested structures
  ⚠️ Variable-length arrays
  ⚠️ Highly unique values
  ⚠️ Complex object hierarchies

This is EXPECTED behavior - TOON is optimized for tabular/repetitive data,
not complex nested document structures. The experiment will show you
exactly where TOON provides the most value!
""")


