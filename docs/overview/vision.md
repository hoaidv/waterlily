We benchmark multiple databases in different scenarios and setups.

# What are possible scenarios and setups

We also call this a "benchmark context"

- Database type (MySQL, Cassandra, Vitess, MongoDB)
- Number of database instances
- Access pattern

# This choosen "benchmark Context"
- Platform = localhost (for all components benchmark scripts, app and db)
- Database type = MySQL
- Instance = 1
- Access pattern on a specific domain and problem
  + Request = READ
  + Throughput = HEAVY
  + Processing complexity = Medium

## Concrete problem
+ Domain e-commerce
+ We have a database of 35M products
+ We need to efficiently read from this database: 
  - By Id 
  - By many Ids

