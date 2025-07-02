#!/usr/bin/env python3
"""
Token Efficiency Analysis for OCTAVE Operators
Simple character and word-based analysis
"""

# Test examples from all scenarios
test_cases = {
    "Microservices": {
        "unicode": "User_Service ⊕ Auth_Service ⚡ Rate_Limiter → Checkout_Flow",
        "ascii_math": "User_Service + Auth_Service * Rate_Limiter -> Checkout_Flow",
        "ascii_text": "User_Service _AND_ Auth_Service _VS_ Rate_Limiter _TO_ Checkout_Flow",
        "natural": "User_Service WITH Auth_Service VERSUS Rate_Limiter LEADS_TO Checkout_Flow"
    },
    "Database": {
        "unicode": "Raw_Data ⊕ Schema_Validation ⚡ Data_Quality_Rules → Clean_Data",
        "ascii_math": "Raw_Data + Schema_Validation * Data_Quality_Rules -> Clean_Data",
        "ascii_text": "Raw_Data _AND_ Schema_Validation _VS_ Data_Quality_Rules _TO_ Clean_Data",
        "natural": "Raw_Data WITH Schema_Validation VERSUS Data_Quality_Rules LEADS_TO Clean_Data"
    },
    "CI/CD": {
        "unicode": "Code_Commit ⊕ Unit_Tests ⚡ Coverage_Threshold → Build_Artifact",
        "ascii_math": "Code_Commit + Unit_Tests * Coverage_Threshold -> Build_Artifact",
        "ascii_text": "Code_Commit _AND_ Unit_Tests _VS_ Coverage_Threshold _TO_ Build_Artifact",
        "natural": "Code_Commit WITH Unit_Tests VERSUS Coverage_Threshold LEADS_TO Build_Artifact"
    },
    "Complex": {
        "unicode": "Order_Service ⊕ (Payment_Result ⊕ Availability_Check) → Order_Confirmation",
        "ascii_math": "Order_Service + (Payment_Result + Availability_Check) -> Order_Confirmation",
        "ascii_text": "Order_Service _AND_ (Payment_Result _AND_ Availability_Check) _TO_ Order_Confirmation",
        "natural": "Order_Service WITH (Payment_Result WITH Availability_Check) LEADS_TO Order_Confirmation"
    }
}

def estimate_tokens(text: str) -> int:
    """Estimate token count (rough approximation: ~4 chars per token, special handling for operators)"""
    # Count words and special characters separately
    words = text.split()
    word_tokens = len(words)
    
    # Special characters often tokenize separately
    special_chars = ['⊕', '⚡', '→', '+', '*', '->', '_AND_', '_VS_', '_TO_']
    special_count = sum(text.count(char) for char in special_chars)
    
    # Rough estimation: words + special tokens
    return word_tokens + special_count

def analyze_token_efficiency():
    """Analyze token efficiency for each operator approach"""
    results = {}
    
    for scenario, examples in test_cases.items():
        scenario_results = {}
        for approach, expression in examples.items():
            chars = len(expression)
            words = len(expression.split())
            tokens = estimate_tokens(expression)
            # Count semantic relationships (synthesis + tension + progress = 3)
            semantic_relationships = 3 if scenario != "Complex" else 4
            efficiency = tokens / semantic_relationships
            
            scenario_results[approach] = {
                "expression": expression,
                "chars": chars,
                "words": words,
                "tokens_est": tokens,
                "semantic_relationships": semantic_relationships,
                "tokens_per_relationship": round(efficiency, 2)
            }
        results[scenario] = scenario_results
    
    return results

def print_analysis():
    """Print formatted analysis results"""
    results = analyze_token_efficiency()
    
    print("# Token Efficiency Analysis Results")
    print("*Note: Token counts are estimates based on word and operator counting*\n")
    
    # Summary statistics
    approach_totals = {"unicode": 0, "ascii_math": 0, "ascii_text": 0, "natural": 0}
    approach_counts = {"unicode": 0, "ascii_math": 0, "ascii_text": 0, "natural": 0}
    approach_chars = {"unicode": 0, "ascii_math": 0, "ascii_text": 0, "natural": 0}
    
    for scenario, data in results.items():
        print(f"## {scenario} Scenario")
        print("| Approach | Chars | Words | Est. Tokens | Relationships | Tokens/Rel |")
        print("|----------|-------|-------|-------------|---------------|------------|")
        
        for approach, metrics in data.items():
            print(f"| {approach.replace('_', ' ').title()} | {metrics['chars']} | {metrics['words']} | {metrics['tokens_est']} | {metrics['semantic_relationships']} | {metrics['tokens_per_relationship']} |")
            approach_totals[approach] += metrics['tokens_est']
            approach_chars[approach] += metrics['chars']
            approach_counts[approach] += 1
        print()
    
    # Overall averages
    print("## Overall Token Efficiency")
    print("| Approach | Avg Chars | Avg Tokens | Avg Efficiency | Rank |")
    print("|----------|-----------|------------|----------------|------|")
    
    averages = []
    for approach, total in approach_totals.items():
        avg_tokens = total / approach_counts[approach]
        avg_chars = approach_chars[approach] / approach_counts[approach]
        avg_efficiency = avg_tokens / 3  # Average 3 relationships per expression
        averages.append((approach, avg_chars, avg_tokens, avg_efficiency))
    
    # Sort by efficiency (lower is better)
    averages.sort(key=lambda x: x[3])
    
    for rank, (approach, avg_chars, avg_tokens, avg_efficiency) in enumerate(averages, 1):
        print(f"| {approach.replace('_', ' ').title()} | {avg_chars:.0f} | {avg_tokens:.1f} | {avg_efficiency:.2f} | {rank} |")
    
    print("\n## Key Findings")
    print(f"- Most efficient: {averages[0][0].replace('_', ' ').title()} ({averages[0][3]:.2f} tokens/relationship)")
    print(f"- Least efficient: {averages[-1][0].replace('_', ' ').title()} ({averages[-1][3]:.2f} tokens/relationship)")
    print(f"- Efficiency difference: {((averages[-1][3] / averages[0][3]) - 1) * 100:.1f}% more tokens for least efficient")
    
    print("\n## Character Count Comparison")
    print("- Shortest expressions use ~{:.0f} characters".format(averages[0][1]))
    print("- Longest expressions use ~{:.0f} characters ({:.0f}% more)".format(
        averages[-1][1], 
        ((averages[-1][1] / averages[0][1]) - 1) * 100
    ))

if __name__ == "__main__":
    print_analysis()