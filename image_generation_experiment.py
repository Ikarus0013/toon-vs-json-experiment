#!/usr/bin/env python3
"""
Image Generation Prompt Experiment: TOON vs JSON

Many image generation APIs (DALL-E, Midjourney, Stable Diffusion) accept
structured JSON prompts with styles, compositions, colors, and object descriptions.
These prompts are often highly repetitive, making them perfect for TOON compression.

This experiment compares token counts for image generation prompts in JSON vs TOON format.
"""
import os
import json
from datetime import datetime
from google import genai
from google.genai.errors import APIError
from toon_py import encode
from typing import List, Dict, Any

# --- CONFIGURATION ---
GEMINI_MODEL = 'gemini-2.5-flash'

# --- IMAGE GENERATION PROMPT GENERATORS ---

def generate_single_image_prompt() -> Dict[str, Any]:
    """Generate a single image generation prompt (like DALL-E/Midjourney style)."""
    return {
        "prompt": "A futuristic cityscape at sunset with flying cars",
        "style": "photorealistic",
        "aspect_ratio": "16:9",
        "quality": "high",
        "seed": 12345
    }

def generate_batch_image_prompts(count: int) -> List[Dict[str, Any]]:
    """Generate multiple image prompts with common styles and settings."""
    styles = ["photorealistic", "anime", "oil painting", "watercolor", "3D render"]
    aspect_ratios = ["16:9", "4:3", "1:1", "9:16"]
    qualities = ["high", "standard"]
    subjects = ["cityscape", "portrait", "landscape", "abstract", "wildlife"]
    times = ["sunset", "sunrise", "noon", "night", "dawn"]
    
    prompts = []
    for i in range(count):
        prompts.append({
            "prompt": f"A {subjects[i % len(subjects)]} at {times[i % len(times)]}",
            "style": styles[i % len(styles)],
            "aspect_ratio": aspect_ratios[i % len(aspect_ratios)],
            "quality": qualities[i % len(qualities)],
            "seed": 1000 + i
        })
    return prompts

def generate_detailed_image_prompts(count: int) -> List[Dict[str, Any]]:
    """Generate detailed image prompts with composition, colors, and objects."""
    styles = ["photorealistic", "anime", "oil painting"]
    color_palettes = ["warm", "cool", "monochrome", "vibrant", "pastel"]
    compositions = ["rule of thirds", "centered", "leading lines", "symmetry"]
    lighting = ["soft", "dramatic", "natural", "studio", "golden hour"]
    moods = ["peaceful", "energetic", "mysterious", "serene", "dynamic"]
    
    objects = [
        ["mountains", "lake", "trees"],
        ["buildings", "street", "cars"],
        ["person", "background", "foreground"],
        ["sky", "clouds", "sun"],
        ["ocean", "waves", "beach"]
    ]
    
    prompts = []
    for i in range(count):
        obj_set = objects[i % len(objects)]
        prompts.append({
            "main_subject": obj_set[0],
            "background_elements": obj_set[1:],
            "style": styles[i % len(styles)],
            "color_palette": color_palettes[i % len(color_palettes)],
            "composition": compositions[i % len(compositions)],
            "lighting": lighting[i % len(lighting)],
            "mood": moods[i % len(moods)],
            "aspect_ratio": "16:9",
            "quality": "high",
            "negative_prompt": "blurry, low quality, distorted"
        })
    return prompts

def generate_scene_layout_prompts(count: int) -> List[Dict[str, Any]]:
    """Generate scene layout prompts with multiple objects and positions."""
    scene_types = ["indoor", "outdoor", "studio", "natural", "urban"]
    objects = ["chair", "table", "lamp", "window", "plant", "artwork", "bookshelf"]
    positions = ["left", "center", "right", "foreground", "background"]
    
    prompts = []
    for i in range(count):
        scene_type = scene_types[i % len(scene_types)]
        num_objects = (i % 5) + 3  # 3-7 objects
        
        scene_objects = []
        for j in range(num_objects):
            scene_objects.append({
                "object": objects[(i + j) % len(objects)],
                "position": positions[j % len(positions)],
                "size": ["small", "medium", "large"][j % 3]
            })
        
        prompts.append({
            "scene_type": scene_type,
            "objects": scene_objects,
            "style": "photorealistic",
            "lighting": "natural",
            "camera_angle": ["eye level", "bird's eye", "low angle"][i % 3],
            "color_scheme": ["warm", "cool", "neutral"][i % 3]
        })
    return prompts

def generate_style_variation_prompts(count: int) -> List[Dict[str, Any]]:
    """Generate prompts with same content but different styles (high repetition)."""
    base_content = "A serene mountain landscape with a lake"
    styles = [
        {"style": "photorealistic", "artist": None},
        {"style": "oil painting", "artist": "Van Gogh"},
        {"style": "watercolor", "artist": None},
        {"style": "anime", "artist": None},
        {"style": "pencil sketch", "artist": None},
        {"style": "digital art", "artist": None},
        {"style": "impressionist", "artist": "Monet"},
        {"style": "abstract", "artist": None}
    ]
    
    prompts = []
    for i in range(count):
        style_info = styles[i % len(styles)]
        prompt = {
            "content": base_content,
            "style": style_info["style"],
            "aspect_ratio": "16:9",
            "quality": "high"
        }
        if style_info["artist"]:
            prompt["artist_reference"] = style_info["artist"]
        prompts.append(prompt)
    return prompts

# --- EXPERIMENT FUNCTIONS ---

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

def prepare_image_prompt(data_format: str, prompt_data: Any) -> str:
    """Prepares prompt for image generation API simulation."""
    if isinstance(prompt_data, list):
        instruction = f"Generate {len(prompt_data)} images based on the following {data_format} prompts:"
    else:
        instruction = f"Generate an image based on the following {data_format} prompt:"
    
    return f"{instruction}\n\n[PROMPTS_{data_format}]\n{json.dumps(prompt_data) if data_format == 'JSON' else encode(prompt_data)}\n[END_PROMPTS_{data_format}]"

def run_image_experiment(client: genai.Client, prompt_data: Any, scenario_name: str) -> Dict[str, Any]:
    """Runs experiment for image generation prompts."""
    
    # JSON encoding
    json_prompt = prepare_image_prompt("JSON", prompt_data)
    t_json = count_tokens(client, json_prompt)
    
    # TOON encoding
    toon_prompt = prepare_image_prompt("TOON", prompt_data)
    t_toon = count_tokens(client, toon_prompt)
    
    # Calculate metrics
    tokens_saved = t_json - t_toon if t_json > 0 and t_toon > 0 else 0
    percentage_reduction = (tokens_saved / t_json * 100) if t_json > 0 else 0
    
    # Get sizes
    json_str = json.dumps(prompt_data, separators=(',', ':'))
    toon_str = encode(prompt_data)
    
    return {
        "scenario": scenario_name,
        "prompt_count": len(prompt_data) if isinstance(prompt_data, list) else 1,
        "json_tokens": t_json,
        "toon_tokens": t_toon,
        "tokens_saved": tokens_saved,
        "percentage_reduction": percentage_reduction,
        "json_size": len(json_str),
        "toon_size": len(toon_str)
    }

def run_image_generation_experiments(client: genai.Client):
    """Runs all image generation prompt experiments."""
    
    print("\n" + "="*70)
    print("IMAGE GENERATION PROMPT EXPERIMENT: TOON vs JSON")
    print(f"Model: {GEMINI_MODEL}")
    print("="*70)
    
    all_results = []
    
    # Test scenarios
    test_configs = [
        ("single", generate_single_image_prompt(), "Single Image Prompt"),
        ("batch_10", generate_batch_image_prompts(10), "Batch Generation (10 images)"),
        ("batch_50", generate_batch_image_prompts(50), "Batch Generation (50 images)"),
        ("batch_100", generate_batch_image_prompts(100), "Batch Generation (100 images)"),
        ("detailed_20", generate_detailed_image_prompts(20), "Detailed Prompts (20 images)"),
        ("detailed_50", generate_detailed_image_prompts(50), "Detailed Prompts (50 images)"),
        ("scene_layout_15", generate_scene_layout_prompts(15), "Scene Layout Prompts (15 scenes)"),
        ("style_variations_20", generate_style_variation_prompts(20), "Style Variations (20 styles, same content)"),
        ("style_variations_50", generate_style_variation_prompts(50), "Style Variations (50 styles, same content)"),
    ]
    
    for config_key, prompt_data, name in test_configs:
        print(f"\n⏳ Running: {name}...")
        results = run_image_experiment(client, prompt_data, name)
        all_results.append(results)
        
        print(f"  JSON: {results['json_tokens']:,} tokens")
        print(f"  TOON: {results['toon_tokens']:,} tokens")
        print(f"  Saved: {results['tokens_saved']:,} tokens ({results['percentage_reduction']:.2f}%)")
    
    # Summary
    print("\n" + "="*70)
    print("IMAGE GENERATION EXPERIMENT SUMMARY")
    print("="*70)
    
    total_saved = sum(r['tokens_saved'] for r in all_results)
    avg_reduction = sum(r['percentage_reduction'] for r in all_results) / len(all_results)
    
    print(f"\nTotal Tokens Saved: {total_saved:,}")
    print(f"Average Reduction: {avg_reduction:.2f}%")
    
    print("\n--- Best Cases ---")
    best = sorted(all_results, key=lambda x: x['percentage_reduction'], reverse=True)[:3]
    for r in best:
        print(f"  {r['scenario']}: {r['percentage_reduction']:.2f}% reduction")
    
    # Save results
    output_data = {
        "experiment_type": "image_generation_prompts",
        "model": GEMINI_MODEL,
        "timestamp": datetime.now().isoformat(),
        "total_tokens_saved": total_saved,
        "average_reduction": avg_reduction,
        "results": all_results
    }
    
    results_file = "image_generation_results.json"
    with open(results_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    print(f"🌐 Results can be viewed in the dashboard (experiment_results.json will be updated)")
    
    return all_results

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Set it with: export GEMINI_API_KEY='your-key-here'")
    else:
        client = genai.Client()
        run_image_generation_experiments(client)
        print("\n✅ Image generation experiment complete!")


