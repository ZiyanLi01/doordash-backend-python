from database import SessionLocal
from models import MenuItem

def update_menu_item_image(menu_item_name, new_image_url):
    db = SessionLocal()
    try:
        # Find the menu item by name
        menu_item = db.query(MenuItem).filter(MenuItem.name == menu_item_name).first()
        
        if menu_item:
            # Update the image URL
            menu_item.image_url = new_image_url
            db.commit()
            print(f"✅ Updated image for '{menu_item_name}' to: {new_image_url}")
        else:
            print(f"❌ Menu item '{menu_item_name}' not found")
            
    except Exception as e:
        print(f"❌ Error updating image: {e}")
        db.rollback()
    finally:
        db.close()

# Example usage
if __name__ == "__main__":
    # Update Pepperoni Pizza image
    update_menu_item_image("Pepperoni Pizza", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop")
    
    # Update Garlic Bread image
    update_menu_item_image("Garlic Bread", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=300&fit=crop")
    
    # Update Tempura Shrimp image
    update_menu_item_image("Tempura Shrimp", "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?w=400&h=300&fit=crop")
    
    # Update Salmon Nigiri image
    update_menu_item_image("Salmon Nigiri", "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop")
    
    # Update Onion Rings image
    update_menu_item_image("Onion Rings", "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=300&fit=crop")
    
    # Update Quesadilla image
    update_menu_item_image("Quesadilla", "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop")
    
    # Update Green Curry image
    update_menu_item_image("Green Curry", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop")
    
    # Update Spring Rolls image
    update_menu_item_image("Spring Rolls", "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=400&h=300&fit=crop")
    
    print("🎉 All menu item images updated!") 