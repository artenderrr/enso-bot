from pathlib import Path

async def seed_db() -> None:
    from models import ClothingItem, ItemIdentifier
    
    item_image_path = Path("seed-images/tee.jpg")
    
    await ClothingItem.create(
        name="Tee",
        collection="Base",
        volume=100,
        image_bytes=item_image_path.read_bytes(),
        image_extension=item_image_path.suffix
    )
    
    for i in range(1, 21):
        await ItemIdentifier.create(
            id_=str(i).zfill(5),
            item_id=1,
            owner="@artenderr",
            purchase_date="29.05.2025",
            owner_note=None
        )
