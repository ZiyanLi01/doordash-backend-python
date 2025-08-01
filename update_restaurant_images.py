from database import SessionLocal
from models import Restaurant

def update_restaurant_image(restaurant_name, new_image_url):
    db = SessionLocal()
    try:
        # Find the restaurant by name
        restaurant = db.query(Restaurant).filter(Restaurant.name == restaurant_name).first()
        
        if restaurant:
            # Update the image URL
            restaurant.image_url = new_image_url
            db.commit()
            print(f"✅ Updated banner image for '{restaurant_name}' to: {new_image_url}")
        else:
            print(f"❌ Restaurant '{restaurant_name}' not found")
            
    except Exception as e:
        print(f"❌ Error updating restaurant image: {e}")
        db.rollback()
    finally:
        db.close()

# Example usage
if __name__ == "__main__":
    # Update all restaurants with much wider banner images to fill any screen width
    update_restaurant_image("Sushi Express", "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=2400&h=400&fit=crop")
    update_restaurant_image("Pizza Palace", "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=2400&h=400&fit=crop")
    update_restaurant_image("Burger Barn", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=2400&h=400&fit=crop")
    update_restaurant_image("Taco Fiesta", "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=2400&h=400&fit=crop")
    update_restaurant_image("Thai Garden", "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=2400&h=400&fit=crop")
    
    print("🎉 Restaurant banner images updated!") 