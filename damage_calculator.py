import math
import os


def ukulele(ukulele_count, clover_count, coefficient):
    chance = coefficient * .25
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    avg_damage = chance * (.8 * (1 + (2 * ukulele_count)))
    return avg_damage


def atg(atg_count, clover_count, coefficient):
    chance = coefficient * .1
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    avg_damage = (atg_count * 3) * chance
    return avg_damage


def meat_hook(hook_count, clover_count, coefficient):
    chance = coefficient * ((100 * hook_count / (hook_count + 5)) / 100)
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    avg_damage = chance * (5 + (5 * hook_count))
    return avg_damage


def kjaro(kjaro_count, clover_count, coefficient):
    chance = coefficient * .08
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    if kjaro_count == 1:
        avg_damage = 5 * chance
    elif kjaro_count > 1:
        avg_damage = (2.5 + (2.5 * kjaro_count)) * chance
    else:
        avg_damage = 0
    return avg_damage


def runald(runald_count, clover_count, coefficient):
    chance = coefficient * .08
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    if runald_count == 1:
        avg_damage = 2.5 * chance
    elif runald_count > 1:
        avg_damage = (1.25 + (1.25 * runald_count)) * chance
    else:
        avg_damage = 0
    return avg_damage


def sticky(sticky_count, clover_count, coefficient):
    chance = coefficient * 0.05 * sticky_count
    if chance > 1:
        chance = 1
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    avg_damage = chance * 1.8
    return avg_damage


def tri_tip(dagger_count, clover_count, coefficient):
    chance = coefficient * 0.15 * dagger_count
    if chance > 1:
        chance = 1
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    avg_damage = chance * 0.2 * (12 / math.floor(1 / coefficient))
    return avg_damage


def crit_chance(item_counts, clover_count):
    chance = ((item_counts['Lens-Makers Glasses'] * .1)
              + (0.05 if item_counts["Harvester's Scythe"] >= 1 else 0)
              + (0.05 if item_counts["Predatory Instincts"] >= 1 else 0))
    if chance > 1:
        chance = 1
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    avg_crit_damage = chance
    return avg_crit_damage


def chance(base_chance, clover_count, coefficient):
    chance = coefficient * base_chance
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    return chance


def meat_hook_chance(hook_count, clover_count, coefficient):
    chance = coefficient * ((100 * hook_count / (hook_count + 5)) / 100)
    chance = 1 - ((1 - chance) ** (clover_count + 1))
    return chance


def calculate_damage(item_counts, base_damage=1.0, coefficient=1.0, proc=None, proc_2=None, proc_3=None):
    damage_sum = base_damage
    damage_sum += base_damage * sticky(item_counts['Sticky Bomb'], item_counts['57 Leaf Clover'], coefficient)
    damage_sum += tri_tip(item_counts['Tri-Tip Dagger'], item_counts['57 Leaf Clover'], coefficient)
    damage_sum += base_damage * kjaro(item_counts["Kjaro's Band"], item_counts['57 Leaf Clover'], coefficient)
    damage_sum += base_damage * runald(item_counts["Runald's Band"], item_counts['57 Leaf Clover'], coefficient)

    if ('Ukulele' not in [proc, proc_2, proc_3]) and (item_counts['Ukulele'] >= 1):
        damage_sum += (chance(.25, item_counts['57 Leaf Clover'], coefficient) * (1 + (2 * item_counts['Ukulele']))
                       * calculate_damage(item_counts, base_damage=.8, coefficient=.2, proc='Ukulele', proc_2=proc,
                                          proc_3=proc_2))

    if ('AtG Mk1' not in [proc, proc_2, proc_3]) and (item_counts['AtG Mk1'] >= 1):
        damage_sum += (chance(.1, item_counts['57 Leaf Clover'], coefficient)
                       * calculate_damage(item_counts, base_damage=3.0, coefficient=1.0, proc='AtG Mk1', proc_2=proc,
                                          proc_3=proc_2))

    if ('Sentient Meat Hook' not in [proc, proc_2, proc_3]) and (item_counts['Sentient Meat Hook'] >= 1):
        damage_sum += (meat_hook_chance(item_counts['Sentient Meat Hook'], item_counts['57 Leaf Clover'], coefficient)
                       * (5 + (5 * item_counts['Sentient Meat Hook']))
                       * calculate_damage(item_counts, base_damage=1.0, coefficient=0.33, proc='Sentient Meat Hook',
                                          proc_2=proc, proc_3=proc_2))

    if item_counts['Brilliant Behemoth'] >= 1:
        damage_sum += base_damage * 1.6

    crit_damage = crit_chance(item_counts, item_counts['57 Leaf Clover'])
    damage_sum += (crit_damage * damage_sum)

    return damage_sum


def main():
    items = ['Sticky Bomb', 'Tri-Tip Dagger', 'Lens-Makers Glasses', 'Ukulele', 'AtG Mk1',
             'Kjaro\'s Band', 'Runald\'s Band', 'Harvester\'s Scythe', 'Predatory Instincts',
             '57 Leaf Clover', 'Brilliant Behemoth', 'Sentient Meat Hook', 'Shaped Glass']
    item_counts = {}
    with open('input_file.txt', 'a') as f:
        if os.path.getsize('input_file.txt') == 0:
            for item in items:
                new_line = item + ': 0\n'
                f.write(new_line)

    with open('input_file.txt', 'r') as f:
        for line in f:
            parts = line.split(':')
            parts[1] = int(parts[1][1:])
            item_counts[parts[0]] = parts[1]

    original_damage = int(input('Enter the base damage of the attack: __%\n')) / 100

    damage_increase = calculate_damage(item_counts, base_damage=original_damage)

    if item_counts['Shaped Glass'] >= 1:
        damage_increase *= 2 ** (item_counts['Shaped Glass'])

    print('%d' % (damage_increase * 100) + '% damage')


if __name__ == '__main__':
    main()
