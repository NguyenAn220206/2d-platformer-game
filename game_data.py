# game_data.py

# Danh sách 5 map
MAPS = [
    {
        "id": 1,
        "file": "maps/map_1.py",
        "unlocked": True,   # map đầu tiên luôn mở
        "completed": False
    },
    {
        "id": 2,
        "file": "maps/map_2.py",
        "unlocked": False,
        "completed": False
    },
    {
        "id": 3,
        "file": "maps/map_3.py",
        "unlocked": False,
        "completed": False
    },
    {
        "id": 4,
        "file": "maps/map_4.py",
        "unlocked": False,
        "completed": False
    },
    {
        "id": 5,
        "file": "maps/map_5.py",
        "unlocked": False,
        "completed": False
    }
]

# Hàm đánh dấu map đã hoàn thành và mở map tiếp theo
def complete_map(map_id):
    for map_data in MAPS:
        if map_data["id"] == map_id:
            map_data["completed"] = True
            break
    # Mở map tiếp theo
    for map_data in MAPS:
        if map_data["id"] == map_id + 1:
            map_data["unlocked"] = True
            break
