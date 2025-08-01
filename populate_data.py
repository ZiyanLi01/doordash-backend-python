from database import SessionLocal, engine
from models import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker

# Create tables
Base.metadata.create_all(bind=engine)

# Sample restaurant data with images
restaurants_data = [
    {
        "name": "Pizza Palace",
        "description": "Authentic Italian pizza with fresh ingredients and wood-fired ovens",
        "address": "123 Main St, Downtown",
        "phone": "(555) 123-4567",
        "cuisine_type": "Italian",
        "rating": 4.5,
        "delivery_fee": 2.99,
        "minimum_order": 15.00,
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop"
    },
    {
        "name": "Sushi Express",
        "description": "Fresh sushi and Japanese cuisine made with premium ingredients",
        "address": "456 Oak Ave, Midtown",
        "phone": "(555) 234-5678",
        "cuisine_type": "Japanese",
        "rating": 4.7,
        "delivery_fee": 3.99,
        "minimum_order": 20.00,
        "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop"
    },
    {
        "name": "Burger Barn",
        "description": "Juicy burgers, crispy fries, and classic American comfort food",
        "address": "789 Pine St, Westside",
        "phone": "(555) 345-6789",
        "cuisine_type": "American",
        "rating": 4.2,
        "delivery_fee": 1.99,
        "minimum_order": 12.00,
        "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop"
    },
    {
        "name": "Taco Fiesta",
        "description": "Authentic Mexican tacos, burritos, and fresh salsas",
        "address": "321 Elm St, Eastside",
        "phone": "(555) 456-7890",
        "cuisine_type": "Mexican",
        "rating": 4.4,
        "delivery_fee": 2.49,
        "minimum_order": 10.00,
        "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&h=300&fit=crop"
    },
    {
        "name": "Thai Garden",
        "description": "Traditional Thai cuisine with aromatic spices and fresh herbs",
        "address": "654 Maple Dr, Northside",
        "phone": "(555) 567-8901",
        "cuisine_type": "Thai",
        "rating": 4.6,
        "delivery_fee": 3.49,
        "minimum_order": 18.00,
        "image_url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400&h=300&fit=crop"
    }
]

# Sample menu items data for each restaurant with image URLs
menu_items_data = {
    "Pizza Palace": [
        {"name": "Margherita Pizza", "description": "Fresh mozzarella, tomato sauce, and basil", "price": 16.99, "category": "Pizza", "image_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=400&h=300&fit=crop"},
        {"name": "Pepperoni Pizza", "description": "Classic pepperoni with melted cheese", "price": 18.99, "category": "Pizza", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop"},
        {"name": "Garlic Bread", "description": "Crispy bread with garlic butter and herbs", "price": 6.99, "category": "Sides", "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop"},
        {"name": "Caesar Salad", "description": "Fresh romaine lettuce with Caesar dressing", "price": 12.99, "category": "Salads", "image_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop"},
        {"name": "Tiramisu", "description": "Classic Italian dessert with coffee and mascarpone", "price": 8.99, "category": "Desserts", "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop"}
    ],
    "Sushi Express": [
        {"name": "California Roll", "description": "Crab, avocado, and cucumber roll", "price": 12.99, "category": "Rolls", "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop"},
        {"name": "Salmon Nigiri", "description": "Fresh salmon over seasoned rice", "price": 8.99, "category": "Nigiri", "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop"},
        {"name": "Miso Soup", "description": "Traditional Japanese soup with tofu", "price": 4.99, "category": "Soups", "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop"},
        {"name": "Tempura Shrimp", "description": "Crispy battered shrimp with dipping sauce", "price": 14.99, "category": "Appetizers", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop"},
        {"name": "Green Tea Ice Cream", "description": "Smooth matcha ice cream", "price": 6.99, "category": "Desserts", "image_url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop"}
    ],
    "Burger Barn": [
        {"name": "Classic Cheeseburger", "description": "Juicy beef patty with cheese and fresh veggies", "price": 11.99, "category": "Burgers", "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop"},
        {"name": "Bacon Deluxe", "description": "Double patty with bacon and special sauce", "price": 15.99, "category": "Burgers", "image_url": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=400&h=300&fit=crop"},
        {"name": "French Fries", "description": "Crispy golden fries with sea salt", "price": 4.99, "category": "Sides", "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=300&fit=crop"},
        {"name": "Onion Rings", "description": "Beer-battered onion rings", "price": 5.99, "category": "Sides", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop"},
        {"name": "Chocolate Milkshake", "description": "Thick and creamy chocolate shake", "price": 6.99, "category": "Drinks", "image_url": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=300&fit=crop"}
    ],
    "Taco Fiesta": [
        {"name": "Street Tacos", "description": "Three authentic street tacos with choice of meat", "price": 9.99, "category": "Tacos", "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&h=300&fit=crop"},
        {"name": "Beef Burrito", "description": "Large burrito with rice, beans, and beef", "price": 12.99, "category": "Burritos", "image_url": "https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=400&h=300&fit=crop"},
        {"name": "Guacamole & Chips", "description": "Fresh guacamole with crispy tortilla chips", "price": 7.99, "category": "Appetizers", "image_url": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400&h=300&fit=crop"},
        {"name": "Quesadilla", "description": "Cheese quesadilla with pico de gallo", "price": 10.99, "category": "Quesadillas", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop"},
        {"name": "Horchata", "description": "Traditional Mexican rice drink", "price": 4.99, "category": "Drinks", "image_url": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=300&fit=crop"}
    ],
    "Thai Garden": [
        {"name": "Pad Thai", "description": "Stir-fried rice noodles with shrimp and peanuts", "price": 16.99, "category": "Noodles", "image_url": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400&h=300&fit=crop"},
        {"name": "Green Curry", "description": "Spicy green curry with coconut milk and vegetables", "price": 18.99, "category": "Curries", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop"},
        {"name": "Spring Rolls", "description": "Fresh vegetables wrapped in rice paper", "price": 8.99, "category": "Appetizers", "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop"},
        {"name": "Tom Yum Soup", "description": "Hot and sour soup with shrimp", "price": 12.99, "category": "Soups", "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop"},
        {"name": "Mango Sticky Rice", "description": "Sweet sticky rice with fresh mango", "price": 7.99, "category": "Desserts", "image_url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop"}
    ]
}

def populate_database():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(MenuItem).delete()
        db.query(Restaurant).delete()
        db.commit()
        
        # Add restaurants
        restaurants = []
        for restaurant_data in restaurants_data:
            restaurant = Restaurant(**restaurant_data)
            db.add(restaurant)
            db.flush()  # This gets the ID
            restaurants.append(restaurant)
        
        # Add menu items for each restaurant
        for restaurant in restaurants:
            restaurant_name = restaurant.name
            if restaurant_name in menu_items_data:
                for item_data in menu_items_data[restaurant_name]:
                    menu_item = MenuItem(
                        **item_data,
                        restaurant_id=restaurant.id,
                        is_available=True
                    )
                    db.add(menu_item)
        
        db.commit()
        print("✅ Database populated successfully!")
        print(f"📊 Added {len(restaurants)} restaurants with images")
        print(f"🍽️  Added {len(restaurants) * 5} menu items with images")
        
        # Print summary
        for restaurant in restaurants:
            menu_count = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant.id).count()
            print(f"   • {restaurant.name}: {menu_count} items")
            
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database() 