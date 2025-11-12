import os
import pytest
from browser_server import search, open_link, find_pattern, AppContext


@pytest.fixture
def app_context():
    """Create an AppContext for testing"""
    return AppContext()


@pytest.fixture
def mock_context(app_context):
    """Create a mock Context with necessary attributes"""
    class MockRequestContext:
        def __init__(self, lifespan_context):
            self.lifespan_context = lifespan_context

    class MockContext:
        def __init__(self):
            self.client_id = "test-client-123"
            self.request_context = MockRequestContext(app_context)

    return MockContext()


@pytest.mark.asyncio
async def test_search_basic(mock_context):
    """Test basic search functionality"""
    # Test a simple search query
    result = await search(mock_context, query="Python programming", topn=5)

    # Verify we got a non-empty result
    assert result is not None
    assert len(result) > 0
    assert isinstance(result, str)

    # Check that result contains expected content markers
    # Browser results typically contain cursor markers like [0], [1], etc.
    assert "[" in result or "†" in result or "http" in result.lower()




@pytest.mark.asyncio
async def test_open_url(mock_context):
    """Test opening a URL directly"""
    # Test opening a well-known URL
    result = await open_link(
        mock_context,
        id="https://www.example.com",
        source="web"
    )

    assert result is not None
    assert len(result) > 0
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_open_after_search(mock_context):
    """Test opening a link from search results"""
    # First perform a search
    search_result = await search(mock_context, query="Python", topn=3)
    assert search_result is not None

    # Then try to open the first result (cursor=0, id=0)
    open_result = await open_link(mock_context, id=0, cursor=0)

    assert open_result is not None
    assert len(open_result) > 0


@pytest.mark.asyncio
async def test_find_pattern(mock_context):
    """Test finding a pattern in a page"""
    # First open a page
    await open_link(
        mock_context,
        id="https://www.example.com",
        source="web"
    )

    # Then search for a common pattern
    result = await find_pattern(mock_context, pattern="example")

    assert result is not None
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_find_pattern_not_found(mock_context):
    """Test finding a pattern that doesn't exist"""
    # First open a page
    await open_link(
        mock_context,
        id="https://www.example.com",
        source="web"
    )

    # Search for a pattern that likely doesn't exist
    result = await find_pattern(mock_context, pattern="xyzabc123notfound")

    assert result is not None
    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_session_isolation():
    """Test that different sessions maintain separate browsers"""
    app_context = AppContext()

    # Create two different mock contexts with different client IDs
    class MockRequestContext:
        def __init__(self, lifespan_context):
            self.lifespan_context = lifespan_context

    class MockContext1:
        def __init__(self):
            self.client_id = "client-1"
            self.request_context = MockRequestContext(app_context)

    class MockContext2:
        def __init__(self):
            self.client_id = "client-2"
            self.request_context = MockRequestContext(app_context)

    ctx1 = MockContext1()
    ctx2 = MockContext2()

    # Perform searches with both contexts
    result1 = await search(ctx1, query="Python", topn=3)
    result2 = await search(ctx2, query="JavaScript", topn=3)

    # Verify both got results
    assert result1 is not None
    assert result2 is not None

    # Verify separate browser instances were created
    assert "client-1" in app_context.browsers
    assert "client-2" in app_context.browsers
    assert app_context.browsers["client-1"] is not app_context.browsers["client-2"]


@pytest.mark.asyncio
async def test_browser_backend_selection():
    """Test that browser backend can be selected via environment variable"""
    # Test with default backend (exa)
    app_context = AppContext()
    browser = app_context.create_or_get_browser("test-session")

    assert browser is not None
    assert hasattr(browser, 'backend')


def test_app_context_remove_browser():
    """Test removing a browser from app context"""
    app_context = AppContext()

    # Create a browser
    browser = app_context.create_or_get_browser("test-session")
    assert "test-session" in app_context.browsers

    # Remove it
    app_context.remove_browser("test-session")
    assert "test-session" not in app_context.browsers

    # Remove non-existent browser (should not raise error)
    app_context.remove_browser("non-existent-session")
