"""..."""

import random

from dnf_game.dnf_main.components.combat.char_roll import roll
from dnf_game.dnf_main.components.combat import loot_coins

"""Generating Gems
When randomly determining gems, roll on the appropriate grade chart. To
determine the gemstone's total value, roll the added value and add it to the
base value. If you would prefer the average value instead, simply double the
base value.

In addition, if the roll to determine the type of gem is an odd roll, the gem
is unworked, which means its value is equal to half the total value of a
normal gem of that type, but it can made into a worked gem with a successful
Craft (jewelry) check of the appropriate DC based on the gem's grade (the gem
counts as the raw material cost, so the crafter need not pay that amount).
On an even roll, the gem is worked, can't be improved upon, and is worth the
listed cost.
"""
descriptions = {
    'agate':
        'These banded stones are a variety of quartz, and take on a '
        'variety of shapes and patterns.',
    'alabaster':
        'This white- to cream-colored stone is thinly cut to create '
        'decorative surfaces or shaped into small objects.',
    'amber':
        'Derived from golden-yellow to golden-orange fossilized tree '
        'resin, pieces of amber sometimes contain insects, pine needles, and '
        'even more exotic flora and fauna.',
    'amethyst':
        'This rare purple or mauve quartz is thought by some to ward off '
        'drunkenness, and is thus held in particularly high esteem by lushes '
        'and winos.',
    'aquamarine':
        'These blue or sea green crystals are often faceted to show off '
        'their luster and reflective qualities.',
    'azurite':
        'This blue copper mineral is produced after copper deposits are '
        'exposed to the elements for a long time, and is used to make blue '
        'dyes as well as jewelry.',
    'bloodstone':
        'This variety of chalcedony is green and dotted with blood red '
        'jasper, and is also called heliotrope.',
    'carnelian':
        'This translucent red or orange mineral is most often polished '
        'to create beads, decorative pieces, and cameos.',
    'chrysoberyl':
        'These hard gemstones can be green, greenish yellow, or yellow '
        'brown. They are brilliant when cut, but often lack the fire of '
        'more precious stones.',
    'chrysoprase':
        'This apple-green decorative stone is sometimes confused with jade, '
        'and is used both decoratively and in the creation of cameos.',
    'citrine':
        'This pale yellow to golden yellow stone is a type of quartz and '
        'is used to create faceted gemstones and decorative objects.',
    'coral':
        'Borne from the sea, coral is not a true mineral, but is the '
        'red, blue, or black skeletal remains of minute marine animals '
        'called coral polyps.',
    'garnet':
        'These gems come in a variety of colors, from red and orange to '
        'yellow and green. They are commonly faceted to set into jewelry.',
    'hematite':
        'These stones have a dark and metallic luster, and are the '
        'chief source of mined iron.',
    'ivory':
        'Ivory comes from the teeth or tusks of elephants, hippopotamuses, '
        'boars, and some whales, and is carved to create both decorative '
        'and functional items.',
    'jade':
        'This bright to dull green stone is carved and polished to '
        'create decorative pieces, small carved statues or objects, '
        'and various ornaments.',
    'jasper':
        'This stone comes in shades of brown, red, yellow, green, and '
        'rarely blue. Sometimes it is striped. It is often carved and '
        'polished to make decorative pieces such as vases and amulets.',
    'jet':
        'This fossil stone is dark gray to black, and is formed from '
        'decaying wood that has been under great pressure for millions '
        'of years.',
    'lapis lazuli':
        'This spotted blue stone is a composed of several different '
        'minerals, primarily lazurite.',
    'malachite':
        'This opaque green stone is often banded with paler hues. It is '
        'made up of crystals that are too small to be faceted, but can '
        'be polished into striking decorative items.',
    'moonstone':
        "This clear stones namesake comes from its blue-white sheen, "
        "though some cultures believe the gem comes from the moon itself.",
    'obsidian':
        'This natural volcanic glass is often black, but blue, brown, '
        'green, red, and gray obsidian also exist. It is carved and '
        'polished into decorative items, and holds a sharp edge that makes '
        'it suitable for primitive blades.',
    'onyx':
        'This stone features curved bands of black, white, and brown '
        'minerals. It is used to make decorative objects.',
    'opal':
        'Found in white, black, and orange colors, the orange variety '
        'is often called a fire opal. Sometimes opals feature iridescent '
        'flashes of other colors. They can be both faceted and used to create '
        'decorative items and cameos.',
    'pearl':
        "Formed by various types of shellfish, pearls are created when "
        "grit gets stuck inside a creature's shell for an extended amount"
        "of time. Freshwater pearls tend to be irregular in shape, while "
        "saltwater pearls are typically a lustrous white and more evenly "
        "shaped. Black pearls are the rarest of pearls.",
    'peridot':
        'These olive green gems have an oily or greasy luster to them.',
    'quartz':
        'This common gem comes in a variety of forms. The nearly clear form '
        'of quartz is also known as rock crystal, and is the most common '
        'kind of quartz. Rose quartz has a pinkish hue, while smoky quartz '
        'is of a hazy brown color and is sometimes called brown quartz. As '
        'its name implies, milky quartz a milky white color. Quartz is '
        'very versatile, and can be carved, faceted, and crafted '
        'into decorative items.',
    'rhodochrosite':
        'These pink- and white-banded stones can be shaped into decorative '
        'items and cameos.',
    'sard':
        'This brownish red stone is often translucent and features '
        'patchy coloring.',
    'sardonyx':
        'This banded mix of sard and onyx is used to make decorative '
        'pieces and cameos.',
    'shell':
        'Shells come in many forms, and can be fashioned into decorative '
        'items or cameos. Sometimes a shell is beautiful enough to be '
        'considered worked even in its natural form.',
    'spinel':
        'Found in pink, blue, red, and star stone varieties, the most '
        'popular form of spinel is red, which is sometimes confused with '
        'a ruby.',
    'tigereye':
        "This golden and brown striped stone, when polished, looks like "
        "a cat's eye.",
    'topaz':
        'These transparent gems range wildly in color. They can be golden '
        'yellow, pink, gray, blue, or green, and are almost always faceted '
        'for fitting into jewelry.',
    'tourmaline':
        'These transparent stones can be crimson, blue, brown, or clear. '
        'They are almost always faceted for jewelry, especially rings '
        'and necklaces.',
    'turquoise':
        'This common gem is typically brilliant blue but is sometimes '
        'greenish blue. It is used to create decorative items, small '
        'figures, and cameos.',
    'zircon':
        'Clear varieties of this stone are often mistaken for diamonds, '
        'but are softer and often flawed. Zircon can be clear, green, '
        'golden, or brown.',
    'diamond':
        'The most popular diamonds are clear, but they can also be golden, '
        'pale pink, pink-red, gray-green, or even black. Among the hardest '
        'of minerals, only other diamonds can cut these gems. These gems '
        'are nearly always faceted.',
    'emerald':
        'These beautiful green gems are rarely flawless, with only '
        'brilliant green specimens being truly void of defects or '
        'impurities. These gems can be polished into decorative items, but '
        'are more often faceted for jewelry.',
    'ruby':
        'Only slightly softer than diamonds, these striking gemstones comes '
        'in numerous shades of red, and are often faceted but sometimes '
        'shaped and polished into decorative items.',
    'sapphire':
        'Sapphires are structurally almost identical to rubies, but are not '
        'red. While they can take on many colors, blue is the most highly '
        'sought after kind of sapphire. The most expensive sapphires are '
        'star sapphires.',
    'pyrite':
        "A brass-yellow mineral with a bright metallic luster. This mineral's "
        "metallic luster and pale brass-yellow hue give it a superficial "
        "resemblance to gold, hence the well-known nickname of fool's gold."

}
gems = {

    1: [  # grade 1
        # name, base + rolls * v
        ("agate", 5, "2d4", 1),
        ("alabaster", 5, "2d4", 1),
        ("azurite", 5, "2d4", 1),
        ("hematite", 5, "2d4", 1),
        ("lapis lazuli", 5, "2d4", 1),
        ("malachite", 5, "2d4", 1),
        ("obsidian", 5, "2d4", 1),
        ("pearl, irregular freshwater", 5, "2d4", 1),
        ("pyrite", 5, "2d4", 1),
        ("rhodochrosite", 5, "2d4", 1),
        ("quartz, rock crystal", 5, "2d4", 1),
        ("shell", 5, "2d4", 1),
        ("tigereye", 5, "2d4", 1),
        ("turquoise", 5, "2d4", 1)
    ],

    2: [
        ('bloodstone', 25, "2d4", 5),
        ('carnelian', 25, "2d4", 5),
        ('chrysoprase', 25, "2d4", 5),
        ('citrine', 25, "2d4", 5),
        ('ivory', 25, "2d4", 5),
        ('jasper', 25, "2d4", 5),
        ('moonstone', 25, "2d4", 5),
        ('onyx', 25, "2d4", 5),
        ('peridot', 25, "2d4", 5),
        ('quartz, milky', 25, "2d4", 5),
        ('quartz, rose', 25, "2d4", 5),
        ('quartz, smoky', 25, "2d4", 5),
        ('sard', 25, "2d4", 5),
        ('sardonyx', 25, "2d4", 5),
        ('spinel, red', 25, "2d4", 5),
        ('spinel, green', 25, "2d4", 5),
        ('zircon', 25, "2d4", 5)
    ],

    3: [
        ('amber', 50, "2d4", 10),
        ('amethyst', 50, "2d4", 10),
        ('chrysoberyl', 50, "2d4", 10),
        ('coral', 50, "2d4", 10),
        ('garnet', 50, "2d4", 10),
        ('jade', 50, "2d4", 10),
        ('jet', 50, "2d4", 10),
        ('pearl, saltwater', 50, "2d4", 10),
        ('spinel, deep blue', 50, "2d4", 10),
        ('tourmaline', 50, "2d4", 10)
    ],

    4: [
        ('aquamarine', 250, "2d4", 50),
        ('opal', 250, "2d4", 50),
        ('pearl, black', 250, "2d4", 50),
        ('topaz', 250, "2d4", 50)
    ],

    5: [
        ('diamond, small', 500, "2d4", 100),
        ('emerald', 500, "2d4", 100),
        ('ruby, small', 500, "2d4", 100),
        ('sapphire', 500, "2d4", 100)
    ],

    6: [
        ('diamond, large', 2500, "2d4", 500),
        ('emerald, brilliant green', 2500, "2d4", 500),
        ('ruby, large', 2500, "2d4", 500),
        ('sapphire, star', 2500, "2d4", 500)
    ]
}


class Gem:
    """..."""

    def __init__(self, name, value, unworked):
        """..."""
        self._name = name
        self._value = value
        self.unworked = unworked
        n = name.split(',')[0]
        self.description = descriptions[n]

    def __str__(self):
        """..."""
        # status = "(unworked)" if self.unworked else ""
        # return "{}: {}".format(self._name, self._value)

        return self._name if not self.unworked else (
            "{} (unworked)".format(self._name))

    def __repr__(self):
        """..."""
        return self.__str__()

    @property
    def name(self):
        """..."""
        return self.__str__()

    @property
    def value(self):
        """..."""
        return self._value // 2 if self.unworked else self._value

    @property
    def default_value(self):
        """..."""
        return self._value


def calculate_hoard(total):
    """..."""
    coins_part = int(total * 0.16)
    gem_total = 5 * int((total - coins_part) / 5)

    hoard = {
        'coins': loot_coins.calculate_hoard(coins_part),
        'gems': []
    }

    for i in range(6, 1 - 1, -1):
        while True:
            gem = gem_generation(i)
            if gem.default_value < gem_total:
                hoard['gems'].append(gem)
                gem_total -= gem.default_value
            else:
                break
    if not hoard['gems']:
        hoard['coins'] += loot_coins.calculate_hoard(total - coins_part)
    # print(hoard)
    # gem_total = sum(gem.default_value for gem in hoard)
    # print(total, coins_v, gem_total)
    # final = gem_total + coins_v
    # print(final)
    return hoard


def gem_generation(grade):
    """..."""
    name, base, dice, mult = random.choice(gems[grade])
    unworked = bool(random.randint(0, 1))
    roll_result = roll(string=dice)
    value = base + (roll_result * mult)
    # print(roll_result, mult, base, value)

    return Gem(name, value, unworked)

if __name__ == '__main__':
    hoard = calculate_hoard(10)
    print(hoard)
