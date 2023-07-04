# Projeto Inicial HAPI-FHIR

Este projeto é um projeto inicial completo que você pode usar para implantar um servidor FHIR usando HAPI FHIR JPA.

## Pré-requisitos
 - Docker, pois todo o projeto pode ser construído usando o docker de vários estágios (com JDK e maven agrupados no docker)

## Executando via Docker

```
docker pull hapiproject/hapi:latest
docker run -p 8080:8080 hapiproject/hapi:latest
```

Isso executará a imagem do docker com a configuração padrão, mapeando a porta 8080 do contêiner para a porta 8080 no host. Após a execução, você pode acessar `http://localhost:8080/` no navegador para acessar a IU do servidor HAPI FHIR ou usar `http://localhost:8080/fhir/` como URL base para suas solicitações REST.

### Exemplo usando ``docker-compose.yml`` para docker-compose

```yaml
version: '3.7'

services:
  fhir:
    container_name: fhir
    image: "hapiproject/hapi:latest"
    ports:
      - "8080:8080"
    configs:
      - source: hapi
        target: /app/config/application.yaml
    depends_on:
      - db


  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_PASSWORD: admin
      POSTGRES_USER: admin
      POSTGRES_DB: hapi
    volumes:
      - ./hapi.postgress.data:/var/lib/postgresql/data

configs:
  hapi:
     file: ./hapi.application.yaml
```

Forneça o seguinte conteúdo em ``./hapi.aplication.yaml``:

```yaml
spring:
  datasource:
    url: 'jdbc:postgresql://db:5432/hapi'
    username: admin
    password: admin
    driverClassName: org.postgresql.Driver
  jpa:
    properties:
      hibernate.dialect: ca.uhn.fhir.jpa.model.dialect.HapiFhirPostgres94Dialect
      hibernate.search.enabled: false
```