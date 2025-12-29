# 2d-platformer-game
2D platformer game built with Python and Pygame, using character-based maps.
# Platformer Game (Pygame)

## Gioi thieu

Day la mot game platformer 2D viet bang **Python + Pygame**. Game ho tro nhieu man choi (map), co menu chon man, gameplay co ke dich (enemy), vat can, va man hinh thong bao **thang / thua**. Du lieu map duoc luu rieng bang file JSON de de mo rong va chinh sua.

Du an phu hop cho muc dich hoc tap: to chuc code game, xu ly map, va quan ly asset trong Pygame.

---

## Tinh nang chinh

* Menu chinh va man hinh chon map
* Nhieu map (level) doc tu file JSON
* He thong player: di chuyen, nhay, va va cham
* Enemy va vat can co ban
* Hien thong bao **Win / Lose** o giua man hinh choi
* Cau truc thu muc ro rang, de mo rong

---

## Cau truc thu muc

```
New Game/
│
├── main.py              # File chay game
├── settings.py          # Cau hinh chung (WIDTH, HEIGHT, FPS,...)
├── menu.py              # Menu chinh
├── map.py               # Man hinh chon map
├── play.py              # Xu ly choi game
├── level.py             # Logic level (map, player, enemy)
├── game_data.py         # Danh sach map va thong tin lien quan
│
├── assets/              # Chua toan bo hinh anh game
│   ├── player/
│   ├── enemy/
│   ├── background/
│   └── ui/
│
├── maps/                # Chua cac file map (JSON)
│   ├── map_1.json
│   ├── map_2.json
│   └── ...
│
└── README.md
```

---

## Cau truc file map (vi du)

File map duoc viet duoi dang **Python (.py)**, mo ta map bang ky tu.

```python
MAP_ID = 1
TILE_SIZE = 50

world_map = [
    '                                                                                ',
    '                                                                                ',
    '                X           X           X                X           X          ',
    '                                                                                ',
    '                           E                T                    E              ',
    '      P       X                 X                 X                              ',
    'XXXXXXXXXX         XXXXXXXX         XXXXXXXX         XXXXXXXX            XXXXXG ',
    '                                                                                ',
    '           T                    E                    T                           ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]
```

### Y nghia ky tu trong map

* `X` : Nen / vat can (ground, wall)

* `P` : Vi tri bat dau cua player

* `E` : Enemy

* `T` : Bay / trap

* `G` : Dich (goal / cong ve dich)

* Khoang trang: khong gian trong

* `TILE_SIZE`: kich thuoc moi o (pixel)

* `MAP_ID`: dinh danh map

---

## Cach chay game

### 1. Cai dat thu vien

Dam bao da cai Python (>= 3.9), sau do cai Pygame:

```bash
pip install pygame
```

### 2. Chay game

```bash
python main.py
```

---

## Dieu khien (co the thay doi theo code)

* Mui ten trai / A: Di sang trai
* Mui ten phai / D: Di sang phai
* Space / W: Nhay

---

## Dinh huong phat trien

* Them am thanh va nhac nen
* Them nhieu loai enemy
* Them vat pham (item)
* Luu tien trinh choi (save/load)
* Cai thien AI enemy

---

## Muc dich hoc tap

Du an nay tap trung vao:

* To chuc code game Pygame
* Quan ly asset va map bang JSON
* Tu duy tach module (menu, play, level)
* Nen tang de phat trien game 2D hoan chinh

---

## Tac gia

Nguyen An

---

## Ghi chu

Day la du an hoc tap, chua toi uu hoa hoan toan. Ban co the tu do chinh sua va mo rong theo nhu cau.
