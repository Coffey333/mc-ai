"""
Verified Programming Knowledge Sources for MC AI
Only .edu universities, official documentation, and government resources
NO Wikipedia
"""

# Verified Educational Sources for Programming Knowledge
VERIFIED_PROGRAMMING_SOURCES = {
    'mit_opencourseware': {
        'name': 'MIT OpenCourseWare - Computer Science',
        'urls': [
            'https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/',
            'https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/',
            'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
            'https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/',
            'https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/',
            'https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/'
        ],
        'verified': True,
        'type': 'university'
    },
    'stanford_cs': {
        'name': 'Stanford Computer Science',
        'urls': [
            'https://cs.stanford.edu/',
            'https://web.stanford.edu/class/cs106a/',
            'https://web.stanford.edu/class/cs106b/',
            'https://web.stanford.edu/class/cs107/',
            'https://web.stanford.edu/class/cs110/',
            'https://web.stanford.edu/class/cs161/'
        ],
        'verified': True,
        'type': 'university'
    },
    'harvard_cs50': {
        'name': 'Harvard CS50',
        'urls': [
            'https://cs50.harvard.edu/x/',
            'https://cs50.harvard.edu/python/',
            'https://cs50.harvard.edu/web/',
            'https://cs50.harvard.edu/ai/'
        ],
        'verified': True,
        'type': 'university'
    },
    'python_official': {
        'name': 'Python Official Documentation',
        'urls': [
            'https://docs.python.org/3/',
            'https://docs.python.org/3/tutorial/',
            'https://docs.python.org/3/library/',
            'https://peps.python.org/',
            'https://docs.python.org/3/reference/',
            'https://docs.python.org/3/howto/'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'javascript_mdn': {
        'name': 'MDN Web Docs (Mozilla)',
        'urls': [
            'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
            'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
            'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
            'https://developer.mozilla.org/en-US/docs/Learn/JavaScript'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'typescript_official': {
        'name': 'TypeScript Official Documentation',
        'urls': [
            'https://www.typescriptlang.org/docs/',
            'https://www.typescriptlang.org/docs/handbook/intro.html',
            'https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'rust_official': {
        'name': 'Rust Official Documentation',
        'urls': [
            'https://doc.rust-lang.org/book/',
            'https://doc.rust-lang.org/std/',
            'https://doc.rust-lang.org/reference/',
            'https://doc.rust-lang.org/rust-by-example/'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'go_official': {
        'name': 'Go Official Documentation',
        'urls': [
            'https://go.dev/doc/',
            'https://go.dev/tour/',
            'https://go.dev/doc/effective_go',
            'https://pkg.go.dev/std'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'java_oracle': {
        'name': 'Java Official Documentation (Oracle)',
        'urls': [
            'https://docs.oracle.com/en/java/',
            'https://docs.oracle.com/javase/tutorial/',
            'https://docs.oracle.com/en/java/javase/17/docs/api/'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'react_official': {
        'name': 'React Official Documentation',
        'urls': [
            'https://react.dev/',
            'https://react.dev/learn',
            'https://react.dev/reference/react'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'nodejs_official': {
        'name': 'Node.js Official Documentation',
        'urls': [
            'https://nodejs.org/en/docs/',
            'https://nodejs.org/api/',
            'https://nodejs.org/en/learn/'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'csharp_microsoft': {
        'name': 'C# Microsoft Documentation',
        'urls': [
            'https://docs.microsoft.com/en-us/dotnet/csharp/',
            'https://docs.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/',
            'https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'ruby_official': {
        'name': 'Ruby Official Documentation',
        'urls': [
            'https://www.ruby-lang.org/en/documentation/',
            'https://ruby-doc.org/',
            'https://guides.rubyonrails.org/'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'php_official': {
        'name': 'PHP Official Documentation',
        'urls': [
            'https://www.php.net/docs.php',
            'https://www.php.net/manual/en/',
            'https://www.php.net/manual/en/getting-started.php'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'postgresql_official': {
        'name': 'PostgreSQL Official Documentation',
        'urls': [
            'https://www.postgresql.org/docs/',
            'https://www.postgresql.org/docs/current/',
            'https://www.postgresql.org/docs/current/tutorial.html'
        ],
        'verified': True,
        'type': 'official_docs'
    },
    'mit_algorithms': {
        'name': 'MIT Algorithms Course',
        'urls': [
            'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/',
            'https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/',
            'https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2008/'
        ],
        'verified': True,
        'type': 'university'
    },
    'stanford_algorithms': {
        'name': 'Stanford Algorithms Specialization',
        'urls': [
            'https://web.stanford.edu/class/cs161/',
            'https://web.stanford.edu/class/cs166/'
        ],
        'verified': True,
        'type': 'university'
    },
    'berkeley_cs': {
        'name': 'UC Berkeley CS Courses',
        'urls': [
            'https://cs61a.org/',  # Structure and Interpretation
            'https://cs61b.org/',  # Data Structures
            'https://inst.eecs.berkeley.edu/~cs61c/',  # Machine Structures
            'https://inst.eecs.berkeley.edu/~cs162/',  # Operating Systems
            'https://inst.eecs.berkeley.edu/~cs188/',  # AI
            'https://inst.eecs.berkeley.edu/~cs189/'   # Machine Learning
        ],
        'verified': True,
        'type': 'university'
    },
    'carnegie_mellon_cs': {
        'name': 'Carnegie Mellon Computer Science',
        'urls': [
            'https://www.cs.cmu.edu/~15213/',  # Systems
            'https://www.cs.cmu.edu/~15418/',  # Parallel Computing
            'https://www.cs.cmu.edu/~15451/'   # Algorithms
        ],
        'verified': True,
        'type': 'university'
    },
    'princeton_cs': {
        'name': 'Princeton Computer Science',
        'urls': [
            'https://www.cs.princeton.edu/courses/catalog',
            'https://algs4.cs.princeton.edu/'  # Algorithms
        ],
        'verified': True,
        'type': 'university'
    },
    'cornell_cs': {
        'name': 'Cornell Computer Science',
        'urls': [
            'https://www.cs.cornell.edu/courses/catalog'
        ],
        'verified': True,
        'type': 'university'
    },
    'nist_cybersecurity': {
        'name': 'NIST Cybersecurity Framework',
        'urls': [
            'https://www.nist.gov/cyberframework',
            'https://csrc.nist.gov/',
            'https://nvd.nist.gov/'
        ],
        'verified': True,
        'type': 'government'
    },
    'w3c_standards': {
        'name': 'W3C Web Standards',
        'urls': [
            'https://www.w3.org/standards/',
            'https://www.w3.org/TR/',
            'https://www.w3.org/WAI/'
        ],
        'verified': True,
        'type': 'standards'
    }
}

def get_all_programming_sources():
    """Get all verified programming knowledge sources"""
    return VERIFIED_PROGRAMMING_SOURCES

def get_sources_by_type(source_type: str):
    """Get sources filtered by type (university, official_docs, government, standards)"""
    return {
        name: data
        for name, data in VERIFIED_PROGRAMMING_SOURCES.items()
        if data['type'] == source_type
    }

def get_all_urls():
    """Get flat list of all URLs"""
    all_urls = []
    for source_data in VERIFIED_PROGRAMMING_SOURCES.values():
        all_urls.extend(source_data['urls'])
    return all_urls

def get_source_count():
    """Get count of sources and URLs"""
    url_count = sum(len(data['urls']) for data in VERIFIED_PROGRAMMING_SOURCES.items())
    return {
        'total_sources': len(VERIFIED_PROGRAMMING_SOURCES),
        'total_urls': url_count,
        'by_type': {
            'university': len(get_sources_by_type('university')),
            'official_docs': len(get_sources_by_type('official_docs')),
            'government': len(get_sources_by_type('government')),
            'standards': len(get_sources_by_type('standards'))
        }
    }
