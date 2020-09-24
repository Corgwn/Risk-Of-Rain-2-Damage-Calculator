from funcs import calc_dmg, syringeSpeed, predatorySpeed, kjaro, runald
import os

def main():
    items = ['Sticky Bomb', 'Tri-Tip Dagger', 'Lens-Makers Glasses', 'Ukulele', 'AtG Mk1',
             "Kjaro's Band", "Runald's Band", "Harvester's Scythe", 'Predatory Instincts',
             '57 Leaf Clover', 'Brilliant Behemoth', 'Sentient Meat Hook', 'Shaped Glass',
             "Soldier's Syringe", 'Purity']
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

    orig_dmg = int(input('Enter the base dmg of the attack: __%\n')) / 100
    orig_coeff = int(input('Enter the base proc coefficient of the attack: __%\n')) / 100

    dmg_increase = 1
    if item_counts['Shaped Glass'] >= 1:
        dmg_increase *= 2 ** (item_counts['Shaped Glass'])
    luck = item_counts['57 Leaf Clover'] - item_counts['Purity']
    dmg_increase = calc_dmg(item_counts, base_dmg=orig_dmg, coefficient=orig_coeff, luck=luck)    

    max_attack_speed = (1 + syringeSpeed(item_counts["Soldier's Syringes"]) 
                        + predatorySpeed(item_counts['Predatory Instincts']))

    with open('output_file.txt', 'w') as f:
        f.write('%d' % (dmg_increase * 100) + '% dmg increase\n' +
                '%d' % (max_attack_speed * 100) + '% attack speed increase\n'
                '%d' % ((kjaro(item_counts["Kjaro's Band"]) + runald(item_counts["Runald's Band"])) * 100)
                + '% dmg on Runald/Kjaro\'s Band\n')

    print('%d' % (dmg_increase * 100) + '% dmg')


if __name__ == '__main__':
    main()
