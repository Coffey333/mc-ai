#!/usr/bin/env python3
"""
Generate priority datasets for MC AI
Controlled generation with progress tracking
"""

from dataset_generator import DatasetGenerator
import time

def main():
    gen = DatasetGenerator()
    
    # Priority domains with target counts
    priority_config = {
        'general_knowledge': 500,
        'programming': 400,
        'health': 350,
        'emotional_intelligence': 400,
        'science': 300,
        'career': 250,
        'relationships': 300,
        'mental_health': 350,
        'productivity': 250,
        'communication': 300,
        'problem_solving': 300,
        'stress_management': 300
    }
    
    print("="*70)
    print("🚀 MC AI PRIORITY DATASET GENERATION")
    print("="*70)
    print(f"\nDomains: {len(priority_config)}")
    print(f"Total target: {sum(priority_config.values()):,} examples")
    print(f"Using: GPT-4o-mini (cost-effective)")
    print("\nStarting...\n")
    
    total_generated = 0
    start_time = time.time()
    
    for i, (domain, count) in enumerate(priority_config.items(), 1):
        print(f"\n[{i}/{len(priority_config)}] {domain.upper()}")
        print(f"Target: {count} examples")
        
        try:
            examples = gen.generate_domain(domain, target_examples=count)
            
            if examples:
                gen.save_domain_dataset(domain, examples)
                total_generated += len(examples)
                print(f"✅ Generated {len(examples)} examples")
            else:
                print(f"⚠️  No examples generated")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*70)
    print("🎉 GENERATION COMPLETE!")
    print("="*70)
    print(f"\nTotal generated: {total_generated:,} examples")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Estimated cost: ${gen.cost_estimate:.2f}")
    print(f"\nDatasets saved to: datasets/")

if __name__ == "__main__":
    main()
