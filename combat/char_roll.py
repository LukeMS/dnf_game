import os
import sys

import re
import random

if not os.path.isdir('combat'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rnd_utils import RangedDictionary
from combat.char_data import data


saving_throws = data["saving_throws"]
save_names = data["save_names"]
att_names = data["att_names"]
classes = data["classes"]
alignments = data["alignments"]
age_dict = data["age_dict"]
age_mod = data["age_mod"]
race_mod = data["race_mod"]
hw_dict = data["hw_dict"]
speed = data["speed"]
races = data["races"]
hit_dice = data["hit_dice"]
bab = data["bab"]
xp_award = data["xp_award"]
size_modifier = data["size_modifier"]
level_adv = data["level_adv"]
cr = data["cr"]


def starting_wealth(_class, verbose=False):
    if verbose:
        print("Class {}, var {}, fix {}".format(
            _class,
            data["starting_wealth"][_class][0],
            data["starting_wealth"][_class][1]
        ))
    var = roll(string=data["starting_wealth"][_class][0], verbose=verbose)
    fix = int(data["starting_wealth"][_class][1])
    if verbose:
        print("var {} * fix {}".format(var, fix))
    wealth = var * fix
    if verbose:
        print(wealth)
    return wealth


def aging_modifiers(age, race):
    test_list = [0] * 6
    final_list = []
    if race not in age_dict:
        return test_list

    mid = age_dict[race]['mid']
    old = age_dict[race]['old']
    ven = age_dict[race]['ven']
    for i, att in zip(range(len(test_list)), att_names):
        result = test_list[i]
        if age >= ven:
            result += age_mod['ven'][att[:3]]
        if age >= old:
            result += age_mod['old'][att[:3]]
        if age >= mid:
            result += age_mod['mid'][att[:3]]

        final_list.append(result)
    return(final_list)


def race_modifiers(race, mode=False):
    test_list = [0] * 6
    if race not in race_mod:
        return test_list
    final_list = []
    for i, att in zip(range(len(test_list)), att_names):
        if att[:3] in race_mod[race]:
            mod = race_mod[race][att[:3]]
        else:
            mod = 0
        final_list.append(test_list[i] + mod)
    # print([a[:3] + ": " + str(b) for a, b in zip(att_names, final_list)])
    return(final_list)


def get_age(race, class_=0):
    if race not in age_dict:
        # not applicable
        return 0, 0
    adulthood = age_dict[race]['ini']
    if class_:
        if class_ not in age_dict[race]['var']:
            class_ = random.choice(list(age_dict[race]['var'].keys()))
            dices, faces = age_dict[race]['var'][class_]
            # print(age_dict[race]['var'][class_])
    else:
        dices, faces = age_dict[race]['var']
    current = adulthood + roll(faces, dices, verbose=0)
    dices, faces = age_dict[race]['max']
    max_age = age_dict[race]['ven'] + roll(faces, dices, verbose=0)
    # print("current", "max_age", current, max_age)
    return current, max_age


def unit_conversion(value, from_unit, to_unit=False, round_=2):
    # lenght in meters
    lenght = {
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'km': 1000,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.34
    }
    if from_unit in lenght.keys():
        if to_unit is False:
            to_unit = 'm'
        if round_:
            return round(value * lenght[from_unit] / lenght[to_unit], 2)
        else:
            return (value * lenght[from_unit] / lenght[to_unit])

    # lenght in kilograms
    weight = {
        'g': 0.001,
        'kg': 1,
        'mg': 1e-6,
        'oz': 0.0283495,
        'lb': 0.453592
    }
    if from_unit in weight.keys():
        if to_unit is False:
            to_unit = 'kg'
        if round_:
            return round(value * weight[from_unit] / weight[to_unit], 2)
        else:
            return value * weight[from_unit] / weight[to_unit]


def height_weight(race, gender, modifiers=[0] * 6, debug=False):

    if debug:
        for race in hw_dict.keys():
            print(race)
            for gender in hw_dict[race].keys():
                print(gender, ', ', sep='', end="")
                h_feets, h_inches = hw_dict[race][gender][0].split("'")
                min_h = unit_conversion(((
                    float(h_feets) * 12 +
                    float(h_inches) +
                    hw_dict[race][gender][2][0]) / 12), 'ft')
                max_h = unit_conversion(((
                    float(h_feets) * 12 +
                    float(h_inches) +
                    (hw_dict[race][gender][2][0] *
                        hw_dict[race][gender][2][1])) / 12), 'ft')
                min_w = unit_conversion(
                    hw_dict[race][gender][1] +
                    hw_dict[race][gender][2][0] * hw_dict[race][gender][3],
                    'lb')
                max_w = unit_conversion(
                    hw_dict[race][gender][1] +
                    hw_dict[race][gender][2][0] * hw_dict[race][gender][2][1] *
                    hw_dict[race][gender][3],
                    'lb')
                print("Height: {}-{}m., Weight: {}-{}kg.".format(
                    round(min_h, 2), round(max_h, 2),
                    round(min_w, 2), round(max_w, 2), end=""))
            print("")
        exit()
    if race is None or race not in hw_dict:
        return 0, 0
    h_feets, h_inches = hw_dict[race][gender][0].split("'")
    roll_result = (roll(
        hw_dict[race][gender][2][0],
        hw_dict[race][gender][2][1], verbose=0) +
        (modifiers[0] + modifiers[2]) / 2)
    height_inches = float(h_feets) * 12 + float(h_inches) + roll_result
    weight = hw_dict[race][gender][1] + \
        (roll_result * hw_dict[race][gender][3])
    height_feet = round(height_inches / 12, 2)
    return height_feet, weight
# height_weight(0, 0, debug=True)


def roll_attributes(verbose=False):
    '''
    If the  scores are too low they are rerolled.
    They are considered too low if the sum of their modifiers (before
    racial adjustments) is 1 or lower, or if the highest score is 14 or
    lower.
    '''
    valid_attributes = 0
    rolls = 0
    while not valid_attributes:
        if verbose:
            print("=======================")
            print("# Roll number", rolls)

        '''
        Each of the character's six ability scores is determined by rolling
        four six-sided dice, ignoring the lowest die roll, and totaling the
        other three.
        '''
        attribute_creation_list = [
            roll(rolls=4, faces=6, mode='discard_lowest', verbose=verbose)
            for x in range(6)]

        attribute_modifiers = list(
            AttributeModifers.get(x) for x in attribute_creation_list)

        total_modifiers = sum(attribute_modifiers)

        if verbose:
            print("New attributes:", attribute_creation_list)
            print("Modifiers:", attribute_modifiers)
            print("Sum:", total_modifiers)

        if total_modifiers > 0 and max(attribute_creation_list) > 13:
            if verbose:
                print('Valid attributes')
            return attribute_creation_list

        rolls += 1

        print('Invalid attributes...')

    @property
    def att_mod(self):
        return [self.attribute_modifiers[x]
                for x in self.attribute_creation_list]


class AttributeModifers:
    dic = RangedDictionary()
    mod = -5
    for i in range(0, 50, 2):
        dic[range(i, i + 1 + 1)] = mod
        mod += 1

    @classmethod
    def get(cls, value):
        return cls.dic[value]


def roll(
        faces=20, rolls=1, modifier=0,
        mode='std', string=None, verbose=False):
    def parse_string(string, verbose=False):
        pattern = (
            '(?P<rolls>\d+)'
            'd'
            '(?P<faces>\d+)'
            '(?P<modifier>(\+|-)\d+)?'
        )
        searchobj = re.match(pattern, string, re.I)
        if searchobj:
            rolls = int(searchobj.group("rolls"))
            faces = int(searchobj.group("faces"))
            if searchobj.group("modifier"):
                modifier = int(searchobj.group("modifier"))
            else:
                modifier = 0
        else:
            print('"{}"not found'.format(string))
            raise ValueError
        if verbose:
            print("{} = {} rolls of {} faces with modifier {}".format(
                string, rolls, faces, modifier))
        return rolls, faces, modifier

    if string or isinstance(faces, str):
        string = string or faces
        rolls, faces, modifier = parse_string(string=string, verbose=verbose)

    roll_list = []
    for i in range(rolls):
        roll = random.randint(1, faces) + modifier

        roll_list.append(roll)
        if verbose:
            print('Rolling D', faces, sep='', end='')
            if modifier:
                print('+', modifier, sep='', end='')
            print(': ', sep='', end='')
            print(roll)
    if verbose:
        print(rolls, sep='', end='')
        print('D', faces, sep='', end='')
        if modifier:
            print('+', modifier, sep='', end='')
        print(' = ', sep='', end='')
    if mode == 'std':
        result = sum(roll_list)
        if verbose:
            print(result)
    elif mode == 'discard_lowest':
        min_roll = min(roll_list)
        result = sum(roll_list) - min_roll
        if verbose:
            print(result, '(discarding %i)' % min_roll)
    return result


def pretty_stats():
    att = roll_attributes()
    att_mod = [AttributeModifers.get(x) for x in att]

    [print("{}: {}({})".format(a, b, c))
        for a, b, c in zip(
            att_names,
            att,
            att_mod)]

if __name__ == '__main__':
    pretty_stats()
    exit()
    from mylib.data_tree import tk_tree_view
    tk_tree_view(AttributeModifers.dic)
    exit()

    c = Character()
    print(c.att_mod)
    exit()
    tk_tree_view(c.__dict__)
