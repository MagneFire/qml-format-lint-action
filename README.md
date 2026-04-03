# qmlformat lint action

Check and format QML files using `qmlformat`.

## Using

Create a file named `.github/workflows/lint.yml` and add:
```yaml
name: Lint

on:
  [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Check QML files
        uses: MagneFire/qml-format-lint-action@v1

```

## Using locally

Build the Docker image:
```sh
docker build -t qml-format-lint .
```

Navigate to the project where you wish to check the QML files and check them using:
```sh
docker run -it --rm --workdir /workdir -v $(pwd):/workdir qml-format-lint
```

Format QML files using:
```sh
docker run -it --rm --workdir /workdir -v $(pwd):/workdir qml-format-lint --fix
```