#!/usr/bin/env python3
"""
Extensive Dataset Generator for MC AI
Generates comprehensive training data using GPT-4o via Replit AI
Cost-effective batch generation with domain coverage
"""

import os
import json
import time
from typing import List, Dict
from openai import OpenAI
from datetime import datetime

class DatasetGenerator:
    """Generate extensive training datasets efficiently"""
    
    def __init__(self):
        # Use Replit AI integration (no API key needed)
        self.client = OpenAI(
            api_key=os.environ.get('AI_INTEGRATIONS_OPENAI_API_KEY'),
            base_url=os.environ.get('AI_INTEGRATIONS_OPENAI_BASE_URL')
        )
        
        # Comprehensive domain coverage (50+ domains)
        self.domains = {
            # Core Knowledge
            'general_knowledge': 'General facts, trivia, common knowledge',
            'science': 'Physics, chemistry, biology, astronomy',
            'mathematics': 'Algebra, calculus, geometry, statistics',
            'history': 'World history, events, civilizations',
            'geography': 'Countries, capitals, natural features',
            
            # Technology & Computing
            'programming': 'Python, JavaScript, web development',
            'data_science': 'Data analysis, machine learning, AI',
            'cybersecurity': 'Security practices, encryption, threats',
            'cloud_computing': 'AWS, Azure, GCP, DevOps',
            'databases': 'SQL, NoSQL, data modeling',
            'web_development': 'HTML, CSS, React, Node.js',
            'mobile_dev': 'iOS, Android, React Native',
            
            # Health & Wellness
            'health': 'Medical information, wellness, fitness',
            'nutrition': 'Diet, food science, healthy eating',
            'mental_health': 'Psychology, emotional wellness',
            'fitness': 'Exercise, training, sports science',
            'meditation': 'Mindfulness, relaxation techniques',
            
            # Life & Career
            'career': 'Job hunting, interviews, professional growth',
            'finance': 'Personal finance, investing, budgeting',
            'business': 'Entrepreneurship, management, strategy',
            'productivity': 'Time management, habits, efficiency',
            'relationships': 'Communication, social skills',
            'parenting': 'Child development, parenting advice',
            
            # Creative & Arts
            'writing': 'Creative writing, storytelling, grammar',
            'art': 'Drawing, painting, design principles',
            'music_theory': 'Music composition, instruments, theory',
            'photography': 'Camera techniques, composition',
            'cooking': 'Recipes, techniques, culinary science',
            
            # Academic
            'literature': 'Books, poetry, literary analysis',
            'philosophy': 'Ethics, logic, philosophical concepts',
            'economics': 'Microeconomics, macroeconomics',
            'linguistics': 'Language, grammar, communication',
            'education': 'Learning theory, teaching methods',
            
            # Practical Skills
            'home_improvement': 'DIY, repairs, maintenance',
            'gardening': 'Plants, landscaping, agriculture',
            'automotive': 'Car maintenance, mechanics',
            'travel': 'Destinations, tips, planning',
            
            # Specialized
            'law': 'Legal concepts, rights, procedures',
            'environment': 'Climate, sustainability, ecology',
            'astronomy': 'Space, planets, cosmology',
            'architecture': 'Design, construction, styles',
            'fashion': 'Style, design, trends',
            
            # MC AI Specific
            'emotional_intelligence': 'Emotions, empathy, social awareness',
            'cymatics': 'Sound, frequencies, patterns',
            'frequency_healing': 'Sound therapy, vibrations',
            'meditation_techniques': 'Mindfulness practices, guided meditation',
            'stress_management': 'Coping strategies, relaxation',
            'creativity': 'Creative thinking, innovation',
            'problem_solving': 'Critical thinking, decision making',
            'communication': 'Effective communication, active listening',
            
            # Technical Depth
            'algorithms': 'Data structures, complexity, optimization',
            'system_design': 'Architecture, scalability, patterns',
            'api_design': 'REST, GraphQL, API best practices',
            'testing': 'Unit tests, integration tests, TDD',
            'devops': 'CI/CD, containers, orchestration'
        }
        
        self.output_dir = 'datasets'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generation stats
        self.total_generated = 0
        self.cost_estimate = 0.0
    
    def generate_batch(self, domain: str, description: str, batch_size: int = 20) -> List[Dict]:
        """
        Generate batch of Q&A examples for a domain
        Uses efficient batch prompting to reduce API calls
        """
        
        prompt = f"""Generate {batch_size} high-quality question-answer pairs for the domain: {domain}
        
Domain description: {description}

Requirements:
1. Cover diverse aspects of the topic
2. Mix difficulty levels (beginner, intermediate, advanced)
3. Include practical examples and explanations
4. Make answers comprehensive but concise (2-4 sentences)
5. Ensure factual accuracy

Format each as JSON:
{{"prompt": "question here", "response": "detailed answer here"}}

Generate {batch_size} examples as a JSON array."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective model
                messages=[
                    {"role": "system", "content": "You are an expert knowledge base creator. Generate accurate, helpful training data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Some variety
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            
            if not content:
                return []
            
            # Parse JSON response
            try:
                # Try to extract JSON array
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                examples = json.loads(content)
                
                # Ensure it's a list
                if isinstance(examples, dict):
                    examples = [examples]
                
                # Add metadata
                for ex in examples:
                    ex['domain'] = domain
                    ex['generated_at'] = datetime.now().isoformat()
                
                # Update stats
                self.total_generated += len(examples)
                self.cost_estimate += 0.001  # Rough estimate per batch
                
                return examples
                
            except json.JSONDecodeError as e:
                print(f"⚠️  JSON parse error for {domain}: {e}")
                return []
        
        except Exception as e:
            print(f"❌ Error generating {domain}: {e}")
            return []
    
    def generate_domain(self, domain: str, target_examples: int = 200) -> List[Dict]:
        """Generate comprehensive examples for a domain"""
        
        description = self.domains.get(domain, domain)
        all_examples = []
        
        print(f"\n📚 Generating {target_examples} examples for: {domain}")
        
        batches = (target_examples // 20) + 1  # 20 per batch
        
        for i in range(batches):
            print(f"  Batch {i+1}/{batches}...", end=' ')
            
            batch = self.generate_batch(domain, description, batch_size=20)
            all_examples.extend(batch)
            
            print(f"✓ ({len(batch)} examples)")
            
            # Rate limiting
            time.sleep(1)
            
            if len(all_examples) >= target_examples:
                break
        
        return all_examples[:target_examples]
    
    def save_domain_dataset(self, domain: str, examples: List[Dict]):
        """Save domain dataset to file"""
        
        domain_dir = os.path.join(self.output_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)
        
        filepath = os.path.join(domain_dir, 'knowledge.json')
        
        with open(filepath, 'w') as f:
            json.dump(examples, f, indent=2)
        
        print(f"💾 Saved {len(examples)} examples to {filepath}")
    
    def generate_all_domains(self, examples_per_domain: int = 200):
        """Generate dataset for all domains"""
        
        print("="*60)
        print("🚀 EXTENSIVE DATASET GENERATION")
        print("="*60)
        print(f"\nTotal domains: {len(self.domains)}")
        print(f"Examples per domain: {examples_per_domain}")
        print(f"Total target: {len(self.domains) * examples_per_domain:,} examples")
        print("\nStarting generation...\n")
        
        start_time = time.time()
        
        for i, (domain, description) in enumerate(self.domains.items(), 1):
            print(f"\n[{i}/{len(self.domains)}] Domain: {domain}")
            
            examples = self.generate_domain(domain, examples_per_domain)
            
            if examples:
                self.save_domain_dataset(domain, examples)
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("✅ GENERATION COMPLETE")
        print("="*60)
        print(f"\nTotal examples generated: {self.total_generated:,}")
        print(f"Total domains: {len(self.domains)}")
        print(f"Time elapsed: {elapsed/60:.1f} minutes")
        print(f"Estimated cost: ${self.cost_estimate:.2f}")
        print(f"\nDatasets saved to: {self.output_dir}/")
    
    def generate_priority_domains(self):
        """Generate high-priority domains first (cost-effective start)"""
        
        priority_domains = [
            'general_knowledge',
            'programming', 
            'health',
            'emotional_intelligence',
            'science',
            'career',
            'relationships',
            'mental_health',
            'productivity',
            'communication',
            'problem_solving',
            'stress_management'
        ]
        
        print("="*60)
        print("🎯 PRIORITY DATASET GENERATION (Cost-Effective)")
        print("="*60)
        print(f"\nGenerating {len(priority_domains)} priority domains")
        print("300 examples each = ~3,600 total examples\n")
        
        for domain in priority_domains:
            if domain in self.domains:
                description = self.domains[domain]
                print(f"\n📚 {domain}")
                
                examples = self.generate_domain(domain, target_examples=300)
                
                if examples:
                    self.save_domain_dataset(domain, examples)
        
        print("\n" + "="*60)
        print("✅ PRIORITY GENERATION COMPLETE")
        print("="*60)
        print(f"\nTotal: {self.total_generated:,} examples")
        print(f"Cost: ~${self.cost_estimate:.2f}")


def main():
    """Main execution"""
    import sys
    
    generator = DatasetGenerator()
    
    # Check arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == 'priority':
            # Generate priority domains (cost-effective)
            generator.generate_priority_domains()
        
        elif mode == 'full':
            # Generate all domains
            examples_per_domain = int(sys.argv[2]) if len(sys.argv) > 2 else 200
            generator.generate_all_domains(examples_per_domain)
        
        elif mode == 'domain':
            # Generate specific domain
            if len(sys.argv) < 3:
                print("Usage: python dataset_generator.py domain <domain_name> [count]")
                return
            
            domain = sys.argv[2]
            count = int(sys.argv[3]) if len(sys.argv) > 3 else 200
            
            if domain in generator.domains:
                examples = generator.generate_domain(domain, count)
                generator.save_domain_dataset(domain, examples)
            else:
                print(f"❌ Domain '{domain}' not found")
                print(f"Available: {', '.join(generator.domains.keys())}")
    
    else:
        # Default: priority domains
        print("Usage:")
        print("  python dataset_generator.py priority              # Generate priority domains (~3,600 examples)")
        print("  python dataset_generator.py full [count]          # Generate all domains (count per domain)")
        print("  python dataset_generator.py domain <name> [count] # Generate specific domain")
        print("\nRunning priority generation by default...\n")
        
        generator.generate_priority_domains()


if __name__ == "__main__":
    main()
