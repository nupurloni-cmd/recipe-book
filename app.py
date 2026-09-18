import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Expanded realistic restaurant menu
recipes = [
    # Starters
    {
        "name": "Paneer Tikka Angaara",
        "ingredient": "Cottage Cheese, Bell Peppers, Smoked Spices, Yogurt",
        "category": "Starters",
    },
    {
        "name": "Crispy Veg Spring Rolls",
        "ingredient": "Shredded Cabbage, Carrots, Glass Noodle",
        "category": "Starters",
    },
    {
        "name": "Hara Bhara Kabab",
        "ingredient": "Spinach, Green Peas, Potatoes, Mint Chutney",
        "category": "Starters",
    },
    {
        "name": "Garlic Butter Mushrooms",
        "ingredient": "Button Mushrooms, Garlic Butter, Parsley, Herbs",
        "category": "Starters",
    },
    # Main Course
    {
        "name": "Paneer Butter Masala",
        "ingredient": "Paneer, Rich Tomato Gravy, Fresh Cream, Butter",
        "category": "Main Course",
    },
    {
        "name": "Dal Makhani",
        "ingredient": "Slow-cooked Black Lentils, Kidney Beans, Butter",
        "category": "Main Course",
    },
    {
        "name": "Veg Dum Biryani",
        "ingredient": "Aromatic Basmati Rice, Mixed Vegetables, Saffron",
        "category": "Main Course",
    },
    {
        "name": "Kadhai Mushroom",
        "ingredient": "Mushrooms, Capsicum, Onion Gravy, Ground Spices",
        "category": "Main Course",
    },
    {
        "name": "Pasta Arrabbiata",
        "ingredient": "Penne Pasta, Tomato Sauce, Garlic, Chili Flakes",
        "category": "Main Course",
    },
    # Desserts
    {
        "name": "Saffron Gulab Jamun",
        "ingredient": "Milk Solids, Cardamom Sugar Syrup, Pistachio",
        "category": "Desserts",
    },
    {
        "name": "Sizzling Chocolate Brownie",
        "ingredient": "Dark Chocolate Cake, Hot Fudge, Vanilla Ice Cream",
        "category": "Desserts",
    },
    {
        "name": "Rasmalai Delight",
        "ingredient": "Soft Cottage Cheese Patties, Saffron Milk, Almonds",
        "category": "Desserts",
    },
    # Beverages
    {
        "name": "Fresh Mint Lime Mojito",
        "ingredient": "Crushed Mint, Lime Juice, Soda, Brown Sugar",
        "category": "Beverages",
    },
    {
        "name": "Mango Lassi",
        "ingredient": "Mango Pulp, Fresh Yogurt, Cardamom, Ice",
        "category": "Beverages",
    },
    {
        "name": "Cold Coffee with Ice Cream",
        "ingredient": "Brewed Espresso, Chilled Milk, Vanilla Scoop",
        "category": "Beverages",
    },
]

COMMIT = os.getenv("RENDER_GIT_COMMIT", "local")[:7]


@app.route("/")
def home():
    categories = ["Starters", "Main Course", "Desserts", "Beverages"]
    grouped_recipes = {
        cat: [r for r in recipes if r["category"] == cat] for cat in categories
    }

    other_recipes = [r for r in recipes if r.get("category") not in categories]
    if other_recipes:
        grouped_recipes["Chef's Specials"] = other_recipes

    return render_template(
        "index.html",
        grouped_recipes=grouped_recipes,
        categories=categories,
        commit=COMMIT,
    )


@app.route("/add", methods=["POST"])
def add_recipe():
    name = request.form.get("name", "").strip()
    ingredient = request.form.get("ingredient", "").strip()
    category = request.form.get("category", "Main Course").strip()

    if not name or not ingredient:
        return "Recipe name and ingredients are required!", 400

    recipes.append(
        {"name": name, "ingredient": ingredient, "category": category}
    )
    return redirect("/")


@app.route("/api/recipes")
def api_recipes():
    return jsonify(recipes)


@app.route("/health")
def health():
    return {"status": "ok", "commit": COMMIT}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

# Enhanced routing configuration
