#!/usr/bin/env python3
"""Continue dataset generation efficiently"""

from dataset_generator import DatasetGenerator
import os
import json

def get_existing_count(domain):
    """Check how many examples exist for a domain"""
    filepath = f"datasets/{domain}/knowledge.json"
    if os.path.exists(filepath):
        with open(filepath) as f:
            return len(json.load(f))
    return 0

def main():
    gen = DatasetGenerator()
    
    # All priority domains with targets
    targets = {
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
        'stress_management': 300,
        'data_science': 300,
        'web_development': 300,
        'nutrition': 250,
        'fitness': 250,
        'writing': 250,
        'mathematics': 300,
        'finance': 250,
        'business': 250
    }
    
    # Find domains that need generation
    todo = []
    for domain, target in targets.items():
        existing = get_existing_count(domain)
        if existing < target:
            needed = target - existing
            todo.append((domain, needed, existing))
    
    if not todo:
        print("✅ All domains complete!")
        return
    
    print(f"\n🚀 Continuing generation...")
    print(f"Domains to process: {len(todo)}\n")
    
    # Generate one domain at a time
    for domain, needed, existing in todo[:3]:  # Do 3 at a time
        print(f"\n📚 {domain}")
        print(f"   Existing: {existing}, Needed: {needed}")
        
        try:
            new_examples = gen.generate_domain(domain, target_examples=needed)
            
            # Merge with existing
            all_examples = []
            filepath = f"datasets/{domain}/knowledge.json"
            if os.path.exists(filepath):
                with open(filepath) as f:
                    all_examples = json.load(f)
            
            all_examples.extend(new_examples)
            gen.save_domain_dataset(domain, all_examples)
            
            print(f"   ✅ Now have {len(all_examples)} examples")
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Show summary
    print(f"\n📊 Current Status:")
    for domain in sorted(targets.keys()):
        count = get_existing_count(domain)
        target = targets[domain]
        status = "✅" if count >= target else "⏳"
        print(f"  {status} {domain}: {count}/{target}")

if __name__ == "__main__":
    main()
