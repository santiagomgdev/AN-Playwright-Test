from playwright.sync_api import expect

def test_hu01_dashboard_loads(authenticated_page):
    authenticated_page.goto("/vinculaciones")
    expect(authenticated_page.get_by_role("heading", name="Gestion de vinculaciones")).to_be_visible()