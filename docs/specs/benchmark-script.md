
# Benchmark script design

For each chosen "benchmark context", benchmark script should be able to 

+ Using `lua` script and `wrk` utility
+ Benchmark the application with different CCU by flag `--connections`
+ Export result to json file, including
  * The "benchmark context" (platform, database type, number of instances, access pattern)
  * The benchmark aspects
    - Different APIs (get one product, get many products)
    - Different CCUs (100, 1000, 10000, 100000)
  * The benchmark result of each combination of aspects (API + CCU)
    - Requests per second (RPS) or Transaction per second (TPS)
    - Latency (min, avg, max, std)
    - Size of transfered data (MB or GB or TB)
  * The result should be easy to be aggregated & visualized
    - Visualize & compare RPS/TPS of selected "BENCHMARK CONTEXT", API, CCU
    - Visualize the change of RPS/TPS of a specific API, with increasing CCU

