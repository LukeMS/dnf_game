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
                "condition": {
                    'object': 'owner.item.possessor.combat',
                    'attribute': '_class',
                    'value': "antipaladin"
                },
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
                "args": ["magic", 2]
            }
        ]
    }
}
