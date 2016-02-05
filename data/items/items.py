import effects
from constants import GAME_COLORS


items_db = {
    'healing potion': {
        'use_function': effects.cast_heal,
        'id': ord('!'),
        'color': GAME_COLORS["blood_red"]
    },

    'scroll of lightning bolt': {
        'use_function': effects.cast_lightning,
        'id': ord('?'),
        'color': GAME_COLORS["papyrus"]
    },

    'scroll of confusion': {
        'use_function': effects.cast_confuse,
        'id': ord('?'),
        'color': GAME_COLORS["papyrus"]
    },

    'scroll of fireball': {
        'use_function': effects.cast_fireball,
        'id': ord('?'),
        'color': GAME_COLORS["papyrus"]
    },
    'remains': {
        'use_function': effects.cast_heal,
        'id': ord('?'),
        'color': GAME_COLORS["corpse"]
    }
}
