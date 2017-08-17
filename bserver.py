# coding=utf-8

from bottle import get, post, run, request, response, static_file, default_app
from http import cookies


"""
Module to tie the quantities, calculator, and form modules together into an online calculator.

The calculator is hosted on ktheis.pythonanywhere.com, but you could have a local server or run it
on other platforms. In the calculator, you define values of named physical quantities,
and then do arithmetic with them. The web server is implemented using web.py.

"""
from calculator import calc, State
from comments import extract_knowns, create_comment
from form import newform, printableLog, helpform, exdict
from database import get_example, get_answer
from exampletracer import grade_answer, generate_hints, generate_tutor_comments
from chemistry import show_formulae, formula_details, show_quantities


@get('/')
def index_get():
    known = [' -- nothing yet -- ']
    browser = request.environ.get('HTTP_USER_AGENT')
    return newform(('', '', '', known, ''), '', '', browser=browser)


@post('/')
def index_post():
    # response.set_header('Content-Type', 'text/html; charset=utf-8')
    response.set_header('X-XSS-Protection', '0')
    browser = request.environ.get('HTTP_USER_AGENT').lower()
    if request.forms.get('sub') == "reset":
        return newform(('', '', '', '', ''), '', '', browser=browser)

    oldmemory = request.forms.get('memory')
    if request.forms.get('sub') == "help":
        return helpform()

    oldinputlog = request.forms.get('inputlog')
    oldlogbook = request.forms.get('logbook')
    if request.forms.get('sub') == "export":
        return printableLog(State(oldmemory), oldlogbook, oldinputlog)

    commands = request.forms.get('commands')
    result, newinputlog = calc(oldmemory, commands)
    # verboselog, brieflog, memory, known, linespace = result

    inputlog = oldinputlog + newinputlog
    if request.forms.get('sub') == " Save ":
        with open('logfile.txt', 'a', encoding='utf-8') as logfile:
            print(inputlog, file = logfile)
            print(inputlog)
        return helpform()
    return newform(result, oldlogbook, inputlog)


@get('/ico/:file')
def send_ico(file):
    return static_file(file, root='static/')


@get('/<nr:re:example.*>')
def example(nr):
    """
    Shows the PQCalc form pre-filled with example calculation commands.
    """
    # web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
    browser = request.environ.get('HTTP_USER_AGENT').lower()
    # browser = web.ctx.env['HTTP_USER_AGENT'].lower()
    known = ["nothing yet"]
    prefill = nr.split('example')[1]
    return newform(('', '', '', known, ''), '', '', prefill=prefill)


@get('/<nr:re:workedexample.*>')
def workedexample(nr):
    """
    Presents a worked example.
    """
    response.set_header('X-XSS-Protection', '0')
    browser = request.environ.get('HTTP_USER_AGENT').lower()
    prefill = nr.split('example')[1]
    text = exdict[prefill][:-2]
    if '<h4>Answer:</h4>' in text:
        text = text.split('<h4>Answer:</h4>')[0]
    result, good_input = calc('', text)
    logbook = ''
    pref = '\n'.join(extract_knowns('='.join(text.split('\n')[1:])))+'\n'
    print(pref)
    print(text)
    return newform(result, logbook, good_input, browser=browser, actualpref=pref)

@get('/cookie')
def cookie():
    mem = request.get_cookie("visited")
    if mem:
        mem = eval(mem)
        pref = mem.decode('utf-8')
    else:
        response.set_cookie("visited", "nothing yet")
        pref = "Hello there. Nice to meet you"
    return newform(('', '', '', '', ''), '', '', actualpref=pref, action='./cookie')

@post('/cookie')
def cookie_post():
    oldsymbols = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    if request.forms.get('sub') == "export":
        allsymbols = State(oldsymbols, False)
        return printableLog(allsymbols, logbook, inputlog)
    if request.forms.get('sub') == "help":
        return helpform(False)
    commands = request.forms.get('commands')
    result, good_input = calc(oldsymbols, commands, False)

    inputlog = inputlog + good_input
    enc = inputlog.encode('utf-8')
    enc = repr(enc[-3000:])
    response.set_cookie("visited", enc)
    if request.forms.get('sub') == " save ":
        with open('logfile.txt', 'a', encoding='utf-8') as logfile:
            print(inputlog, file = logfile)
            print(inputlog)
        return helpform(False)
    return newform(result, logbook, inputlog, action='./cookie')


hints = None

@get('/<hwid:re:hw.*>')
def hw(hwid):
    global hints
    hints = None
    question = get_example(hwid[2:])
    if not question:
        return "waah, does not exist"
    if '@@' in question:
        question, pref = question.split('@@', 1)
    else:
        pref = ''
    answer, followup = get_answer(hwid[2:])
    #rint('question', question)
    result, good_input = calc('', question)

    inputlog = good_input
    logbook = ''
    if hwid.endswith('b'):
        outp, logp, memory, known, linespace = result
        outp = '<span style="font-size: 12pt; color: maroon;">' + outp + '</span><br>'
        logp = '<span style="font-size: 12pt; color: maroon;">' + logp + '</span><br>'
        outp = outp.replace('color: navy', 'color: indigo')
        logp = logp.replace('color: navy', 'color: indigo')
        if followup:
            outp = outp + '<hr>' + '<span title="%s">Think about it...</span>' % followup.splitlines()[0].split('Think about it:')[1]
        result = outp, logp, memory, known, linespace
        return newform(result, logbook, inputlog,
                       action=hwid, button2='submit', otherbuttons=('export',), actualpref=pref)
    return newform(result, logbook, inputlog,
                   action=hwid, button2='', otherbuttons='', show_top=True)

import json
from html import escape, unescape


@post('/<hwid:re:hw.*>')
def hw_post(hwid):
    oldsymbols = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    oldstuff = len(inputlog.splitlines())
    hints = request.forms.get('hints')
    if hints:
        hints = json.loads(unescape(hints))
    print(oldstuff, inputlog)
    if request.forms.get('sub') == "export":
        allsymbols = State(oldsymbols)
        return printableLog(allsymbols, logbook, inputlog)
    commands = request.forms.get('commands')
    result, good_input, = calc(oldsymbols, commands)
    if commands:
        inputlog = inputlog + "\n" + good_input
    outp, logp, memory, known, linespace = result
    answer, followup = get_answer(hwid[2:])
    question = get_example(hwid[2:])
    student_answer = inputlog[:]
    for q in question.splitlines():
        student_answer = student_answer.replace(q+'\r\n', '')
    if request.forms.get('sub') == "submit":
        grade = grade_answer(student_answer, answer, question, hwid)
        if followup:
            fu = followup.splitlines()
            followup = fu[0] + '<ul  style="list-style-type:none"><li>' + '</li><br><li>'.join((f if f[1] != '*' else f[:1]+f[2:]) for f in fu[1:]) + '</li></ul>'
            result, good_input, = calc('', followup)
            outp, logp, memory, known, linespace = result
            return newform((grade+outp, logp, '', '', ''), logbook, inputlog, actualpref='The answer is: ', button2='extra credit?', action='yipee')
        return newform((grade, logp, '', '', ''), logbook, inputlog, otherbuttons=('export',))
    if not commands:
        if '__tutor__' in inputlog:
            outp = 'Tutor says: Please input commands. I will comment but give no hints'
        else:
            if not hints:
                print("Hints for:", hwid)
                print("Student answer:", student_answer)
                hints = generate_hints (hwid, student_answer, answer, question)
                for h in hints:
                    pass #rint(h)
                print('done with hints')
            outp = hints.pop(0)
            if not hints:
                hints = [outp]
            hints = json.dumps(hints)
        return newform((outp, '', memory, known, linespace), logbook, inputlog, action=hwid, button2='submit', otherbuttons=('export',), hints=hints)
    else:
        if '__tutor__' in inputlog and '__tutor__' not in commands:
            feedback = generate_tutor_comments (hwid, inputlog, oldstuff, answer, question)
            outp, logp, memory, known, linespace = result
            return newform((outp + feedback, logp, memory, known, linespace), logbook, inputlog, action=hwid, button2='submit',
                           otherbuttons=('export',))

    return newform(result, logbook, inputlog,
                   action=hwid, button2='submit', otherbuttons=('export',))

@get('/<nr:re:formulae.*>')
def formula(nr):
    response.set_header('X-XSS-Protection', '0')
    try:
        if '.' in nr:
            text = formula_details(*nr.split('formulae')[1].split('.'))
            result, good_input = calc('', text)
            outp, logp, memory, known, linespace = result
            result = outp, logp, memory, known, linespace
            return newform(result, '', '', action=None, button2='', otherbuttons='',
                           actualpref="\n\nClick on formulas to make commands appear here (and then copy into calculator)\n")
        else:
            text = show_formulae(int(nr.split('formulae')[1]))
    except ZeroDivisionError:
        text = 'No data'
    result, good_input = calc('', text)
    return newform(result, '', '', action=None, button2='', otherbuttons='', show_top=True,
                   actualpref="\n\nClick on formulas to make commands appear here (and then copy into calculator)\n")

@get('/<nr:re:units.*>')
def unit_table(nr):
    response.set_header('X-XSS-Protection', '0')
    try:
        text = show_quantities(int(nr.split('units')[1]), flashcard=True)
        s = State()
        for line in text.splitlines():
            if line.startswith('@'):
                create_comment(line, s)
            else:
                s.printnlog(line)
    except ValueError:
        result = ('No data',)
    result = '\n'.join(line.replace('<br>','') for line in s.output), '', '', '', ''
    return newform(result, '', '', action=None, button2='', otherbuttons='', show_top=True,
                   actualpref="Click on formulas to make commands appear here\n")



run(host='localhost', port=8080, debug=True)
#application = default_app()