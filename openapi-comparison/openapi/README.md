# OpenAPI Demo

## Cách chạy

### 1. Dùng Swagger Editor

* Mở: https://editor.swagger.io/
* Paste file `openapi.yaml`

### 2. Dùng Swagger UI local

```bash
npm install -g swagger-ui-cli
swagger-ui-cli serve openapi.yaml
```

### 3. Generate server code

```bash
npm install @openapitools/openapi-generator-cli
npx openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-flask \
  -o server-python
```

### 4. Generate client code

```bash
npx openapi-generator-cli generate \
  -i openapi.yaml \
  -g javascript \
  -o client-js

cd client-python

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```
