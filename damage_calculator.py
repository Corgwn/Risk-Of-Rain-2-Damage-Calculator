from funcs import calculate_damage, syringeSpeed, predatorySpeed
import os

def main():
    items = ['Sticky Bomb', 'Tri-Tip Dagger', 'Lens-Makers Glasses', 'Ukulele', 'AtG Mk1',
             'Kjaro\'s Band', 'Runald\'s Band', 'Harvester\'s Scythe', 'Predatory Instincts',
             '57 Leaf Clover', 'Brilliant Behemoth', 'Sentient Meat Hook', 'Shaped Glass',
             'Soldier\'s Syringe']
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

    damage_increase = 1
    if item_counts['Shaped Glass'] >= 1:
        damage_increase *= 2 ** (item_counts['Shaped Glass'])
    damage_increase = calculate_damage(item_counts, base_damage=original_damage)    

    max_attack_speed = (1 + syringeSpeed(item_counts["Soldier's Syringes"]) 
                        + predatorySpeed(item_counts['Predatory Instincts']))

    with open('output_file.txt', 'w') as f:
        f.write('%d' % (damage_increase * 100) + '% damage increase\n' +
                '%d' % (max_attack_speed * 100) + '% attack speed increase\n')

    print('%d' % (damage_increase * 100) + '% damage')


if __name__ == '__main__':
    main()
