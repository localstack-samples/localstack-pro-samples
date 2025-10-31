import boto3
import json
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import uuid
import argparse

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / 'serverless-config.json'
with open(CONFIG_PATH, 'r') as f:
    cfg = json.load(f)

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=cfg.get('endpoint'),
    region_name=cfg.get('region'),
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

TABLE_NAME = f"ekart-products-{cfg.get('env', 'dev')}"
table = dynamodb.Table(TABLE_NAME)

def create_product(title, description, price, category, subcategory, brand, stock, rating, reviews, seller="seller-001", image_text=None):
    if image_text is None:
        image_text = title
    return {
        "product_id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "price": Decimal(str(price)),
        "currency": "USD",
        "category": category,
        "subcategory": subcategory,
        "brand": brand,
        "stock_quantity": stock,
        "rating": Decimal(str(rating)),
        "review_count": reviews,
        "seller_id": seller,
        "is_active": True,
        "variants": [],
        "tags": [],
        "images": [
            {
                "image_id": str(uuid.uuid4()),
                "url": f"https://via.placeholder.com/400x400/000000/FFFFFF/?text={image_text.replace(' ', '+')}",
                "alt_text": title,
                "is_primary": True
            }
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

DEFAULT_PRODUCTS = [
    create_product("MacBook Pro 16-inch M3 Pro", "Apple MacBook Pro with M3 Pro chip, 16-inch Liquid Retina XDR display, 18GB unified memory, 512GB SSD", 2499.99, "Electronics", "Laptops", "Apple", 15, 4.9, 342),
    create_product("Dell XPS 15 9530", "15.6-inch FHD+ InfinityEdge display, Intel Core i7-13700H, 16GB RAM, 512GB SSD, NVIDIA GeForce RTX 4050", 1799.99, "Electronics", "Laptops", "Dell", 22, 4.7, 189),
    create_product("Lenovo ThinkPad X1 Carbon Gen 11", "14-inch WUXGA IPS display, Intel Core i7-1355U, 16GB RAM, 512GB SSD, Windows 11 Pro", 1649.99, "Electronics", "Laptops", "Lenovo", 18, 4.6, 156, "seller-002"),
    create_product("iPhone 15 Pro Max", "6.7-inch Super Retina XDR display, A17 Pro chip, 256GB storage, Titanium design, USB-C", 1199.99, "Electronics", "Smartphones", "Apple", 45, 4.8, 892),
    create_product("Samsung Galaxy S24 Ultra", "6.8-inch Dynamic AMOLED 2X display, Snapdragon 8 Gen 3, 256GB storage, 200MP camera, S Pen included", 1299.99, "Electronics", "Smartphones", "Samsung", 38, 4.7, 654),
    create_product("Google Pixel 8 Pro", "6.7-inch LTPO OLED display, Google Tensor G3, 128GB storage, Best-in-class AI features", 999.99, "Electronics", "Smartphones", "Google", 29, 4.6, 423, "seller-002"),
    create_product("Sony WH-1000XM5 Wireless Headphones", "Industry-leading noise cancellation, 30-hour battery life, Hi-Res Audio, Multipoint connection", 399.99, "Electronics", "Audio", "Sony", 67, 4.8, 1234, "seller-003"),
    create_product("AirPods Pro (2nd generation)", "Active Noise Cancellation, Transparency mode, Personalized Spatial Audio, MagSafe charging", 249.99, "Electronics", "Audio", "Apple", 89, 4.7, 2156),
    create_product("Bose QuietComfort Ultra Headphones", "World-class noise cancellation, Spatial Audio, 24-hour battery, Premium comfort", 429.99, "Electronics", "Audio", "Bose", 43, 4.6, 567, "seller-003"),
    create_product("Apple Watch Series 9 GPS + Cellular 45mm", "Always-On Retina display, S9 chip, Advanced health features, 18-hour battery, Crash Detection", 499.99, "Electronics", "Wearables", "Apple", 56, 4.8, 987),
    create_product("Samsung Galaxy Watch 6 Classic 47mm", "Rotating bezel, Advanced sleep tracking, Body composition analysis, Sapphire crystal display", 429.99, "Electronics", "Wearables", "Samsung", 34, 4.6, 445),
    create_product("iPad Pro 12.9-inch M2", "12.9-inch Liquid Retina XDR display, M2 chip, 256GB storage, Apple Pencil support, 5G capable", 1099.99, "Electronics", "Tablets", "Apple", 28, 4.9, 678),
    create_product("Samsung Galaxy Tab S9 Ultra", "14.6-inch Dynamic AMOLED 2X display, Snapdragon 8 Gen 2, 256GB storage, S Pen included", 1199.99, "Electronics", "Tablets", "Samsung", 19, 4.7, 234),
    create_product("Breville Barista Express Espresso Machine", "Built-in conical burr grinder, Microfoam milk texturing, PID temperature control, Stainless steel", 699.99, "Home & Kitchen", "Coffee Makers", "Breville", 24, 4.7, 3421, "seller-004"),
    create_product("Keurig K-Elite Coffee Maker", "Strong brew setting, Iced coffee capability, 75oz reservoir, Programmable auto on/off", 169.99, "Home & Kitchen", "Coffee Makers", "Keurig", 78, 4.5, 5632, "seller-004"),
    create_product("Ninja Air Fryer Max XL", "5.5 quart capacity, Max Crisp Technology, 7 cooking functions, Dishwasher safe basket", 129.99, "Home & Kitchen", "Air Fryers", "Ninja", 92, 4.8, 8934, "seller-004"),
    create_product("Philips Premium Airfryer XXL", "7 quart capacity, Fat Removal technology, Smart sensing, Keep warm function, Digital touchscreen", 349.99, "Home & Kitchen", "Air Fryers", "Philips", 41, 4.6, 2341, "seller-004"),
    create_product("Dyson V15 Detect Cordless Vacuum", "Laser dust detection, LCD screen with real-time particle count, 60 minutes run time, HEPA filtration", 749.99, "Home & Kitchen", "Vacuum Cleaners", "Dyson", 33, 4.7, 1567, "seller-005"),
    create_product("iRobot Roomba j7+ Robot Vacuum", "Advanced AI obstacle avoidance, Self-emptying base, Smart mapping, Voice control compatible", 799.99, "Home & Kitchen", "Vacuum Cleaners", "iRobot", 47, 4.6, 2789, "seller-005"),
    create_product("Withings Body+ Smart Scale", "Full body composition analysis, WiFi & Bluetooth sync, Tracks 8 metrics, Multi-user recognition", 99.99, "Sports & Fitness", "Smart Scales", "Withings", 125, 4.5, 3456, "seller-006"),
    create_product("Fitbit Charge 6", "Built-in GPS, Heart rate monitoring, Sleep tracking, 7-day battery life, Water resistant 50m", 159.99, "Sports & Fitness", "Fitness Trackers", "Fitbit", 87, 4.4, 2134, "seller-006"),
    create_product("Garmin Forerunner 965", "AMOLED display, Training readiness, Race predictor, 23-day battery, Full-color maps", 599.99, "Sports & Fitness", "Fitness Trackers", "Garmin", 39, 4.8, 876, "seller-006"),
    create_product("Manduka PRO Yoga Mat", "6mm thick, Superior cushioning, Lifetime guarantee, Non-slip surface, Eco-friendly materials", 119.99, "Sports & Fitness", "Yoga Equipment", "Manduka", 156, 4.7, 4567, "seller-006"),
    create_product("Project Hail Mary by Andy Weir", "Hardcover - A lone astronaut must save the Earth from disaster in this propulsive new sci-fi thriller", 24.99, "Books", "Science Fiction", "Ballantine Books", 234, 4.9, 12456, "seller-007"),
    create_product("The Midnight Library by Matt Haig", "Between life and death, there's a library. A place where the books on the shelves represent possible lives.", 16.99, "Books", "Contemporary Fiction", "Viking", 189, 4.6, 8934, "seller-007"),
    create_product("PlayStation 5 Console", "Ultra-high speed SSD, Ray tracing, 4K gaming, Tempest 3D AudioTech, DualSense wireless controller", 499.99, "Gaming", "Consoles", "Sony", 12, 4.8, 5678, "seller-008"),
    create_product("Xbox Series X", "12 teraflops GPU power, 4K gaming at 120 FPS, 1TB SSD, Quick Resume, Game Pass compatible", 499.99, "Gaming", "Consoles", "Microsoft", 18, 4.7, 4321, "seller-008"),
    create_product("Nintendo Switch OLED Model", "7-inch OLED screen, Enhanced audio, 64GB storage, Adjustable stand, Handheld and docked modes", 349.99, "Gaming", "Consoles", "Nintendo", 67, 4.8, 7890, "seller-008"),
    create_product("Logitech G Pro X Superlight Gaming Mouse", "63g ultra-lightweight, HERO 25K sensor, 70-hour battery, LIGHTSPEED wireless, Ambidextrous design", 159.99, "Gaming", "Gaming Mice", "Logitech", 143, 4.8, 3421, "seller-009"),
    create_product("Razer BlackWidow V4 Pro Mechanical Keyboard", "Green mechanical switches, Programmable command dial, Underglow RGB, Magnetic wrist rest", 229.99, "Gaming", "Gaming Keyboards", "Razer", 78, 4.6, 1234, "seller-009"),
    create_product("Nike Air Max 270", "Men's Running Shoes, Max Air unit, Breathable mesh upper, Multiple colorways available", 150.00, "Fashion", "Sneakers", "Nike", 234, 4.5, 5678, "seller-010"),
    create_product("Adidas Ultraboost 22", "Women's Running Shoes, Boost cushioning, Primeknit+ upper, Continental rubber outsole", 190.00, "Fashion", "Sneakers", "Adidas", 167, 4.7, 4321, "seller-010"),
    create_product("Casio G-Shock GA-2100", "Men's Analog-Digital Watch, Shock resistant, 200m water resistance, Carbon Core Guard structure", 99.00, "Fashion", "Watches", "Casio", 345, 4.7, 8765, "seller-011"),
    create_product("Fossil Gen 6 Hybrid Smartwatch", "Analog watch face with smart features, Heart rate tracking, Notifications, 2-week battery life", 229.00, "Fashion", "Watches", "Fossil", 89, 4.4, 1234, "seller-011"),
    create_product("Herman Miller Aeron Office Chair", "Ergonomic mesh office chair, Adjustable lumbar support, PostureFit SL, 12-year warranty", 1395.00, "Office", "Furniture", "Herman Miller", 23, 4.8, 2345, "seller-012"),
    create_product("Autonomous SmartDesk Pro", "Electric standing desk, Dual motor, Memory presets, Anti-collision, 48x30 inch desktop", 599.00, "Office", "Furniture", "Autonomous", 45, 4.6, 3456, "seller-012"),
    create_product("Canon EOS R6 Mark II Mirrorless Camera", "24.2MP Full-Frame sensor, 40fps continuous shooting, 6K video, In-body image stabilization", 2499.00, "Electronics", "Cameras", "Canon", 14, 4.9, 234, "seller-013"),
    create_product("Sony Alpha a7 IV Mirrorless Camera", "33MP Full-Frame sensor, Real-time Eye AF, 4K 60fps video, 10fps continuous shooting", 2498.00, "Electronics", "Cameras", "Sony", 19, 4.8, 567, "seller-013"),
    create_product("DJI Mavic 3 Drone", "Hasselblad camera, 5.1K video, 46-minute flight time, Omnidirectional obstacle sensing", 2199.00, "Electronics", "Drones", "DJI", 31, 4.7, 892, "seller-013")
]

def load_products_from_file(path: Path):
    with open(path, 'r') as f:
        data = json.load(f)
    # Expect a list of product dicts already in the target schema
    return data

def seed_products(products):
    print(f"Seeding {len(products)} products to DynamoDB table {TABLE_NAME}...")
    for i, product in enumerate(products, 1):
        try:
            table.put_item(Item=product)
            print(f"✓ [{i}/{len(products)}] Added: {product.get('title', product.get('name', product['product_id']))}")
        except Exception as e:
            print(f"✗ [{i}/{len(products)}] Failed: {str(e)}")
    print("\n🎉 Seeding complete.")

def main():
    parser = argparse.ArgumentParser(description='Seed EKart data into DynamoDB')
    parser.add_argument('--file', '-f', type=str, help='Path to JSON file containing products array')
    args = parser.parse_args()

    if args.file:
        products = load_products_from_file(Path(args.file))
    else:
        products = DEFAULT_PRODUCTS
    seed_products(products)

if __name__ == '__main__':
    main()


