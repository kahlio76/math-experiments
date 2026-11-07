# Erdős Problem 13

Related to [Erdős Problem 13](https://www.erdosproblems.com/13). `maxA.py` uses MaxSAT to find the largest
A ⊆ {1, ..., N} where no element divides a sum of r larger elements of A (repeats allowed), and prints how
far it exceeds N/(r+1).

    python3 maxA.py <r> <N start> <N end> <step>
