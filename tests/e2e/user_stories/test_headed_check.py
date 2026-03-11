def test_browser_is_visible(authenticated_page):
    import time
    authenticated_page.goto("/")
    time.sleep(5)  # force the browser to stay open 5 seconds