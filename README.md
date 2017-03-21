# 8-puzzle_benchmark

Comparison of different algorithms used to solve 8-puzzle problem

#### Algorithm implemented

1. [x] BFS.
2. [x] IDDFS.
3. [x] A* with misplaced heuristic.
4. [x] A* with manhattan heuristic.

**Test Case**

|Board| \ \  \ | \ \ \ | \ \ \ | Target| \ \ \ | \ \ \ | 
| --- | --- | --- | --- | --- | --- | --- |
|7|2|4| \ \ \ |1|2|3|  
|5|0|6| \ \ \ |4|5|6|
|8|3|1| \ \ \ |7|8|0|

**Result**

|Algorithm|Time|Queue size|Correctness|
| --- | --- | --- | --- |
|Uniformed BFS|`3min15s`|37790|✔️|
|Iterative Deepening DFS|`34.60s`|8511|✔️|
|A* with misplaced heuristic|`0.68s`|1537|✔️|
|A* with misplaced heuristic|`0.09s`|209|✔️|


### Usage

```bash
https://github.com/memoiry/8-puzzle-benchmark
cd 8-puzzle-benchmark
python 8-puzzle.py
```

<p align="center"><img src="https://ooo.0o0.ooo//2017//03//21//58d12ac09ebd7.png" width="480"></p>

### Conclusion
It can be seen that A* with manhattan distance has the best performance, which only needs 0.09s and has a 209 queue size.

IDDFS has a better Queue size computing time reduction compared to BFS.

