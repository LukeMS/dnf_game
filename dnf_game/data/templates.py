"""..."""
from dnf_game.data.constants import COLORS
from dnf_game.dnf_main import effects
from dnf_game.dnf_main.data_handler.data_handler import (
    get_all_weapons, get_all_armors)


def get_templates():
    """..."""
    templates = {
        "TileEntity": {
            "_default": {
                "block_mov": False,
                "block_sight": False,
                "color": None
            },
            "floor": {
                "id": ord("."),
                "color": (129, 106, 86),
                "_rnd_gen_cost": 64
            },
            "hall": {
                "id": ord("/"),
                "color": (129, 106, 86),
                "_rnd_gen_cost": 1
            },
            "wall": {
                "id": ord("#"),
                "color": (161, 161, 161),
                "_rnd_gen_cost": 8,
                "block_mov": True,
                "block_sight": True,
            },
            "water": {
                "id": ord("="),
                "color": COLORS["blue"]
            },
            "mountain": {
                "id": ord("M"),
                "color": COLORS["light_chartreuse"]
            },
            "hill": {
                "id": ord("h"),
                "color": COLORS["dark_chartreuse"]
            },
            "land": {
                "id": ord("."),
                "color": COLORS["darker_green"]
            },
            "coast": {
                "id": ord("c"),
                "color": COLORS["darker_amber"]
            },
            "shallow_water": {
                "id": ord("~"),
                "color": COLORS["dark_blue"]
            },
            "deep_water": {
                "id": ord("¬"),
                "color": COLORS["darkest_blue"]
            },

            "arctic_shallow_water": {
                "id": ord("~"),
                "color": COLORS["sky"]
            },
            "arctic_deep_water": {
                "id": ord("¬"),
                "color": COLORS["dark_sky"]
            },
            "arctic coast": {
                "id": ord("c"),
                "color": (248, 243, 223)
                # COLORS["lightest_amber"]  # (255, 255, 255)
            },
            "arctic land": {
                "id": ord("."),
                "color": (248, 248, 255)  # (255, 255, 255)
            },
            "arctic hill": {
                "id": ord("h"),
                "color": (245, 245, 245)  # (255, 255, 255)
            },
            "arctic mountain": {
                "id": ord("M"),
                "color": (245, 245, 245)  # (255, 255, 255)
            },

            "temperate desert": {
                "id": ord("d"),
                "color": (240, 220, 7)
            },
            "subtropical desert": {
                "id": ord("d"),
                "color": (250, 150, 24)
            },
            "tropical desert": {
                "id": ord("d"),
                "color": (255, 65, 12)
            },

            "boreal grassland": {
                "id": ord("."),
                "color": COLORS["dark_sea"]
            },
            "grassland": {
                "id": ord("."),
                "color": COLORS["darker_green"]
            },
            "savana": {
                "id": ord("."),
                "color": COLORS["darker_yellow"]  # (153, 219, 33)
            },

            "woodland": {
                "id": ord("w"),
                "color": COLORS["dark_turquoise"]  # (0, 255, 255)
            },
            "boreal forest": {
                "id": ord("B"),
                "color": COLORS["dark_sea"]  # (5, 100, 33)
            },
            "temperate deciduous forest": {
                "id": ord("D"),
                "color": COLORS["dark_chartreuse"]  # (47, 186, 74)
            },
            "temperate rain forest": {
                "id": ord("T"),
                "color": COLORS["dark_green"]  # (7, 250, 160)
            },
            "tropical rain forest": {
                "id": ord("R"),
                "color": COLORS["darker_green"]  # (8, 250, 50)
            },

            # removed
            "tundra": {
                "id": ord(","),
                "color": (87, 235, 249)
            },
            "tropical seasonal forest": {
                "id": ord("S"),
                "color": (153, 219, 33)
            }
        },
        "FeatureEntity": {
            '_default': {
                'color': COLORS["gray"],
                "block_mov": False,
                "block_sight": False
            },
            'stair_up': {
                'id': ord("<")
            },
            'stair_down': {
                'id': ord(">")
            },
            "door_closed": {
                "id": ord("="),
                "color": (161, 161, 161),
                "block_mov": True,
                "block_sight": True
            },
            "door_locked": {
                "id": ord("¬"),
                "color": (161, 161, 161),
                "block_mov": True,
                "block_sight": True
            },
            "door_open": {
                "id": ord("\\"),  # 92
                "color": (161, 161, 161)
            }
        },
        "ItemEntity": {
        },

        "FeatureComponent": {
            "_default": {
                'use_function': None,
            },
            'stair_up': {
                'use_function': effects.change_dng_level,
                'direction': "up"
            },
            'stair_down': {
                'use_function': effects.change_dng_level,
                'direction': "down"
            }
        },
        "ItemComponent": {
            "_default": {
                'use_function': None,
                'color': COLORS["papyrus"]
            },
            'healing potion': {
                'use_function': effects.cast_heal,
                'id': ord('!'),
                'color': COLORS["blood_red"]
            },
            'scroll of lightning bolt': {
                'use_function': effects.cast_lightning,
                'id': ord('?')
            },
            'scroll of confusion': {
                'use_function': effects.cast_confuse,
                'id': ord('?')
            },
            'scroll of fireball': {
                'use_function': effects.cast_fireball,
                'id': ord('?')
            },
            'remains': {
                'use_function': effects.cast_heal,
                'id': ord('?'),
                'color': COLORS["corpse"]
            }
        },
        "WeaponComponent": {
            "_default": {
                "id": ord("|"),
                "color": COLORS["grey"]
            },
            **get_all_weapons()
        },
        "ArmorComponent": {
            "_default": {
                "id": ord("["),
                "color": COLORS["grey"],
                "on_equip": [],
                "on_unequip": []
            },
            **get_all_armors()
        }
    }
    return templates

if __name__ == '__main__':
    from pprint import pprint
    pprint(get_templates(), indent=4)
