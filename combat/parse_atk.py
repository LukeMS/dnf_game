import re
from collections import OrderedDict
from pprint import pprint

strings = {
    'n_attacks': (
        ' *(?P<attacks>\d)+ (?P<melee_desc>\D[a-z]*(( |-)[a-z]*)*) '
        '(?P<melee>(\+|-)\d+(/(\+|-)\d+)*)? *'
        '( ?bite | ?touch | ?melee touch | ?melee )?;'
        '(?P<melee_dmg>\d*d\d*((\+|-)\d*)?)? ?'
        '(/( ?(?P<melee_crit1>\d*)-\d*))? ?'
        '(/( ?x(?P<melee_crit_dmg>\d)))? ?'
        '(( ?plus )'
        '(?P<melee_esp>((\d*(d\d*((\+|-)\d*)?)? )?'
        '[a-z]*( [a-z]*)*)*))*'
        '(/((?P<melee_crit2>\d*)-\d*))?'
    ),
    'attacks/': (
        ' *(?P<melee_desc>((([a-z]* )?(\+|-)\d))? ?'
        '\D[a-z]*( [a-z]*)*) ?(?P<melee>(\+|-)\d+(/(\+|-)\d+)+)+ *;'
        '(?P<melee_dmg>\d*d\d*(\+|-)\d*)? ?'
        '(/( ?(?P<melee_crit1>\d*)-\d*))? ?'
        '(/( ?x(?P<melee_crit_dmg>\d)))? ?'
        '(( ?plus )'
        '(?P<melee_esp>((\d*(d\d*((\+|-)\d*)?)? )?'
        '[a-z]*( [a-z]*)*)*))*'
        '(/( ?(?P<melee_crit2>\d*)-\d*))?'
    ),
    'single': (
        ' *(?P<melee_desc>((\+|-)\d*)? ?\D[a-z]*( [a-z]*)*) '
        '(?P<melee>(\+|-)\d+)? *'
        '( ?bite | ?touch | ?melee touch | ?melee )?;'
        '(?P<melee_dmg>\d*d\d*((\+|-)\d*)?)? ?'
        '(/( ?(?P<melee_crit1>\d*)-\d*))?'
        '(/( ?x(?P<melee_crit_dmg>\d)))? ?'
        '(( ?plus )'
        '(?P<melee_esp>((\d*(d\d*((\+|-)\d*)?)? )?'  # more then one plus
        '[a-z]*( [a-z]*)*)*))*'  # 2d8+5 plus 1d8 acid plus grab
        '(/( ?(?P<melee_crit2>\d*)-\d*))?'
    ),
    'esp_no_dmg': (
        ' *(?P<melee_desc>\D[a-z]*( [a-z]*)*) (?P<melee>(\+|-)\d+)? *;'
        '(?P<melee_esp>\D[a-z]*( [a-z]*)*)'),
    'save_reduction1': (
        ' *DC (?P<dc>\d*) (?P<save>Fort)\.* (?P<effect>half) *'),
    'save_reduction2': (
        ' *(?P<save>Fort)\.* *DC (?P<dc>\d*) (?P<effect>half) *')
}


def clear_outter_space(string):
    # print('clear_outter_space -> string "{}"'.format(string))
    if string not in ['', None]:
        if string[0] == ' ':
            string = string[1:]
        if string[-1:] in [' ', ',']:
            string = string[:-1]
    return string


def parse_plus(melee_esp, dict_, verbose=True):
    if verbose:
        print('======== running ### parse_plus ###')
        print('string before split: "{}"'.format(melee_esp))
    if melee_esp is None:
        dict_.append(None)
        return
    else:
        melee_esp = melee_esp.split(' and ')
    if len(melee_esp) == 1:
        if verbose:
            print("splitted string has lenght 1")
        melee_esp_match = re.match(
            '(?P<esp_dice>\d*(d\d*((\+|-)\d*)?)?)? ?(?P<esp_desc>\D[a-z]*)',
            melee_esp[0], re.I)
        if melee_esp_match:
            if verbose:
                print('esp_dice: "{}"'.format(
                    melee_esp_match.group('esp_dice')))
                print('esp_desc: "{}"'.format(
                    melee_esp_match.group('esp_desc')))
        else:
            melee_esp_match = re.match(
                '(?P<esp_dice>\d*)? ?(?P<esp_desc>\D[a-z]*)',
                melee_esp[0], re.I)
            print('no match')
            exit()
        if melee_esp_match.group('esp_dice'):
            dict_.append(tuple(
                (melee_esp_match.group('esp_desc'),
                    str(melee_esp_match.group('esp_dice'))))
            )
        else:
            dict_.append(melee_esp_match.group('esp_desc'))
    else:
        for each in melee_esp:
            melee_esp_match = re.match((
                '(?P<esp_dice>\d*(d\d*((\+|-)\d*)?)? )? ?'
                '(?P<esp_desc>\D[a-z]*( [a-z]*)*)'),
                each, re.I)
            if melee_esp_match:
                if verbose:
                    print('esp_dice', melee_esp_match.group('esp_dice'))
                    print('esp_desc', melee_esp_match.group('esp_desc'))
                # print(melee_esp_match.groups())
                if melee_esp_match.group('esp_dice'):
                    dict_.append(
                        tuple((
                            melee_esp_match.group('esp_desc'),
                            melee_esp_match.group('esp_dice')
                        )))
                else:
                    dict_.append(melee_esp_match.group('esp_desc'))
            else:
                print('bogus')
                exit()
    if verbose:
        pprint(dict_)
        print('======== ending ### parse_plus ###')


def parse_melee(line, verbose=True):
    adjustments = OrderedDict()
    [adjustments.update(x) for x in [
        {", or ": " or "},
        {"touch +4 melee touch (steal voice)":
            "touch +4 (1d0 plus steal voice)"},
        {"(rage)": ""},
        {"(": ";"},
        {")": ""},
        {"vs.": ";"}
    ]]
    for replace_from, replace_to in adjustments.items():
        line = line.replace(replace_from, replace_to)

    new = {
        'main': {
            "melee": [],
            "melee_desc": [],
            "melee_dmg": [],
            "melee_crit": [],
            "melee_esp": [],
            'melee_crit_dmg': []
        }
    }

    if line in [None, [None], 'none']:
        if verbose:
            print(line)
        new = {
            'main': {
                "melee": [None],
                "melee_desc": [None],
                "melee_dmg": [None],
                "melee_crit": [None],
                "melee_esp": [None],
                'melee_crit_dmg': [None]
            }
        }
        return new

    splitted = line.split(",")
    if verbose:
        print("____________")
        print("New line", splitted)

    for split in splitted:
        """ beginning of specific parsing for alternative attacks """
        # 2 slams +12 ;2d6+3 or masterwork falchion +13/+8 ;2d6+3/18-20
        split = clear_outter_space(split)
        searchobj = re.search(' or ', split, re.I)
        if searchobj:
            if verbose:
                print('or: "{}"'.format(split))
            new['alt'] = {
                "melee": [],
                "melee_desc": [],
                "melee_dmg": [],
                "melee_crit": [],
                "melee_esp": [],
                'melee_crit_dmg': []
            }
            splitted_line = split.split(' or ')
            for each, i in zip(splitted_line, range(len(splitted_line))):
                if verbose:
                    print('each: "{}"'.format(each))
                if i == 0:
                    atk = 'main'
                elif i == 1:
                    atk = 'alt'

                searcheach = re.match(strings['n_attacks'], each, re.I)
                if searcheach:
                    if verbose:
                        print("split:", each)

                    if searcheach.group("melee") is None:
                        splitted_attacks = searcheach.group("melee")
                    else:
                        splitted_attacks = searcheach.group("melee").split('/')

                    splitted_attacks = searcheach.group("melee").split('/')
                    for i in range(int(searcheach.group("attacks"))):

                        if verbose:
                            print(searcheach.group('melee'))
                        melee = searcheach.group('melee')
                        if melee:
                            if len(splitted_attacks) == 1:
                                new[atk]['melee'].append(
                                    int(splitted_attacks[0]))
                            else:
                                new[atk]['melee'].append(
                                    int(splitted_attacks[i]))
                        else:
                            new[atk]['melee'].append(0)

                        new[atk]['melee_desc'].append(
                            str(searcheach.group("melee_desc")))
                        new[atk]['melee_dmg'].append(
                            str(searcheach.group("melee_dmg")))

                        if searcheach.group("melee_crit1"):
                            melee_crit = searcheach.group("melee_crit1")
                        else:
                            melee_crit = searcheach.group("melee_crit2")
                        new[atk]['melee_crit'].append(melee_crit)

                        parse_plus(
                            searcheach.group("melee_esp"),
                            new[atk]['melee_esp'],
                            verbose=verbose)

                        melee_crit_dmg = searcheach.group("melee_crit_dmg")
                        if melee_crit_dmg:
                            new[atk]['melee_crit_dmg'].append(
                                int(melee_crit_dmg))
                        else:
                            new[atk]['melee_crit_dmg'].append(2)

                    if verbose:
                        pprint(new)
                        print("____________")
                    continue

                # Huge greatclub +12/+7 ;4d6+9
                searcheach = re.match(strings['attacks/'], each, re.I)
                if searcheach:
                    if verbose:
                        print("split:", each)
                    splitted_attacks = searcheach.group("melee").split('/')
                    attacks = len(splitted_attacks)
                    if verbose:
                        print(attacks)
                        print(splitted_attacks)
                        print(searcheach.group('melee'))
                    for i in range(attacks):
                        new[atk]['melee'].append(int(splitted_attacks[i]))
                        new[atk]['melee_desc'].append(
                            str(searcheach.group("melee_desc")))
                        new[atk]['melee_dmg'].append(
                            str(searcheach.group("melee_dmg")))

                        if searcheach.group("melee_crit1"):
                            melee_crit = searcheach.group("melee_crit1")
                        else:
                            melee_crit = searcheach.group("melee_crit2")
                        new[atk]['melee_crit'].append(melee_crit)

                        parse_plus(
                            searcheach.group("melee_esp"),
                            new[atk]['melee_esp'],
                            verbose=verbose)

                        melee_crit_dmg = searcheach.group("melee_crit_dmg")
                        if melee_crit_dmg:
                            new[atk]['melee_crit_dmg'].append(
                                int(melee_crit_dmg))
                        else:
                            new[atk]['melee_crit_dmg'].append(2)

                    if verbose:
                        pprint(new)
                        print("____________")
                    continue

                # bite +21 ;3d6+8/19-20 plus grab
                #  tail slap +21 ;2d8+6
                searchobj = re.match(strings['single'], each, re.I)
                if searchobj:
                    if verbose:
                        print("each:", each)
                        print(searchobj.group('melee'))
                    melee = searchobj.group('melee')
                    if melee:
                        new[atk]['melee'].append(int(melee))
                    else:
                        new[atk]['melee'].append(0)

                    new[atk]['melee_desc'].append(
                        str(searchobj.group("melee_desc")))
                    new[atk]['melee_dmg'].append(
                        str(searchobj.group("melee_dmg")))

                    if searchobj.group("melee_crit1"):
                        melee_crit = searchobj.group("melee_crit1")
                    else:
                        melee_crit = searchobj.group("melee_crit2")
                    new[atk]['melee_crit'].append(melee_crit)

                    if searchobj.group("melee_dmg"):
                        if verbose:
                            print("melee_dmg {}".format(
                                searchobj.group("melee_dmg")))
                        melee_esp = searchobj.group('melee_esp')
                        parse_plus(
                            melee_esp, new['main']['melee_esp'], verbose=verbose)
                    else:
                        if verbose:
                            print("no melee_dmg")
                        melee_esp_match = re.match(
                            strings['esp_no_dmg'], each, re.I)
                        if melee_esp_match:
                            melee_esp = melee_esp_match.group('melee_esp')
                            if verbose:
                                print('found esp_no_dmg "{}"'.format(melee_esp))
                            parse_plus(
                                melee_esp, new['main']['melee_esp'],
                                verbose=verbose)
                            # print(new['main'])
                        else:
                            if verbose:
                                print('found no esp_no_dmg: "{}"'.format(each))
                            parse_plus(
                                each, new[atk]['melee_esp'],
                                verbose=verbose)
                            # print(new['main'])

                    melee_crit_dmg = searchobj.group("melee_crit_dmg")
                    if melee_crit_dmg:
                        new[atk]['melee_crit_dmg'].append(
                            int(melee_crit_dmg))
                    else:
                        new[atk]['melee_crit_dmg'].append(2)

                    if verbose:
                        pprint(new)
                        print("____________")
                    if each == "slam +5 ;1d6+6":
                        pass
                    continue


############





            if verbose:
                print('WITH "OR"')
                # print("***{}***".format(line))
                print('error: "{}" remains'.format(each))
                print('currently parsed:')
                pprint(new)
                exit()
            """ end of specific parsing for alternative attacks """

        else:

            # 2 claws +15 ;1d8+4/19-20 plus grab
            # 2 heavy ballistae +14 (4d8/17-20/x3)
            searchobj = re.match(strings['n_attacks'], split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                if searchobj.group("melee") is None:
                    splitted_attacks = searchobj.group("melee")
                else:
                    splitted_attacks = searchobj.group("melee").split('/')
                for i in range(int(searchobj.group("attacks"))):

                    if verbose:
                        print(searchobj.group('melee'))
                    melee = searchobj.group('melee')
                    if melee:
                        if len(splitted_attacks) == 1:
                            new['main']['melee'].append(
                                int(splitted_attacks[0]))
                        else:
                            new['main']['melee'].append(
                                int(splitted_attacks[i]))
                    else:
                        new['main']['melee'].append(0)

                    new['main']['melee_desc'].append(
                        str(searchobj.group("melee_desc")))
                    new['main']['melee_dmg'].append(
                        str(searchobj.group("melee_dmg")))

                    if searchobj.group("melee_crit1"):
                        melee_crit = searchobj.group("melee_crit1")
                    else:
                        melee_crit = searchobj.group("melee_crit2")
                    new['main']['melee_crit'].append(melee_crit)

                    parse_plus(
                        searchobj.group("melee_esp"), new['main']['melee_esp'],
                        verbose=verbose)

                    melee_crit_dmg = searchobj.group("melee_crit_dmg")
                    if melee_crit_dmg:
                        new['main']['melee_crit_dmg'].append(
                            int(melee_crit_dmg))
                    else:
                        new['main']['melee_crit_dmg'].append(2)

                if verbose:
                    pprint(new)
                    print("____________")
                if split == " 2 claws ;1d3+1":
                    pass
                continue

            # Huge greatclub +12/+7 ;4d6+9
            searchobj = re.match(strings['attacks/'], split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                splitted_attacks = searchobj.group("melee").split('/')
                attacks = len(splitted_attacks)
                if verbose:
                    print(attacks)
                    print(splitted_attacks)
                    print(searchobj.group('melee'))
                for i in range(attacks):
                    new['main']['melee'].append(int(splitted_attacks[i]))
                    new['main']['melee_desc'].append(
                        str(searchobj.group("melee_desc")))
                    new['main']['melee_dmg'].append(
                        str(searchobj.group("melee_dmg")))

                    if searchobj.group("melee_crit1"):
                        melee_crit = searchobj.group("melee_crit1")
                    else:
                        melee_crit = searchobj.group("melee_crit2")
                    new['main']['melee_crit'].append(melee_crit)

                    parse_plus(
                        searchobj.group("melee_esp"), new['main']['melee_esp'],
                        verbose=verbose)
                    melee_crit_dmg = searchobj.group("melee_crit_dmg")

                    if melee_crit_dmg:
                        new['main']['melee_crit_dmg'].append(
                            int(melee_crit_dmg))
                    else:
                        new['main']['melee_crit_dmg'].append(2)

                if verbose:
                    pprint(new)
                    print("____________")
                if split == "+1 spear +17/+12/+7 ;1d8+7/x3":
                    pass
                continue

            # bite +21 ;3d6+8/19-20 plus grab
            #  tail slap +21 ;2d8+6
            searchobj = re.match(strings['single'], split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                    print(searchobj.group('melee'))
                melee = searchobj.group('melee')
                if melee:
                    new['main']['melee'].append(int(melee))
                else:
                    new['main']['melee'].append(0)

                new['main']['melee_desc'].append(
                    str(searchobj.group("melee_desc")))
                new['main']['melee_dmg'].append(
                    str(searchobj.group("melee_dmg")))

                if searchobj.group("melee_crit1"):
                    melee_crit = searchobj.group("melee_crit1")
                else:
                    melee_crit = searchobj.group("melee_crit2")
                new['main']['melee_crit'].append(melee_crit)

                if searchobj.group("melee_dmg"):
                    if verbose:
                        print("melee_dmg {}".format(
                            searchobj.group("melee_dmg")))
                    melee_esp = searchobj.group('melee_esp')
                    parse_plus(
                        melee_esp, new['main']['melee_esp'], verbose=verbose)
                else:
                    if verbose:
                        print("no melee_dmg")
                    melee_esp_match = re.match(
                        strings['esp_no_dmg'], split, re.I)
                    if melee_esp_match:
                        melee_esp = melee_esp_match.group('melee_esp')
                        if verbose:
                            print('found esp_no_dmg "{}"'.format(melee_esp))
                        parse_plus(
                            melee_esp, new['main']['melee_esp'],
                            verbose=verbose)
                        # print(new['main'])
                    else:
                        if verbose:
                            print('found no esp_no_dmg: "{}"'.format(split))
                        parse_plus(
                            split, new['main']['melee_esp'],
                            verbose=verbose)
                        # print(new['main'])

                melee_crit_dmg = searchobj.group("melee_crit_dmg")
                if melee_crit_dmg:
                    new['main']['melee_crit_dmg'].append(
                        int(melee_crit_dmg))
                else:
                    new['main']['melee_crit_dmg'].append(2)

                if verbose:
                    pprint(new)
                    print("____________")
                if split == "bite +5 ;1d6 plus 1d6 acid and disease":
                    pass
                continue

            # bite +5 ;1d6 plus 1d6 acid and disease
            searchobj = re.match(
                (
                    '(^|^ )(\w*|\w* \w*) \+(\d*) ;(\d*d\d*) '
                    'plus (\d*d\d*) (\w*|\w* \w*) and (\w*|\w* \w*)$'),
                split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                1/0
                new['main']['melee'].append(int(searchobj.group(3)))
                new['main']['melee_desc'].append(str(searchobj.group(2)))
                new['main']['melee_dmg'].append(str(searchobj.group(4)))
                new['main']['melee_crit'].append(None)
                new['main']['melee_esp'].append([
                    tuple((str(searchobj.group(6)), str(searchobj.group(5)))),
                    str(searchobj.group(7))
                ])
                melee_crit_dmg = searchobj.group("melee_crit_dmg")
                if melee_crit_dmg:
                    new['main']['melee_crit_dmg'].append(
                        int(melee_crit_dmg))
                else:
                    new['main']['melee_crit_dmg'].append(2)

                if verbose:
                    pprint(new)
                    print("____________")
                continue

            # DC 19 Fort half
            searchobj = re.match(strings['save_reduction1'], split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                if len(new['main']['melee']) == len(new['main']['melee_esp']):
                    if len(new['main']['melee_esp']) == 1:
                        new['main']['melee_esp'][0] = {
                            'save': {
                                'dc': searchobj.group('dc'),
                                'save': searchobj.group('save').lower(),
                                'effect': searchobj.group('effect')}}
                if verbose:
                    pprint(new)
                    print("____________")
                continue

            # DC 19 Fort half
            searchobj = re.match(strings['save_reduction2'], split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                if len(new['main']['melee']) == len(new['main']['melee_esp']):
                    if len(new['main']['melee_esp']) == 1:
                        new['main']['melee_esp'][0] = {
                            'save': {
                                'dc': searchobj.group('dc'),
                                'save': searchobj.group('save').lower(),
                                'effect': searchobj.group('effect')}}
                        if verbose:
                            pprint(new)
                            print("____________")
                        continue

            searchobj = re.match(
                (' *(and )*(?P<melee_esp>[a-z]*(( |-)[a-z]*)*) *'),
                split, re.I)
            if searchobj:
                if verbose:
                    print("split:", split)
                if len(new['main']['melee']) == len(new['main']['melee_esp']):
                    if len(new['main']['melee_esp']) == 1:
                        if new['main']['melee_esp'][0] is None:
                            new['main']['melee_esp'][0] = searchobj.group(
                                'melee_esp')
                            if verbose:
                                pprint(new)
                            continue
                            print("____________")
                        else:
                            new['main']['melee_esp'].append(
                                searchobj.group('melee_esp'))
                            if verbose:
                                pprint(new)
                                print("____________")
                            continue

                    else:
                        equal_status = True
                        for i in range(1, len(new['main']['melee_esp'])):
                            if verbose:
                                print('i {}'.format(i))
                            if (new['main']['melee_esp'][0] !=
                                    new['main']['melee_esp'][i]):
                                equal_status = False
                        if equal_status:
                            for i in range(len(new['main']['melee_esp'])):
                                if type(new['main']['melee_esp'][i]) != list:
                                    new['main']['melee_esp'][i] = [new['main'][
                                        'melee_esp'][i],
                                        searchobj.group('melee_esp')]
                                else:
                                    new['main']['melee_esp'][i].append(
                                        searchobj.group('melee_esp'))
                            continue
                elif len(new['main']['melee']) == 1:
                    new['main']['melee_esp'].append(
                        searchobj.group('melee_esp'))
                    if verbose:
                        pprint(new)
                        print("____________")
                    continue
                else:
                    if verbose:
                        print('else')
                        pprint(new)
                    # exit()

            print('WITHOUT "OR"')
            print("***{}***".format(line))
            print('error: "{}" remains'.format(split))
            print('currently parsed:')
            pprint(new)
            exit()
    return new
