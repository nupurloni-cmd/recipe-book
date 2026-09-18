from app import app, recipes


def client():
    """Configures the Flask test client and resets data before each test."""
    app.config["TESTING"] = True
    recipes.clear()
    return app.test_client()


# Test 1: Health route returns status ok
def test_health():
    c = client()
    response = c.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


# Test 2: Valid form submission adds a recipe and updates the API route
def test_add_recipe_success():
    c = client()
    response = c.post(
        "/add",
        data={
            "name": "Paneer Tikka",
            "ingredient": "Paneer, Spices",
            "category": "Starters",
        },
    )
    assert response.status_code == 302  # Redirects back to home

    api_res = c.get("/api/recipes")
    assert len(api_res.json) == 1
    assert api_res.json[0]["name"] == "Paneer Tikka"
    assert api_res.json[0]["category"] == "Starters"


# Test 3: Invalid input (missing required fields) is rejected
def test_invalid_input_rejected():
    c = client()
    response = c.post(
        "/add",
        data={"name": "", "ingredient": "Salt", "category": "Starters"},
    )
    assert response.status_code == 400  # Bad Request
