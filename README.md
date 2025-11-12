# MCP Browser Server

An MCP (Model Context Protocol) server that provides web browsing and search capabilities. This tool allows language models to search the web, open links, and navigate web pages.

## Features

- **Web search**: Search for information using YouCom or Exa backends
- **Link navigation**: Open and navigate to specific URLs
- **Pattern matching**: Find specific patterns within web pages
- **Session management**: Maintains browsing state per client session
- **Citation support**: Enables proper citation of web sources

## Installation

```bash
cd mcp-browser
uv pip install -e .
```

## Usage

### Running the Server

```bash
python browser_server.py
```

The server will start on port **8001**.

### Environment Variables

- `BROWSER_BACKEND` (optional): Choose backend - "exa" (default) or "youcom"
- Backend-specific API keys may be required (e.g., `EXA_API_KEY`)

### API

#### `search`

Search for information related to a query and display top results.

**Parameters:**
- `query` (string, required): Search query
- `topn` (integer, optional): Number of results to display (default: 10)
- `source` (string, optional): Source filter

**Returns:** Formatted search results with cursor indices

#### `open`

Open a link or navigate to a specific page location.

**Parameters:**
- `id` (integer/string, optional): Link ID or fully qualified URL
- `cursor` (integer, optional): Page cursor from previous search
- `loc` (integer, optional): Line number to start viewing
- `num_lines` (integer, optional): Number of lines to display
- `view_source` (boolean, optional): View page source
- `source` (string, optional): Source specification

**Returns:** Page content with line numbers

#### `find`

Find exact matches of a pattern in the current page.

**Parameters:**
- `pattern` (string, required): Pattern to search for
- `cursor` (integer, optional): Page cursor

**Returns:** Matches with line numbers

### Citation Format

Information from the browser tool should be cited using:
- `【{cursor}†L{line_start}(-L{line_end})?】`
- Examples: `【6†L9-L11】` or `【8†L3】`

## Dependencies

- mcp
- fastapi>=0.116.1
- uvicorn>=0.35.0
- gpt-oss (for SimpleBrowserTool implementation)

## Architecture

The browser server depends on the main `gpt-oss` package for the `SimpleBrowserTool` implementation, which provides the actual browsing functionality with support for multiple backends (YouCom, Exa).

## Testing

### Setup

1. Install test dependencies:
```bash
uv pip install -e ".[test]"
```

2. Configure environment variables by copying `.env.example` to `.env`:
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
   - `EXA_API_KEY` - Required if using Exa backend (default)
   - `YDC_API_KEY` - Required if using YouCom backend

### Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_browser_server.py
```

Run specific test:
```bash
pytest tests/test_browser_server.py::test_search_basic -v
```

### Test Coverage

The test suite covers:
- **Search functionality**: Basic search, different result counts, empty queries
- **Link navigation**: Opening URLs directly, navigating search results
- **Pattern matching**: Finding patterns in pages, handling missing patterns
- **Session management**: Browser isolation between different client sessions
- **Backend selection**: Environment-based backend configuration

**Note**: Tests make real API calls and require valid API keys. Test results depend on live API responses and may vary.

## License

See the main gpt-oss repository for license information.
