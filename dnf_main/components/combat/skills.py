"""..."""

from dnf_game.dnf_main.components.combat import char_data


class SkillNode:
    """A node representing a specifig skill."""

    def __init__(self, name, properties, tree):
        """Create a new skill.

        Every skill starts untrained, with 0 ranks.
        """
        self.name = name
        self.tree = tree

        self.__dict__.update(properties)

        self.trained = False
        self.ranks = 0

    @property
    def available(self):
        """Available if skill can be used untrained or was trained."""
        return self.untrained or self.trained

    @property
    def acquireable(self):
        """..."""
        creature = self.tree.creature
        return self.ranks < creature.level

    @property
    def value(self):
        """Trained class skills have bonuses."""
        creature = self.tree.creature

        class_skill = 3 if (self.trained and creature._class in
                            char_data.data["class_skills"][self.name]) else 0
        base = self.ranks + class_skill
        """
        print("{}: trained {}, ranks {}, class skill {}, base {}".format(
            self.name, self.trained, self.ranks, class_skill, base))
        """

        return base + self.armor_penalty

    @property
    def check(self):
        """..."""
        creature = self.tree.creature
        return self.value + creature.att_mod_dict[self.ability]

    @property
    def check_debug(self):
        """..."""
        creature = self.tree.creature
        # return self.value + creature.att_mod_dict[self.ability]

        base = self.value
        att_mod = creature.att_mod_dict[self.ability]
        att = creature.attributes_dict[self.ability]
        value = base + att_mod
        string = "{} = {} + {} ({} {})".format(
            value,
            base,
            att_mod,
            self.ability,
            att
        )

        return string

    @property
    def armor_penalty(self):
        """Skill armor penaly.

        A character who is wearing armor with which he is not
        proficient applies its armor check penalty to all skill checks based
        on Dexterity or Strenght ('armor_check' is True).
        """
        creature = self.tree.creature

        if self.armor_check:
            equipped_in_slot = creature.equipped_in_slot("body")
            if equipped_in_slot:
                armor = equipped_in_slot
            else:
                return 0
            armor_feat = {
                "light armor": "armor proficiency (light)",
                "medium armor": "armor proficiency (medium)",
                "heavy armor": "armor proficiency (heavy)"
            }
            for armor_type, armor_feat in armor_feat.items():
                if armor.type == armor_type:
                    feat = creature.feats.get(armor_feat)
                    if feat.acquired:
                        return 0
                    else:
                        return armor.armor_check_penalty
        else:
            return 0

    def acquire(self):
        """..."""
        self.ranks += 1
        # print("Acquiring {}, new rank: {}".format(self.name, self.ranks))
        # print("New check {}".format(self.check))
        self.trained = True


class SkillTree:
    """A structure with all the skills."""

    skills = {}

    def __init__(self, creature):
        """Create the basic structure with every skill."""
        self.creature = creature

        self.spent_points = 0
        self.racial_bonus = 0

        for k, v in char_data.data["skills"].items():
            self.skills[k] = SkillNode(k, v, self)

        self.acquire_racial_skills()

    def acquire_racial_skills(self):
        """..."""
        race = self.creature.race
        racial_skills = char_data.data["racial_skill_mods"][race]
        for bonus in racial_skills:
            # eg ("intimidate", 2)
            # print(bonus)
            self.racial_bonus += bonus[1]
            # print("racial_bonus", self.racial_bonus)
            for i in range(bonus[1]):
                self.acquire(bonus[0], racial=True)

    @property
    def total_points(self):
        """Total skill points.

        At each level the character gains a certain ammount, determined by
        his class(es), adjusted by his Intelligence modifer (minimum of 1).
        """
        per_class = char_data.data["skills_per_class"][self.creature._class]
        per_int = self.creature.att_mod_dict["int"]
        # print("per_class", per_class)
        # print("per_int", per_int)
        base = max(per_class + per_int, 1)

        """Humans gain an additional skill rank at first level and one
        additional rank whenever they gain a level.
        """
        if self.creature.race == "human":
            base += 1
        # print("base", base)
        return (base * self.creature.level) + self.racial_bonus

    @property
    def available_points(self):
        """Available skill points to invest."""
        return self.total_points - self.spent_points

    def acquire(self, name, racial=False):
        """Add one rank to the skill."""
        skill = self.skills[name]
        if self.available_points and (racial or skill.acquireable):
            skill.acquire()
            self.spent_points += 1
