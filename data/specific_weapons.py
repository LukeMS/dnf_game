"""Specific (named) weapons."""

SPECIFIC = {
    "bastard's sting": {
        "masterwork": 1,
        "magic": 2,
        "on_turn_actions": [],
        "on_hit_actions": [],
        "base_item": 'bastard sword',
        "on_equip": [
            {
                "type": "check",
                "match": "all",  # "all" or "any" of the conditions
                "conditions": [
                    {
                        # if creature IS of class antipaladin
                        'object': 'owner.item.possessor.combat',
                        'attribute': '_class',
                        'value': ("is", "antipaladin")
                    }
                ],
                True: [
                    {
                        "type": "action",
                        "action": "add_to",
                        "args": {
                            "category": "on_hit",
                            "actions": ["unholy"]
                        }
                    },
                    {
                        "type": "action",
                        "action": "add_to",
                        "args": {
                            "category": "on_turn",
                            "actions": ["unholy aurea"]
                        }
                    },
                    {
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "magic",
                            "value": 5
                        }
                    }
                ],
                False: [
                    {
                        "type": "action",
                        "action": "set_attribute",
                        "args": {
                            "field": "magic",
                            "value": 2
                        }
                    }
                ]
            }
        ],
        "on_unequip": [
            {
                "type": "action",
                "action": "remove_from",
                "args": {
                    "category": "on_hit",
                    "actions": ["unholy"]
                },
            },
            {
                "type": "action",
                "action": "remove_from",
                "args": {
                    "category": "on_turn",
                    "actions": ["unholy aurea"]
                },
            },
            {
                "type": "action",
                "action": "set_attribute",
                "args": {
                    "field": "magic",
                    "value": 2
                }
            }
        ]
    }
}
