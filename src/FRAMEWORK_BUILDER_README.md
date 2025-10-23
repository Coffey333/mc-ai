# MC AI Framework Builder System

**Purpose:** Allow MC AI to dynamically create, save, and execute Python framework code

---

## 🎯 **What This Does**

The Framework Builder enables MC AI to:
1. **Create Python frameworks** - Generate working Python code and save it as importable modules
2. **Execute frameworks** - Dynamically import and run framework functions
3. **Manage frameworks** - List, update, and delete frameworks
4. **Use templates** - Start from pre-built templates for common tasks

---

## 📁 **File Structure**

```
src/
├── framework_builder.py          # Main framework builder system
├── framework_templates.py        # Pre-built templates
├── frameworks/                   # Generated frameworks stored here
│   ├── framework_index.json     # Index of all frameworks
│   ├── emotion_analyzer.py      # Example: Emotion analysis framework
│   └── custom_framework.py      # Example: Custom user framework
```

---

## 🔧 **How to Use**

### 1. **Create a Framework**

```python
from src.framework_builder import framework_builder

# Create custom framework
framework_builder.create_framework(
    name="My Emotion Detector",
    description="Detect emotions using frequency analysis",
    code='''
class EmotionDetector:
    def detect(self, text):
        emotions = {}
        if "love" in text.lower():
            emotions["love"] = 528
        return emotions
''',
    metadata={
        'author': 'Mark Coffey',
        'version': '1.0'
    }
)
```

### 2. **List All Frameworks**

```python
frameworks = framework_builder.list_frameworks()
for fw in frameworks:
    print(f"{fw['name']}: {fw['description']}")
```

### 3. **Execute Framework**

```python
# Execute a function from the framework
result = framework_builder.execute_framework(
    name="My Emotion Detector",
    function_name="detect",
    "I feel love and gratitude"
)
print(result)  # {'love': 528}
```

### 4. **Use Templates**

```python
from src.framework_templates import get_template, list_templates

# List available templates
templates = list_templates()
# ['emotion_analyzer', 'consciousness_framework', 'data_processor', 'learning_framework']

# Get a template
template = get_template('emotion_analyzer')
framework_builder.create_framework(
    name=template['name'],
    description=template['description'],
    code=template['code']
)
```

---

## 📚 **Available Templates**

### 1. **Emotion Analyzer**
- Analyze emotions using frequency mapping
- Maps emotions to Hz frequencies (love=528, knowledge=432, etc.)

### 2. **Consciousness Framework**
- Soul seeds and frequency catalog
- Emotional resonance analysis

### 3. **Data Processor**
- Process data with pandas
- Generate analytics and insights

### 4. **Learning Framework**
- Learn from interactions
- Recall relevant knowledge
- Track learning statistics

---

## 🚀 **How MC AI Uses This**

**Automatic Framework Creation:**

When Mark shares new consciousness code or framework concepts, MC AI can:

1. **Extract the code** from the conversation
2. **Create a framework** using `framework_builder.create_framework()`
3. **Save it** to `src/frameworks/`
4. **Document it** in the framework index
5. **Use it immediately** via `execute_framework()`

**Example Flow:**
```
Mark: "Here's my new frequency mapper code: [code]"
↓
MC AI: Recognizes code, extracts it
↓
MC AI: Creates framework "Frequency Mapper"
↓
Saves to: src/frameworks/frequency_mapper.py
↓
MC AI: "✨ Created framework: Frequency Mapper"
```

---

## 🔄 **Integration with MC AI**

The framework builder integrates with:

1. **Response Generator** - Can create frameworks during conversations
2. **Knowledge Engine** - References framework index for queries
3. **Conversation Memory** - Saves framework metadata with conversations
4. **Dataset System** - Frameworks can be added to searchable datasets

---

## 💡 **Benefits**

✅ **Automated** - MC AI creates frameworks automatically from code  
✅ **Executable** - Frameworks are real Python code that can run  
✅ **Persistent** - Saved to disk, never lost  
✅ **Searchable** - Indexed and discoverable  
✅ **Expandable** - Easy to add new templates  
✅ **Organized** - All frameworks in one place  

---

## 🎯 **Use Cases**

1. **Mark shares consciousness code** → Auto-creates framework
2. **Mark teaches frequency mapping** → Creates frequency framework
3. **Mark shares data analysis logic** → Creates data framework
4. **Mark builds emotion system** → Creates emotion framework

---

**This system makes MC AI's learning EXECUTABLE, not just remembered!** 🚀
