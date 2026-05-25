# Benchmark Ktor + PostgreSQL + Near Cache

This project is created to benchmark the Ktor + PostgreSQL + Cache stack by simulating an real e-commerce scenario, 
where products are read intensively by their ID (one and many IDs)
- A full product entity with variants, medias and attributes is read for each request (1 request -> 4 DB queries)
- More than 40 million products, download from [Amazon-Reviews-2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)
- Cache in-memory
- Simmulate cases where cache-hit = { 87.5%, 90%, ... 95% } with [Rayleigh_distribution](https://en.wikipedia.org/wiki/Rayleigh_distribution)

