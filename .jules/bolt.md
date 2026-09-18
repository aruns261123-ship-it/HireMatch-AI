## 2025-02-12 - String Concatenation Optimization
**Learning:** String concatenation using `+=` inside a loop can lead to O(n^2) time complexity due to immutability of strings in Python, although CPython has internal optimizations that might mitigate this in some cases.
**Action:** Use `list.append()` to collect string parts and `''.join()` (or `'\n'.join()`) to concatenate them into a single string to guarantee O(n) performance.
