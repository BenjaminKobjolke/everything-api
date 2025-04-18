# Everything Search API

A simple HTTP API for the Everything search engine.

## Overview

This API provides a simple HTTP interface to the Everything search engine, allowing you to search for files and folders on your Windows system through HTTP requests.

## Requirements

- Windows operating system
- [Everything](https://www.voidtools.com/) search engine installed and running
- Python 3.6 or higher
- Everything64.dll (included)

## Installation

1. Clone this repository or download the source code.

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

The API can be configured using the `settings.ini` file or command-line arguments.

### settings.ini

```ini
[Server]
host = localhost
port = 5000

[Search]
max_results = 100

[Logging]
level = INFO
log_file = everything_api.log
```

### Command-line Arguments

- `--config`: Path to configuration file (default: settings.ini)
- `--host`: Host to bind the server to (overrides config file)
- `--port`: Port to bind the server to (overrides config file)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--log-file`: Path to log file

## Usage

1. Start the Everything search engine.

2. Run the API server:

   ```
   python main.py
   ```

3. Make HTTP requests to search for files and folders:

   ```
   http://localhost:5000/everything-search-api/search?q=example
   ```

   By default, the search will match all words in the query. To match any of the words instead:

   ```
   http://localhost:5000/everything-search-api/search?q=shilo pdf 2025&match_all=false
   ```

### API Endpoints

#### GET /everything-search-api/search

Search for files and folders.

**Parameters:**

- `q` (required): Search query
  - The total length of all search terms combined must be at least 3 characters
  - If the total length is less than 3, the API will return an error with status code 400:
    ```json
    {
      "error": "Total length of search terms must be at least 3 characters. Current length: 2"
    }
    ```
- `limit` (optional): Maximum number of results to return (default: 100)
- `match_all` (optional): Whether to match all words in the query (default: true)
  - When set to `true` (default), the search will only return results that match all words in the query
  - When set to `false`, the search will return results that match any of the words in the query

**Example Response:**

```json
{
  "results": [
    {
      "filename": "example.txt",
      "path": "C:\\path\\to\\example.txt",
      "size": 1024,
      "date_modified": "2025-03-24T09:18:00"
    }
  ],
  "query": "example",
  "count": 1
}
```

When using `match_all=true` (the default), the API will filter results to ensure all search terms are present in the file path. The response includes:

```json
{
  "results": [...],
  "query": "shilo pdf 2025",
  "count": 8,
  "total_count": 42,
  "original_query": "shilo pdf 2025"
}
```

Where:

- `count`: The number of results after filtering (that match all search terms)
- `total_count`: The total number of results found by Everything before filtering
- `original_query`: The original query (included for reference)

## Helper Scripts

### install.bat

Installs the required dependencies.

```
install.bat
```

### run.bat

Runs the API server.

```
run.bat
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
