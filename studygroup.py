from matchup import collection_done
from database import get_answer
from calculator import calc, State
from collections import defaultdict as ddict

pumps = {
    'K': ['Q: The first thing I like to do is to write down all the quantitative information in the question.',
          'C: When I have trouble sorting out the different types of quantities in a problem, I check out this table',
          "B: If the question mentions concepts I don't understand, I like to go to the chapter summary",
          'L: What was the first thing they did in the worked example?'],
    'I': ["Q: I like to reread the question to make sure I'm not missing any given quantities",
          'B: If it has units, write it down',
          'L: What other data did they use in the worked example?'],
    'Us': ['B: What are we trying to figure out? What <em>are</em> the unknowns?',
          'Q: If we look at the problem above, is there question marks somewhere, or keywords like "calculate" or "determine"?',
          'L: What were the unknowns in the worked example?'],
    'U': ['B: What are we trying to figure out? What is the unknown?',
          'Q: If we look at the problem above, is there a question mark somewhere, or a keyword like "calculate" or "determine"?',
          'L: What was the unknown in the worked example?'],
    'F': ['B: I like writing down the chemical equation of the reaction we are talking about.',
          'C: What type of reaction is this? Can we write it down?',
          'L: Was there a chemical equation in the worked example?'],
    'P': ['Q: There are multiple unknowns here. Which one should we start with?',
          'L: In what order did they proceed in the worked example?'],
    'S': ['Q: I think it might be time for some mathematical formula that connects knowns and unknowns.',
          'B: Could we just write down the mathematical equation that relates all the quantities (starting with an "@" so it is a comment)?',
          'C: chapter specific wisdom*',
          'L: How did they approach the calculation in the worked example?',
          'B: What are we trying to figure out again?',
          'Q: I love solving mathematical equations for the unknown... is it time for some of that?',
          'C: \nchapter specific wisdom*',
          'L: How did they approach the calculation in the worked example?'
          ],
    '@': ['Q: I think it might be time for some mathematical equation that connects knowns and unknowns.',
          'B: Could we just write down the mathematical equation that relates all the quantities (starting with an "@" so it is a comment)?',
          'C: chapter specific wisdom*',
          'L: How did they approach the calculation in the worked example?'],
    'A': ["Q: Let's check our work and then submit it to have it graded",
          'B: Does the answer have the correct units and is in the ballpark we expected? So submit already...',
          'L: One more look at the worked example, and then we are ready to submit?'],
}

book_of_wisdom = {
    '3': 'This chapter is all about chemical amounts of substances.\n '
         'Check whether the problem is about a pure substance (where you can use the molar mass M) '
         'or a solution (where you can use the definition of concentration or the dilution law) '
         'or about composition of a compound (where you can use the chemical formula).',
    '4': 'This chapter is about stoichiometry, i.e. how the amounts of substances in a reaction are related'
       ' to one another.\n We should make sure we have a balanced equation so we can apply\n'
       '@n_1 / ν_1 = n_2 / ν_2\n Stoichiometry problems are either about stoichiometric ratio (equation above) or about limiting reactant (if I have this much of one '
       'and this much of another reactant, how much can react before we run out of one reactant), where we can use'
         '\n@ n[->] = min(n_react1 / ν_1, n_react2 / ν_2, ...)'
}


def done(answer):
    for i, a in enumerate(answer):
        if '= ?' in a or '=?' in a:
            query = a.split('=')[0].rstrip()
            if not any(b.startswith(query) for b in answer[i+1:]):
                return False
    return True

pump = 0

def pumpit(hwid, inputlog, oldsymbols, reset=False):
    global pump
    if reset:
        pump = 0
        return
    try:
        if not oldsymbols:
            commands = pumps['K'][pump]
        else:
            answer, _ = get_answer(hwid[2:])
            answer = answer.splitlines()
            inputs = inputlog.splitlines()
            if not collection_done(inputlog, '\n'.join(answer)):
                commands = pumps['I'][pump]
            elif sum('= ?' in a for a in answer) > sum(('= ?' in b or '=?' in b) for b in inputs):
                if any(('= ?' in b or '=?' in b) for b in inputs):
                    commands = pumps['Us'][pump]
                else:
                    commands = pumps['U'][pump]
            elif any(a[0] == '!' for a in answer if a) and not any(b[0] == '!' for b in inputs if b):
                commands = pumps['F'][pump]
            elif any(a.startswith('Plan') for a in answer) and not any(b.startswith('Plan') for b in inputs):
                commands = pumps['P'][pump]
            elif any(a[0] == '@' for a in answer if a) and not any(b[0] == '@' for b in inputs if b):
                commands = pumps['@'][pump]
            elif not done(inputs):
                if any(a[0] == '@' for a in inputs if a) and pump < 4:
                    pump += 4
                commands = pumps['S'][pump]
            else:
                commands = pumps['A'][pump]
        pump += 1
    except IndexError:
        commands = '{"ico/B.jpg" height ="50" style="display: inline"}{"ico/Q.jpg" height ="50" style="display: inline"}{"ico/L.jpg" height ="50" style="display: inline"}{"ico/C.jpg" height ="50" style="display: inline"}<br>This is frustrating, we''re out&#33; Try office hours or a tutor, maybe?'
        pump = -1
    if commands[1] == ':' and commands[0] in 'BLCQ':
        commands = '{"ico/%s.jpg" width ="50" style="display: inline"}' % commands[0] + commands[2:]
        if 'mathematical equation' in commands:
            link = '<a href="./formulae%s" target="_blank">mathematical equation</a>' % hwid[2:].split('.')[0]
            commands = commands.replace('mathematical equation', link)
        if 'worked example' in commands:
            link = '<a href="./%s" target="_blank">worked example</a> ' % hwid[:-1]
            commands = commands.replace('worked example', link)
        if 'chapter summary' in commands:
            link = '<a href="./ico/summary.html#%s" target="_blank">chapter summary</a> ' % hwid[2:].split('.')[0]
            commands = commands.replace('chapter summary', link)
        if 'chapter specific wisdom*' in commands:
            chapter = hwid[2:-1].split('.')[0]
            if chapter in book_of_wisdom:
                wisdom = book_of_wisdom[chapter]
            else:
                wisdom = 'I got nothin'
            commands = commands.replace('chapter specific wisdom*', wisdom)
    result, good_input, = calc(oldsymbols, commands)
    outp, logp, memory, known, linespace = result
    return outp

formulae = ddict(list) # contains formulae by chapter, with priority
quantities = ddict(list)

def prep_formulae():
    with open('./mysite/formulae_examples.txt', 'r', encoding='utf-8') as inp:
        rawinput = inp.read()
    for ch in rawinput.split('\nChapter ')[1:]:
        chnr = int(ch.split('\n')[0].split(':')[0])
        #rint('Chapter', chnr)
        for form in ch.split('<hr>')[1:]:
            if form:
                formu = form.splitlines()
                formuheader = formu[1]
                formubody = '\n'.join(formu[3:])
                #rint('Formula', formuheader)
                p = int(formu[2][13])
                #rint('  Priority', p)
                formulae[chnr].append((formuheader, p, formubody))

prep_formulae()
print('\n'*4)

assessment = ['', '...important for many chemistry topics', '...might need one of those', '...less likely']

def show_formulae(chapter, cutoff = 3):
    out = []
    out.append('<h3>New from this chapter</h3>')
    collection = ddict(list)
    for ID, formula in enumerate(formulae[chapter]):
        collection[formula[1]].append((formula[0], ID))
    for priority in range(1,5+1):
        for f in collection[priority]:
            math, descr = f[0].split('#', maxsplit=1)
            out.append('%s@<a href="formulae%d.%d">%s</a>' % (math, chapter, f[1], descr))
    collection = ddict(list)
    for chap in range(1,chapter):
        for ID, f in enumerate(formulae[chap]):
            if f[1] <= cutoff:
                collection[f[1]].append((f[0], chap, ID))
    out.append('<h3>From previous chapters</h3>' )
    for priority in range(1,cutoff+1):
        out.append('<h4>%s</h4>' % assessment[priority])
        for f in collection[priority]:
            math, descr = f[0].split('#', maxsplit=1)
            out.append('%s@<a href="formulae%d.%d">%s</a>' % (math, f[1], f[2], descr))
    return '\n'.join(out)

def formula_details(chapter, ID):
    title = '<h3>Formula from Chapter %d</h3>\n' % int(chapter)
    out = formulae[int(chapter)][int(ID)]
    return title + out[0].replace('#','@') + '\n' + out[2]


print('************ 13 **************')
show_formulae(13)
print('************ 4 **************')
print(show_formulae(4))

def prep_quantities():
    with open('./mysite/quantities.txt', 'r', encoding='utf-8') as csvfile:
        headers = csvfile.__next__()[1:-1].split('\t')
        print('\n', headers)
        for row in csvfile:
            it = row[:-1].split('\t')
            newitems = [it[0], it[1]+' '+ it[2], it[3]+' ('+ it[4]+')', it[6], it[8], it[7]]
            try:
                quantities[int(newitems[0])].append(newitems)
            except:
                quantities[0].append(newitems[1:])

def html_table(lol):
    out = ['<h3>Common quantities up given chapter</h3>']
    out.append('<table>')
    out.append('  <tr>')
    out.extend('    <th>'+ b + '</th>' for b in lol[0])
    out.append('  </tr>')
    for sublist in lol[1:]:
        out.append('  <tr>')
        out.extend('    <td>' + b + '</td>' for b in sublist)
        out.append('  </tr>')
    out.append('</table>')
    return '\n'.join(out)


header =  ['Ch.', 'quantity and symbol', 'typical unit (symbol)', 'dimension', 'definition']

def show_quantities(chapter=1):
    items = [header]
    for q in quantities[chapter]:
        if q[4]:
            q[4] = '\n@' + q[4] + '\n'
        items.append(q[:5])
    for chap in range(1,chapter):
        for q in quantities[chap]:
            if q[5] and int(q[5]) < 3:
                items.append(q[:5])
    return(html_table(items))


prep_quantities()
print(show_quantities(8))