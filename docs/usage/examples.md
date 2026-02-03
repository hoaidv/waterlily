
Extract product IDs from database using the preset database connection.

```sh
./gradlew extractProductIds -PproductCount=10000000
```

Install & Start prometheus

```sh
brew install prometheus
brew services start prometheus
```

Stop & Not start at Login prometheus

```sh
# stops the service
brew services stop prometheus
# cleans up, so that it does not restart on login
brew services cleanup
```

Install & Start grafana

```sh
brew install grafana
brew services start grafana
```