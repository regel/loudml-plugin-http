# HTTP plug-in for LoudML

Add webhook capabilities to LoudML to make it send HTTP notifications on
anomaly detection.

## Setup

```bash
./setup.py install
```

## Coonfiguration

Define your webhook in a JSON file (e.g. `my-http-hook.json`):

```json
{
    "type": "http",
    "name": "my-http-hook",
    "config": {
        "method": "POST",
        "url": "http://your/url/"
    }
}
```
Submit it to LoudML:

```bash
curl -X PUT -H 'Content-Type: application/json' "localhost:8077/models/<model_name>/hooks" -d @my-http-hook.json
```

## Body format

### On anomaly detection

When an anomaly is detected, LoudML will send a query with this body:

```json
{
    "type": "anomaly_start",
    "model": <model_name>,
    "timestamp": <timestamp>,
    "score": <score>,
    "predicted": <predicted values>,
    "observed": <observed values>
}
```

Example:

```json
{
    "type": "anomaly_start",
    "model": "mymodel",
    "timestamp": 1526484353.267578,
    "score": 82,
    "predicted": {
        "foo": 18.0,
        "bar": 5.0
    }
    "observed": {
        "foo": 26.0,
        "bar": 1.0
    }
}
```

### When anomaly ends

When the anomaly ends, LoudML will send a query with this body:

```json
{
    "type": "anomaly_start",
    "model": <model_name>,
    "timestamp": <timestamp>,
    "score": <score>,
}
```

Example:

```json
{
    "type": "anomaly_start",
    "model": "mymodel",
    "timestamp": 1526485853.767845,
    "score": 68,
    "predicted": {
        "foo": 17.5,
        "bar": 5.1
    }
    "observed": {
        "foo": 17.2,
        "bar": 5.0
    }
}
```
