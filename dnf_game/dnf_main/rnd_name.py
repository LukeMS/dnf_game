"""..."""

import random

from dnf_game.util import RangedDictionary, SingletonMeta
from dnf_game.dnf_main import data_handler


class NameGen(dict, metaclass=SingletonMeta):
    """..."""

    def __init__(self):
        """..."""
        self.names_db = data_handler.get_names()

        self.name_dict = {
            'human': {
                'names': RangedDictionary({
                    range(0, 75): 'human',
                    range(75, 100): 'generic'
                }),
                'surnames': RangedDictionary({
                    range(0, 75): 'human',
                    range(75, 100): 'generic'
                })
            },
            'dwarf': {
                'names': RangedDictionary({
                    range(0, 100): 'dwarf'
                }),
                'surnames': RangedDictionary({
                    range(0, 100): 'dwarf'
                })
            },
            'elf': {
                'names': RangedDictionary({
                    range(0, 100): 'elf'
                }),
                'surnames': RangedDictionary({
                    range(0, 70): None,
                    range(70, 85): 'generic',
                    range(85, 90): 'human',
                    range(90, 95): 'gnome',
                    range(95, 100): 'halfling'
                })
            },
            'gnome': {
                'names': RangedDictionary({
                    range(0, 100): 'gnome'
                }),
                'surnames': RangedDictionary({
                    range(0, 100): 'gnome'
                })
            },
            'halfling': {
                'names': RangedDictionary({
                    range(0, 100): 'halfling'
                }),
                'surnames': RangedDictionary({
                    range(0, 100): 'halfling'
                })
            },
            'half-elf': {
                'names': RangedDictionary({
                    range(0, 25): 'human',
                    range(25, 50): 'generic',
                    range(50, 100): 'elf'
                }),
                'surnames': RangedDictionary({
                    range(0, 30): None,
                    range(30, 60): 'generic',
                    range(60, 90): 'human',
                    range(90, 95): 'gnome',
                    range(95, 100): 'halfling'
                })
            },
            'half-orc': {
                'names': RangedDictionary({
                    range(0, 25): 'human',
                    range(25, 50): 'generic',
                    range(50, 100): 'orc'
                }),
                'surnames': RangedDictionary({
                    range(0, 25): 'human',
                    range(25, 50): 'generic',
                    range(50, 100): 'orc'
                })
            }
        }


def get_name(race=None, gender=None, number=1):
    """..."""
    name_gen = NameGen()
    race = race or random.choice(list(name_gen.name_dict.keys()))
    gender = gender or random.choice(['male', 'female'])

    name_list = []
    surname_list = []

    surnames = name_gen.name_dict[race]['surnames']
    names = name_gen.name_dict[race]['names']

    for x in range(number):
        try:
            name_key = names[random.randint(0, 99)]
            surname_key = surnames[random.randint(0, 99)]
        except KeyError:
            print("Race %s, Gender %s, Key %s" % (race, gender, x))
            raise

        if name_key == 'generic':
            name_list.append(
                random.choice(name_gen.names_db[name_key]['names']))
        else:
            name_list.append(
                random.choice(name_gen.names_db[name_key]['names'][gender]))
        if surname_key is None:
            surname_list.append("")
        else:
            surname_list.append(
                random.choice(name_gen.names_db[surname_key]['surnames']))

    return name_list, surname_list


if __name__ == '__main__':
    name_list, surname_list = get_name(race='human', number=1)
    [print(name, surname) for name, surname in zip(name_list, surname_list)]
    name_list, surname_list = get_name(race='human', number=1)
    [print(name, surname) for name, surname in zip(name_list, surname_list)]
