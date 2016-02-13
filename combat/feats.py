import os
import sys

try:
    import combat
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    import combat

from interpreter import interpreter

FEATS_DIC = {
    "armor proficiency (light)": {
        "name": "Armor Proficiency (Light)",
        "on_equip": [
            {
                "type": "check",
                "match": "all",  # "all" or "any" of the conditions
                "conditions": [
                    {
                        # if creature IS wearing light armor
                        'object': 'creature.equipped_armor',
                        'attribute': 'type',
                        'value': ("is", "light armor")
                    },
                    {
                        # and does NOT have light armor proficiency
                        'object': 'self',  # the very own feat
                        'attribute': 'acquired',
                        'value': ("not", True)
                        # 'value': ("is", False)  # another way, same result
                        # usable when compared value is not boolean
                    }
                ],

                True: [
                    {
                        # -1 penalty to attack from this feat
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "bab",
                            "value": ('$creature.equipped_armor.'
                                      'armor_check_penalty'),
                            "op": "-"
                        }
                    }
                ],

                False: [
                    {
                        # no penalty to attack from this feat
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "bab",
                            "value": 0
                        }
                    }
                ]
            }
        ]

    },

    "armor proficiency (medium)": {
        "name": "Armor Proficiency (Medium)",
        "requisites": {
            "feats": ["armor proficiency (light)"]
        },
        "on_equip": [
            {
                "type": "check",
                "match": "all",  # "all"|"any"
                "conditions": [
                    {
                        # if creature IS wearing medium armor
                        'object': 'creature.equipped_armor',
                        'attribute': 'type',
                        'value': ("is", "medium armor")
                    },
                    {
                        # and does NOT have medium armor proficiency
                        'object': 'self',  # the very own feat
                        'attribute': 'acquired',
                        'value': ("not", True)
                        # 'value': ("is", False)  # another way, same result
                        # usable when compared value is not boolean
                    }
                ],

                True: [
                    {
                        # -1 penalty to attack from this feat
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "bab",
                            "value": ('$creature.equipped_armor.'
                                      'armor_check_penalty'),
                            "op": "-"
                        }
                    }
                ],

                False: [
                    {
                        # no penalty to attack from this feat
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "bab",
                            "value": 0
                        }
                    }
                ]
            }
        ]

    },

    "armor proficiency (heavy)": {
        "name": "Armor Proficiency (Heavy)",
        "requisites": {
            "feats": ["armor proficiency (medium)"]
        },
        "on_equip": [
            {
                "type": "check",
                "match": "all",  # "all"|"any"
                "conditions": [
                    {
                        # if creature IS wearing medium armor
                        'object': 'creature.equipped_armor',
                        'attribute': 'type',
                        'value': ("is", "heavy armor")
                    },
                    {
                        # and does NOT have medium armor proficiency
                        'object': 'self',  # the very own feat
                        'attribute': 'acquired',
                        'value': ("not", True)
                        # 'value': ("is", False)  # another way, same result
                        # usable when compared value is not boolean
                    }
                ],

                True: [
                    {
                        # -1 penalty to attack from this feat
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "bab",
                            "value": ('$creature.equipped_armor.'
                                      'armor_check_penalty'),
                            "op": "-"
                        }
                    }
                ],

                False: [
                    {
                        # no penalty to attack from this feat
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "bab",
                            "value": 0
                        }
                    }
                ]
            }
        ]

    }

}

DEFAULT_FEAT = {
    "class_feature": False,
    "racial_trait": False,
    "acquired": False,
    "bab": 0,
    'requisites': {
        "feats": [],
        "others": []
    },
    "on_equip": [],  # called every time creature changes equipment
    "on_unequip": []
}


class FeatTree:
    feats = {}

    def __init__(self, creature):
        self.creature = creature

        self.points = 1

        if self.creature.race == "human":
            self.points += 1

        if self.creature._class == "fighter":
            self.points += 1

        for feat in FEATS_DIC:
            self.feats[feat] = FeatNode(feat=feat, tree=self)

    def acquire(self, feat_name):
        feat = self.feats[feat_name]
        if feat.acquireable:
            feat.acquired = True
            print("{} acquired".format(feat))
            return True
        else:
            return False

    def class_acquire(self):
        creature = self.creature
        for feat in self.feats:
            if feat.class_feature and creature._class in feat.class_req:
                feat.acquired = True
        if self.class_feature and "level" >= self.level_req:
            self.acquired = True
            print("{} acquired".format(self))
            return True
        else:
            return False

    def get(self, feat):
        return self.feats[feat]

    def on_equip(self):
        # print("\n", "#" * 6, "\n", "called FEAT_ON_EQUIP", "\n", "#" * 6)
        for feat in self.feats.values():
            interpreter(feat, feat.on_equip)  # if feat.on_equip

    def on_unequip(self):
        # print("\n", "#" * 6, "\n", "called FEAT_ON_EQUIP", "\n", "#" * 6)
        for feat in self.feats.values():
            interpreter(feat, feat.on_unequip)  # if feat.on_unequip

def set_default_recusevely(dic, default=DEFAULT_FEAT):
    for key, value in default.items():
        if isinstance(value, dict):
            dic.setdefault(key, {})
            set_default_recusevely(dic[key], default[key])
        else:
            dic.setdefault(key, value)


class FeatNode:
    """ Types of feat requisites:
    has feat x;
    feat x (class feature);
    feat x (weapon proficiency y)

    has rank x skill y;
    attribute x >= y;
    class x level y;
    caster level >= x;
    race
    racial trait
    darkvision (racial trait?)
    size
    save s with value v
    not class x or y

    ability to cast spell s
    cast "arcane" spell of elemental school "fire"
    paladin level x (cast paladin spells of level y)
    cast level l spells of class c or school s
    skill focus in skill that is considered class skill by bloodline
    worshiper of deity d
    has spell-like ability sla
    n type t feats
    proficienct with deity's chosen weapon
    ---
    skill.focus = True|False
    """

    def __init__(self, feat, tree):
        self.tree = tree

        template = FEATS_DIC[feat]

        self.__dict__.update(template)

        set_default_recusevely(self.__dict__)

    def __repr__(self):
        return "'{}: {}'".format(self.__class__.__name__, self.name)

    @property
    def creature(self):
        return self.tree.creature


    @property
    def acquireable(self):
        return self.available and not self.class_feature

    @property
    def available(self):
        dependencies = []
        available = True
        for feat_name in self.requisites['feats']:
            feat = self.tree.get(feat_name)
            if not feat.acquired:
                available = False
                dependencies.append(feat.name)

        for check in self.requisites['others']:
            pass
            # if check...
            #    result = False

        if not available:
            print("Missing dependencies:")
            for dependency in dependencies:
                print("    {}".format(dependency))

        return available

    def all_requisites(self):
        return self.req_feats

    def missing_requisites(self):
        return {feat for feat in self.req_feats if not feat.acquired}
