## 2024-05-24 - Pre-compile Regex
**Learning:** Pre-compiling static regex expressions avoids recompilation overhead on each method invocation.
**Action:** When a function does repetitive regex searches against static patterns, precompile them globally or at class level.
