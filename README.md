# Association Rule Mining: Apriori Algorithm

This Python project implements the Apriori algorithm to find frequent itemsets and generate association rules from a dataset of online shopping behavior. The goal is to identify products that are frequently browsed together by customers, which can be used for cross-selling and product recommendations.

## Project Structure

The project consists of a single Python file and an input data file (`browsing.txt`).

-   **`main.py`:** Contains the Python code implementing the Apriori algorithm.
-   **`browsing.txt`:** The input dataset where each line represents a browsing session, and item IDs are separated by spaces.
-   **`results.txt`:** The output file where the frequent itemsets and top association rules are written.

## Algorithm Implementation

The code implements the Apriori algorithm with the following steps:

1.  **Data Loading:** Reads the `browsing.txt` file and processes each line into a list of browsed item IDs.
2.  **Finding Frequent Itemsets:**
    -   Identifies frequent 1-itemsets based on a minimum support threshold (`MIN_SUPPORT = 100`).
    -   Iteratively finds frequent k-itemsets (k=2 and 3) by generating candidates from the frequent (k-1)-itemsets and pruning those that do not meet the minimum support.
3.  **Generating Association Rules:**
    -   Generates potential association rules from the frequent 2-itemsets and 3-itemsets.
4.  **Calculating Confidence:**
    -   Calculates the confidence for each generated rule. Confidence is defined as `support(X union Y) / support(X)` for a rule `X => Y`.
    -   Filters rules based on a minimum confidence threshold (`MIN_CONFIDENCE = 0.75`).
5.  **Output:**
    -   Writes the number of frequent k-itemsets (for k=1, 2, and 3) to `results.txt`.
    -   Writes the top 5 association rules for pairs (2-itemsets) and triples (3-itemsets) to `results.txt`, sorted by confidence in descending order.

## How to Run

1.  **Save the code:** Save the provided Python code as a `.py` file (e.g., `main.py`).
2.  **Ensure `browsing.txt` exists:** Make sure the `browsing.txt` file is in the same directory as your Python script, as the code is currently set to look for it there.
3.  **Run the script:** Open a terminal or command prompt, navigate to the directory where you saved the files, and run the script using the Python interpreter:

    ```bash
    python your_script_name.py
    ```

    Replace `your_script_name.py` with the actual name of your Python file (e.g., `main.py`).

4.  **Check the output:** The script will print a confirmation message to the console indicating that the results have been written to `results.txt`. Open the `results.txt` file to view the frequent itemsets and the top 5 association rules for pairs and triples.

## Global Variables

-   `MIN_SUPPORT = 100`: The minimum number of times an itemset must appear in the sessions to be considered frequent.
-   `MIN_CONFIDENCE = 0.75`: The minimum confidence (as a fraction) for an association rule to be included in the top 5 lists.

## Output

The script will generate a file named `results.txt` in the same directory as the script. This file will contain:

-   The count of frequent 1-itemsets, 2-itemsets, and 3-itemsets found.
-   The top 5 association rules for pairs with a confidence of 75% or higher, sorted by confidence (descending).
-   The top 5 association rules for triples with a confidence of 75% or higher, sorted by confidence (descending).

## Notes

-   The code uses the absolute path to find `browsing.txt` and `results.txt`, making it less dependent on the working directory when the script is run.
-   The sorting of the top 5 rules for both pairs and triples is based on confidence in decreasing order. Ties are broken based on the lexicographical order of the items in the antecedent.