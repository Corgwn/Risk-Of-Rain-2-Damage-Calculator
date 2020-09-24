import math
import os


def ukulele(ukulele_count, luck, coefficient):
    chance = coefficient * .25
    chance = 1 - ((1 - chance) ** (luck + 1))
    avg_dmg = chance * (.8 * (1 + (2 * ukulele_count)))
    return avg_dmg


def atg(atg_count, luck, coefficient):
    chance = coefficient * .1
    chance = 1 - ((1 - chance) ** (luck + 1))
    avg_dmg = (atg_count * 3) * chance
    return avg_dmg


def meat_hook(hook_count, luck, coefficient):
    chance = coefficient * ((100 * hook_count / (hook_count + 5)) / 100)
    chance = 1 - ((1 - chance) ** (luck + 1))
    avg_dmg = chance * (5 + (5 * hook_count))
    return avg_dmg


def kjaro(kjaro_count):
    if kjaro_count > 0:
        dmg = (3 + (3 * kjaro_count))
    return dmg


def runald(runald_count):
    if runald_count > 0:
        dmg = (2.5 + (2.5 * runald_count))
    return dmg


def sticky(sticky_count, luck, coefficient):
    chance = coefficient * 0.05 * sticky_count
    if chance > 1:
        chance = 1
    chance = 1 - ((1 - chance) ** (luck + 1))
    avg_dmg = chance * 1.8
    return avg_dmg


def tri_tip(dagger_count, luck, coefficient):
    chance = coefficient * 0.15 * dagger_count
    if chance > 1:
        chance = 1
    chance = 1 - ((1 - chance) ** (luck + 1))
    avg_dmg = chance * 0.2 * (12 / math.floor(1 / coefficient))
    return avg_dmg


def crit_chance(item_counts, luck):
    chance = ((item_counts['Lens-Makers Glasses'] * .1)
              + (0.05 if item_counts["Harvester's Scythe"] >= 1 else 0)
              + (0.05 if item_counts["Predatory Instincts"] >= 1 else 0))
    if chance > 1:
        chance = 1
    chance = 1 - ((1 - chance) ** (luck + 1))
    avg_crit_dmg = chance
    return avg_crit_dmg


def chance(base_chance, luck, coefficient):
    chance = coefficient * base_chance
    chance = 1 - ((1 - chance) ** (luck + 1))
    return chance


def meat_hook_chance(hook_count, luck, coefficient):
    chance = coefficient * ((100 * hook_count / (hook_count + 5)) / 100)
    chance = 1 - ((1 - chance) ** (luck + 1))
    return chance


def calc_dmg(item_counts, base_dmg=1.0, coefficient=1.0, proc=None, proc_2=None, proc_3=None, luck=0):
    dmg_sum = base_dmg
    dmg_sum += base_dmg * sticky(item_counts['Sticky Bomb'], item_counts['57 Leaf Clover'], coefficient)
    dmg_sum += tri_tip(item_counts['Tri-Tip Dagger'], item_counts['57 Leaf Clover'], coefficient)

    if ('Ukulele' not in [proc, proc_2, proc_3]) and (item_counts['Ukulele'] >= 1):
        dmg_sum += (chance(.25, item_counts['57 Leaf Clover'], coefficient) * (1 + (2 * item_counts['Ukulele']))
                       * calc_dmg(item_counts, base_dmg=.8, coefficient=.2, proc='Ukulele', proc_2=proc,
                                          proc_3=proc_2))

    if ('AtG Mk1' not in [proc, proc_2, proc_3]) and (item_counts['AtG Mk1'] >= 1):
        dmg_sum += (chance(.1, item_counts['57 Leaf Clover'], coefficient)
                       * calc_dmg(item_counts, base_dmg=3.0, coefficient=1.0, proc='AtG Mk1', proc_2=proc,
                                          proc_3=proc_2))

    if ('Sentient Meat Hook' not in [proc, proc_2, proc_3]) and (item_counts['Sentient Meat Hook'] >= 1):
        dmg_sum += (meat_hook_chance(item_counts['Sentient Meat Hook'], item_counts['57 Leaf Clover'], coefficient)
                       * (5 + (5 * item_counts['Sentient Meat Hook']))
                       * calc_dmg(item_counts, base_dmg=1.0, coefficient=0.33, proc='Sentient Meat Hook',
                                          proc_2=proc, proc_3=proc_2))

    if item_counts['Brilliant Behemoth'] >= 1:
        dmg_sum += base_dmg * 1.6

    crit_dmg = crit_chance(item_counts, item_counts['57 Leaf Clover'])
    dmg_sum += (crit_dmg * dmg_sum)

    return dmg_sum


def syringeSpeed(num_syringes):
    #Each syringe gives .15 increase to attack speed
    return 0.15 * num_syringes


def predatorySpeed(num_predatory):
    speed_increase = 0
    if (num_predatory > 0):
        #The first predatory gives max of .36, each subsequent gives .24
        speed_increase += .12
        speed_increase += num_predatory * .24
    return speed_increase