from random import randint, random, choice
from math import sqrt, exp
amino_acids = [1,4,14,2,17]
wildtype = [7,2,8,13,15]

expform = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form enctype="multipart/form-data" action="lab12" method="post" id="myform">
<h2>Directed evolution simulation</h2>
Try to change the sequence of a redox enzyme to accept NADH as a cofactor (see <a href="http://proteopedia.org/wiki/index.php/Arnold_lab:_coenzyme_specificity">link</a>)<br><br>
We do not know which phenotype (here: enzyme activity) a given genotype has; therefore, sampling from a library of random sequences with carefully chosen constraints can help to obtain the desired phenotype.

In this example, there is structural information available, so you can try a structure-guided strategy. Or you can do what nature does - introduce variation along the entire protein sequence.
Once you have multiple genotypes with improved phenotype, you can try to mix and match to see which changes work in synergy. Many changes in the gene will not have a large change
in phenotype or make it worse. Also, some changes in the genotype will affect protein stability to the point where the protein does not fold properly. Keep those ideas in mind while creating your experimental strategy,
and keep good notes so you can go back to genotypes that showed promise if you get stuck.<br><br>


<h3>Choose your experiment</h3>

What sequence are we starting with? (leave blank for wild type, or something like 200A 32G or F200A W32G)<br>
<input type="textarea" id="start" name="start" size="20"><br><br>
How many different clones do you want?
<input type="textarea" id="clones" name="clones" size="5">(you get more variation with more clones, but also more work/cost/time)<br><br>
What type of experiment?<br>
<input type="radio" id="what" name="what" value="site-saturation"> Site-saturation mutagenesis (below, enter the residue #, e.g. 200)<br>
<input type="radio" id="what" name="what" value="random"> Error-prone PCR (below, enter the average number of changes for each, e.g. 1.5)<br>
<input type="radio" id="what" name="what" value="combine"> Mix and match mutuations (below, list the choices for each residue #, e.g. 200EL 202GV)<br><br>
Parameters (depends on choice of experiment, see above)<br>
<input type="textarea" id="parameters" name="parameters" size="20"><br>
<input type="submit" name="start now" value="start now">
</form>
</body>
</html>'''

genetic_code = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
    'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
    'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W',
}

from collections import defaultdict

single_point = defaultdict(list)

other_three = {'A':'TCG', 'T':'CGA', 'C':'GAT', 'G':'ATC'}

for codon in genetic_code:
    aa = genetic_code[codon]
    first, middle, last = tuple(codon)
    for x in other_three[first]:
        single_point[aa].append(genetic_code[''.join([x, middle, last])])
    for x in other_three[last]:
        single_point[aa].append(genetic_code[''.join([first, x, last])])
    for x in other_three[last]:
        single_point[aa].append(genetic_code[''.join([first, middle, x])])

for aa in single_point:
    pass #rint (aa, ':', ''.join(sorted(single_point[aa])))

gaussian_skewed = [-6.28370e-1,
-1.61990e-1,
 3.83800e-1,
-6.81520e-2,
-1.54130e-1,
-1.28380e+0,
-1.21760e+0,
-2.30370e+0,
 8.34940e-1,
-8.99700e-1,
 1.21480e-2,
-3.21360e-2,
 1.34260e+0,
 4.85940e-1,
-7.19520e-1,
-3.82960e-1,
 1.00500e+0,
 3.19490e-1,
-1.12140e+0,
-3.99070e-1,]

gaussian = [-8.9940e-1,
-2.3780e-1,
 4.6450e-2,
 9.8170e-1,
-6.3910e-1,
-1.3200e+0,
 4.5180e-1,
-5.8460e-1,
-8.2790e-1,
-1.4760e+0,
 7.2790e-1,
 8.9160e-2,
 2.8660e+0,
 4.3170e-1,
-9.9280e-2,
 1.1440e+0,
-1.1080e+0,
 1.2880e-2,
-2.3600e-1,
 2.6410e-1,]

aa_one_list = list('ARNDCQEGHILKMFPSTWYV_')
aa_one_dict = {a:i for i,a in enumerate(aa_one_list)}

entire_wildtype = '''MSVKTKEKEMAVTILYEQDVDPKVIQGLKVGIIGYGSQGHAHALNLMDSGVDVRVGLREGSSSWKTAEEAGLKVTDMDTA
AEEADVIMVLVPDEIQPKVYQEHIAAHLKAGNTLAFAHGFNIHYGYIVPPEDVNVIMCAPKGPGHIVRRQFTEGSGVPDL
ACVQQDATGNAWDIVLSYCWGVGGARSGIIKATFAEETEEDLFGEQAVLCGGLVELVKAGFETLTEAGYPPELAYFECYH
EMKMIVDLMYESGIHFMNYSISNTAEYGEYYAGPKVINEQSREAMKEILKRIQDGSFAQEFVDDCNNGHKRLLEQREAIN
THPIETTGAQIRSMFSWIKKEDLEHHHHHH
'''

entire_wildtype = [aa_one_dict[a] for a in entire_wildtype if a != '\n']

#rint(entire_wildtype)


def activity(sequence, ideal):
    deltaGdagger = 0
    deltaStability = 0
    for nr in sequence:
        if nr in ideal:
            if sequence[nr] != ideal[nr]:
                deltaGdagger += gaussian[(ideal[nr] - sequence[nr])% 20 - 1] - 4
                for nr2 in sequence:
                    if nr2 in ideal and nr != nr2 and sequence[nr2] != ideal[nr2]:
                        #print('interactin', 2 * gaussian[(nr - nr2 + w2 - m2)% 20])
                        deltaGdagger += 0.3 * gaussian[(nr - nr2 + sequence[nr] - sequence[nr2])% 20]
        else:
            deltaGdagger += 0.3 * gaussian_skewed[(sequence[nr] + 13 * nr) % 20]
            deltaStability += gaussian_skewed[(sequence[nr] + 17 * nr) % 20]
    #rint("Stability", deltaStability)
    return 1000 * exp(deltaGdagger/2) if deltaStability > -2 else -1

'''
A set of 10 positions that might matter a lot is given to students.
3 of them actually matter, and they are sent to activity function.

All other mutations tend to destabilize protein and tend to lower activity,
but you could get lucky.

Start with user interface so testing becomes easier.

Protein to be used:

wildtype:
MSVKTKEKEMAVTILYEQDVDPKVIQGLKVGIIGYGSQGHAHALNLMDSGVDVRVGLREGSSSWKTAEEAGLKVTDMDTA
AEEADVIMVLVPDEIQPKVYQEHIAAHLKAGNTLAFAHGFNIHYGYIVPPEDVNVIMCAPKGPGHIVRRQFTEGSGVPDL
ACVQQDATGNAWDIVLSYCWGVGGARSGIIKATFAEETEEDLFGEQAVLCGGLVELVKAGFETLTEAGYPPELAYFECYH
EMKMIVDLMYESGIHFMNYSISNTAEYGEYYAGPKVINEQSREAMKEILKRIQDGSFAQEFVDDCNNGHKRLLEQREAIN
THPIETTGAQIRSMFSWIKKEDLEHHHHHH

S61D S63D I95V
                                                            * *
MSVKTKEKEMAVTILYEQDVDPKVIQGLKVGIIGYGSQGHAHALNLMDSGVDVRVGLREGDSDWKTAEEAGLKVTDMDTA
AEEADVIMVLVPDEV*QPKVYQEHIAAHLKAGNTLAFAHGFNIHYGYIVPPEDVNVIMCAPKGPGHIVRRQFTEGSGVPDL
ACVQQDATGNAWDIVLSYCWGVGGARSGIIKATFAEETEEDLFGEQAVLCGGLVELVKAGFETLTEAGYPPELAYFECYH
EMKMIVDLMYESGIHFMNYSISNTAEYGEYYAGPKVINEQSREAMKEILKRIQDGSFAQEFVDDCNNGHKRLLEQREAIN
THPIETTGAQIRSMFSWIKKEDLEHHHHHH


'''
important_sites = {61,63,95}
wildtype = {61:'S', 63:'S', 95:'I'}
for nr in wildtype:
    wildtype[nr] = aa_one_dict[wildtype[nr]]

best_NADH =  {61:'D', 63:'D', 95:'V'}
for nr in best_NADH:
    best_NADH[nr] = aa_one_dict[best_NADH[nr]]



def stability(mutant, wildtype):
    '''
    If =, stability should be zero. The more mutations, the greater the range.
    The more mutations, the lower the average
    '''
    single_effect = 0.0
    changes = 0
    for m, w in zip(mutant, wildtype):
        if m != w:
            changes += 1
            single_effect += gaussian[(w - m)% 20 - 1]
    if not changes:
        return 0.0
    if changes > 1:
        correlation_effect = gaussian[(sum(mutant) - sum(wildtype)) % 20]
        scaled_effect = 0.5 * sqrt(changes) * (correlation_effect - 1)
    else:
        scaled_effect = 0.0
    return scaled_effect + single_effect


def error_prone(wildtype, number, average):
    size = len(wildtype)
    chance = average/size
    for _ in range(number):
        mutations = {}
        for rn, aa in enumerate(wildtype):
            if random() < chance:
                #print(aa)
                amino_acid = choice(single_point[aa_one_list[aa]])
                mutations[rn+1] = aa_one_dict[amino_acid]
        yield mutations

aa_list = ['Ala', 'Arg', 'Asn', 'Asp', 'Cys', 'Gln', 'Glu', 'Gly', 'His', 'Ile', 'Leu', 'Lys', 'Met', 'Phe', 'Pro', 'Ser', 'Thr', 'Trp', 'Tyr', 'Val', 'Stop']
aa_dict = {a:i for i,a in enumerate(aa_list)}

NNK = 'Phe Leu Ser Ser Tyr Stop Cys Trp Leu Leu Pro Pro His Arg Arg Gln Ile Met Thr Thr Asn Lys Ser Arg Val Val Ala Ala Asp Glu Gly Gly'.split()
NNK_list = [aa_dict[i] for i in NNK]

#print (NNK_list)
def site_saturation_NNK(site, number):
    for _ in range(number):
        aa = choice(NNK_list)
        if aa == '20':
            yield None, aa
        else:
            yield site, aa



def combine(sequences, samples):
    sequence = wildtype.copy()
    for _ in range(samples):
        for nr, s in sequences:
            new_aa = choice(s)
            sequence[nr] = new_aa
        yield sequence


def pretty_mut(mut):
    if not mut:
        return 'original'
    if any(mut[x] == '_' for x in mut):
        return 'nonsense: ' + ', '.join(str(x) + mut[x] for x in mut)
    return ', '.join(aa_one_list[entire_wildtype[x-1]] + str(x) + aa_one_list[mut[x]] for x in mut if entire_wildtype[x-1] != mut[x])


def parse_mutation(string):
    string = string.replace(',', ' ').replace(';', ' ')
    try:
        mutation = {}
        for m in string.split():
            if m[0].isdigit():
                nr = int(m[:-1])
            else:
                nr = int(m[1:-1])
            aa = aa_one_dict[m[-1].upper()]
            mutation[nr] = aa
        return mutation
    except:
        return({})

def assess_result(mut, start_changes):
    for nr in start_changes:
        if nr not in mut:
            mut[nr] = start_changes[nr]
    label = pretty_mut(mut)
    if any(mut[a] == 20 for a in mut):
        r = 'truncated'
    else:
        act = activity(mut, wildtype)
        if act == -1:
            r = 'not stable'
        else:
            seq2 = wildtype.copy()
            for a in mut:
                seq2[a] = mut[a]
            act2 = activity(seq2, best_NADH)
            r = (act, act2)
    return label, r


def random_changes(entire_wildtype, start_changes, parameters, clones):
    try:
        mutation_rate = float(parameters)
    except:
        mutation_rate = 1.5
    start_sequence = entire_wildtype.copy()
    for nr in start_changes:
        start_sequence[nr] = start_changes[nr]
    result = []
    for mut in error_prone(start_sequence, clones, mutation_rate):
        result.append(assess_result(mut, start_changes))
    return result

def saturated_site (start_changes, parameters, clones):
    nr = int(parameters)
    result = []
    for rn, aa in site_saturation_NNK(nr, clones):
        mut = {rn: aa}
        result.append(assess_result(mut, start_changes))
    return result


def parse_choices(item):
    for i, c in enumerate(item):
        if not c.isdigit():
            break
    nr = int(item[:i])
    choices = [aa_one_dict[i] for i in item[i:]]
    return nr, choices


def combine_mutations (start_changes, parameters, clones):
    sequence = {}
    sites = {}
    for item in parameters.split():
        nr, choices = parse_choices(item)
        sites[nr] = choices
    result = []
    for _ in range(clones):
        for nr in sites:
            new_aa = choice(sites[nr])
            sequence[nr] = new_aa
        result.append(assess_result(sequence, start_changes))
    return result




def directed_evolution(start, typexp, parameters, clones):
    start_sequence = parse_mutation(start)
    if typexp == 'random':
        result = random_changes(entire_wildtype, start_sequence, parameters, clones)
        outp = ['Picking %d clones from a library of random changes generated by error-prone PCR of of a template encoding for %s' %
                  (clones, pretty_mut(start_sequence))]
    elif typexp == 'site-saturation':
        result = saturated_site (start_sequence, parameters, clones)
        outp = ['Picking %d clones from a library of changes in residue #%s starting with a template encoding for %s. There are 32 different codons in an NNK-mutagenic primer.' %
                  (clones, parameters, pretty_mut(start_sequence))]
    elif typexp == 'combine':
        outp = ['Picking %d clones from a library combining variation in multiple sites (%s) starting with a template encoding for %s' %
                  (clones, parameters, pretty_mut(start_sequence))]
        result = combine_mutations (start_sequence, parameters, clones)
    outp.append('Shown below are enzyme activities (in arbitrary units) for the samples variants<br><br><table width="50%" style="border:1px solid black;border-collapse:collapse;"><tr><th style="border:1px solid black;border-collapse:collapse;">activity with NADH</th><th style="border:1px solid black;border-collapse:collapse;">activity with NADPH</th><th style="border:1px solid black;border-collapse:collapse;">mutation</th></tr>')
    for item in result:
        outp.append('\n<tr>')
        if len(item[1]) == 2:
            outp.append('<td align="right" style="border:1px solid black;border-collapse:collapse;">%7.2f</td><td  style="border:1px solid black;border-collapse:collapse;" align="right">%7.2f</td><td align="middle" style="border:1px solid black;border-collapse:collapse;">%s</td>' % (item[1][1], item[1][0], item[0]))
        else:
            outp.append('<td colspan="2" style="border:1px solid black;border-collapse:collapse;">%s</td><td style="border:1px solid black;border-collapse:collapse;" align="middle">%s</td>' % (item[1], item[0]))
        outp.append('</tr>')
    outp.append('</table>')
    return '\n'.join(outp)


def newpheno():
    return expform

def workpheno(start, clones, what, parameters):
    result = 'working on it'
    print (start, clones, what, parameters)
    iclones = int(clones)
    result = directed_evolution(start, what, parameters, iclones)
    return result


if __name__ == '__main__':
    result = directed_evolution('', 'combine', '63SD 95LV', 20)
    result = result + directed_evolution('63D 95V', 'site-saturation', '61', 20)
    result = result + directed_evolution('34K', 'random', '2.0', 20)
    print(result)

    print(wildtype)
    print(best_NADH)

    for trial in ['61D 95V 63D', '61R', '61D', '']:
        sequence = wildtype.copy()

        for mut in trial.split():
            nr = int(mut[:-1])
            aa = mut[-1]
            aa_nr = aa_one_dict[aa]
            if nr in important_sites:
                sequence[nr] = aa_nr
        print()
        print(trial if trial else 'wildtype', ':', sequence)
        print('NADH activity:', '%8.3f' % activity(sequence, best_NADH))
        print('NADPH activity:', '%8.3f' % activity(sequence, wildtype))

    print('\n\nSite saturation residue number 61')
    sequence = wildtype.copy()
    sequence[63] = aa_one_dict['D']
    for rn, aa in site_saturation_NNK(61, 90):
        if rn and aa != 20:
            sequence[rn] = aa
            nadh = activity(sequence, best_NADH)
            nadph = activity(sequence, wildtype)
            print('%s%d %8.1f %8.1f %8.5f' % (aa_list[aa], rn, nadh, nadph, nadh / nadph))
        else:
            print('nonsense   n/a      n/a      n/a')

    D = aa_one_dict['D']
    S = aa_one_dict['S']

    for s in combine([(61, (D, S, 7)), (63, (D, S))], 10):
        print(s)
        nadh = activity(s, best_NADH)
        nadph = activity(s, wildtype)
        print('%8.1f %8.1f %8.5f' % (nadh, nadph, nadh / nadph))

    sampled = set()
    for rn, aa in site_saturation_NNK(2, 90):
        sampled.add(aa)

    # print(len(sampled), sorted(sampled))
    print('NNK strategy with 90 samples missed: ',
          ', '.join([aa_list[i] for i in (set(range(0, 21)) - sampled)]) if len(sampled) < 21 else 'nothing')



