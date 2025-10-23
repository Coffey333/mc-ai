#!/usr/bin/env python3
"""
Migrate file-based datasets to PostgreSQL
Run this when ready to move to database-backed storage

Usage:
    python scripts/migrate_datasets_to_db.py [--dry-run]
"""
import psycopg2
import json
import os
import sys
from pathlib import Path

def migrate_datasets(dry_run=False):
    """Migrate all datasets from files to PostgreSQL"""
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not set")
        sys.exit(1)
    
    if dry_run:
        print("🔍 DRY RUN MODE - no changes will be made")
    
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        dataset_dir = Path('datasets')
        if not dataset_dir.exists():
            print("❌ datasets/ directory not found")
            sys.exit(1)
        
        total_examples = 0
        migrated_domains = 0
        
        for domain_file in sorted(dataset_dir.glob('*.json')):
            domain_name = domain_file.stem
            
            if domain_name == 'archive':
                print(f"⏭️  Skipping archive folder")
                continue
            
            print(f"\n📂 Processing {domain_name}...")
            
            try:
                with open(domain_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"  ⚠️  Error reading {domain_file}: {e}")
                continue
            
            examples = data.get('examples', [])
            if not examples:
                print(f"  ⚠️  No examples found")
                continue
            
            if not dry_run:
                cur.execute(
                    "INSERT INTO datasets (domain_name, metadata) "
                    "VALUES (%s, %s) "
                    "ON CONFLICT (domain_name) DO UPDATE "
                    "SET updated_at = NOW(), metadata = EXCLUDED.metadata "
                    "RETURNING id",
                    (domain_name, json.dumps(data.get('metadata', {})))
                )
                dataset_id = cur.fetchone()[0]
                
                for example in examples:
                    content = example.get('content') or example.get('completion', '')
                    response = example.get('response', '')
                    
                    if not content:
                        continue
                    
                    cur.execute(
                        "INSERT INTO examples (dataset_id, content, response, metadata) "
                        "VALUES (%s, %s, %s, %s)",
                        (dataset_id, content, response, json.dumps(example))
                    )
                
                cur.execute(
                    "UPDATE datasets SET example_count = "
                    "(SELECT COUNT(*) FROM examples WHERE dataset_id = %s) "
                    "WHERE id = %s",
                    (dataset_id, dataset_id)
                )
            
            total_examples += len(examples)
            migrated_domains += 1
            print(f"  ✅ {len(examples)} examples")
        
        if not dry_run:
            conn.commit()
            print(f"\n✅ Migration complete!")
        else:
            print(f"\n🔍 Dry run complete - no changes made")
        
        print(f"📊 Summary:")
        print(f"  Domains: {migrated_domains}")
        print(f"  Examples: {total_examples}")
        
        cur.execute("SELECT domain_name, example_count FROM datasets ORDER BY domain_name")
        print(f"\n📋 Database contents:")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]} examples")
        
        conn.close()
    
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    migrate_datasets(dry_run)
