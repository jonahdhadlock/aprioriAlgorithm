# --- Association Rule Mining: Apriori Algorithm ---

# Import the necessary tools
from itertools import combinations
from collections import Counter
import os

# Define GLOBAL variables for the minimum support and confidence of frequent k-itemsets
MIN_SUPPORT = 100
MIN_CONFIDENCE = 0.75

# Specify the absolute path to browsing.txt
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'browsing.txt')

# Read the file into the program for analysis
def custom_read() -> list:
    with open(file_path, 'r') as file:
        return [line.strip().split() for line in file]


# Find frequent 1-itemsets
def find_frequent_one_itemsets(sessions: list) -> dict:
    item_counts = Counter(item for session in sessions for item in session)
    return {frozenset([item]): count for item, count in item_counts.items() if count >= MIN_SUPPORT}


# Find and prune k-itemsets
def find_next_frequent_itemsets(sessions: list, prev_frequent_itemsets: dict, k: int) -> dict:
    frequent_items_from_prev_step = set(item for itemset in prev_frequent_itemsets for item in itemset)
    itemset_counts = Counter()

    for session in sessions:
        frequent_items_in_session = [item for item in session if item in frequent_items_from_prev_step]
        if len(frequent_items_in_session) >= k:
            for combo in combinations(frequent_items_in_session, k):
                itemset_counts[frozenset(combo)] += 1

    return {itemset: count for itemset, count in itemset_counts.items() if count >= MIN_SUPPORT}


# Generate all possible association rules from a given set of frequent itemsets
def generate_association_rules(frequent_itemsets: dict) -> list:
    all_rules = []
    for itemset, support_count in frequent_itemsets.items():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    all_rules.append((antecedent, consequent, support_count))
    return all_rules


# Calculate confidence for rules and filter by the minimum threshold
def calculate_confidence(all_rules: list, all_frequent_itemsets: dict) -> list:
    confident_rules = []
    for antecedent, consequent, itemset_support_count in all_rules:
        antecedent_support_count = all_frequent_itemsets.get(antecedent)

        if antecedent_support_count:
            confidence = itemset_support_count / antecedent_support_count
            if confidence >= MIN_CONFIDENCE:
                confident_rules.append((antecedent, consequent, confidence))
    return confident_rules


# --- Writes separate top 5 lists for pairs and triples ---
def custom_write(frequent_itemsets: dict, rules_2s: list, rules_3s: list):
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.txt')
    with open(output_path, 'w') as output_file:
        for k, itemsets in frequent_itemsets.items():
            print(f"--- Found {len(itemsets)} Frequent {k}-Itemsets ---", file=output_file)

        # Format and print rules
        print_rule_set = lambda rule_list, title: (
            print(f"\n{title}", file=output_file),
            [print(f"{i + 1}. {{{', '.join(rule[0])}}} -> {{{', '.join(rule[1])}}}, Confidence: {rule[2]:.6f}",
                   file=output_file) for i, rule in enumerate(rule_list[:5])] if rule_list else print(
                "No rules met the minimum confidence threshold.", file=output_file)
        )

        print_rule_set(rules_2s, "--- Top 5 Association Rules for Pairs (Confidence >= 75%) ---")
        print_rule_set(rules_3s, "--- Top 5 Association Rules for Triples (Confidence >= 75%) ---")

    return output_path


# --- Orchestrates separate processing for each rule type ---
def main():
    sessions = custom_read()

    # Steps 1, 2, 3: Find all frequent itemsets
    frequent_1s = find_frequent_one_itemsets(sessions)
    frequent_2s = find_next_frequent_itemsets(sessions, frequent_1s, 2)
    frequent_3s = find_next_frequent_itemsets(sessions, frequent_2s, 3)

    all_frequent_itemsets = {**frequent_1s, **frequent_2s, **frequent_3s}
    sort_key = lambda rule: (-rule[2], sorted(list(rule[0])))

    # Process rules from 2-itemsets
    potential_rules_2s = generate_association_rules(frequent_2s)
    confident_rules_2s = calculate_confidence(potential_rules_2s, all_frequent_itemsets)
    sorted_rules_2s = sorted(confident_rules_2s, key=sort_key)

    # Process rules from 3-itemsets
    potential_rules_3s = generate_association_rules(frequent_3s)
    confident_rules_3s = calculate_confidence(potential_rules_3s, all_frequent_itemsets)
    sorted_rules_3s = sorted(confident_rules_3s, key=sort_key)

    # Output the results to an external .txt file
    output_path = custom_write(
        {1: frequent_1s, 2: frequent_2s, 3: frequent_3s},
        sorted_rules_2s,
        sorted_rules_3s
    )

    print(f"Successfully wrote results to: {output_path}")


if __name__ == "__main__":
    main()