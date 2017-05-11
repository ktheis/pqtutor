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
print('#'*30, 'calculator')
from comments import extract_knowns
from form import newform, printableLog, helpform, exdict
from mathparser import crashtest
print('#'*30, 'mathparser')
from database import get_example, get_answer
from matchup import checkanswer
from studygroup import pumpit, show_formulae, formula_details, show_quantities
print('#'*30, 'matchup')

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

@get('/icrash')
def crash_test():
    return crashtest()


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


@get('/<hwid:re:hw.*>')
def hw(hwid):
    question = get_example(hwid[2:])
    answer, followup = get_answer(hwid[2:])
    if not question:
        return "waah, does not exist"
    print('question', question)
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
                       action=hwid, button2='submit', otherbuttons=('export',))
    return newform(result, logbook, inputlog,
                   action=hwid, button2='', otherbuttons='', show_top=True)

@post('/<hwid:re:hw.*>')
def hw_post(hwid):
    browser = request.environ.get('HTTP_USER_AGENT').lower()
    oldsymbols = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    if request.forms.get('sub') == "export":
        allsymbols = State(oldsymbols)
        return printableLog(allsymbols, logbook, inputlog)
    commands = request.forms.get('commands')
    result, good_input, = calc(oldsymbols, commands)
    #return (verbose_work, brief_work, m, known, linespace), input_log
    inputlog = inputlog + "\n" + good_input
    outp, logp, memory, known, linespace = result
    if request.forms.get('sub') == "submit":
        answer, followup = get_answer(hwid[2:])
        grade = checkanswer(inputlog, answer)
        if followup:
            result, good_input, = calc('', followup)
            outp, logp, memory, known, linespace = result
            return newform((grade+outp, logp, '', '', ''), logbook, inputlog, actualpref='The answer is: ', button2='extra credit?')
        return newform((grade, logp, '', '', ''), logbook, inputlog, otherbuttons=('export',))
    if not commands:
        outp = pumpit(hwid, inputlog, oldsymbols)
        return newform((outp, '', memory, known, linespace), logbook, inputlog, action=hwid, button2='submit', otherbuttons=('export',))
    else:
        pumpit(0,0,0,reset=True)
    return newform(result, logbook, inputlog,
                   action=hwid, button2='submit', otherbuttons=('export',))

import re

@get('/<nr:re:formulae.*>')
def formula(nr):
    response.set_header('X-XSS-Protection', '0')
    try:
        if '.' in nr:
            text = formula_details(*nr.split('formulae')[1].split('.'))
            result, good_input = calc('', text)
            outp, logp, memory, known, linespace = result
            result = logp, logp, memory, known, linespace
            return newform(result, '', '', action=None, button2='', otherbuttons='',
                           actualpref="Can't calculate on this page (just paste into main calculation)\n")
        else:
            text = show_formulae(int(nr.split('formulae')[1]))
    except ValueError:
        text = 'No data'
    result, good_input = calc('', text)
    return newform(result, '', '', action=None, button2='', otherbuttons='', show_top=True,
                   actualpref="Can't calculate on this page (just paste into main calculation)\n")

@get('/<nr:re:units.*>')
def unit_table(nr):
    response.set_header('X-XSS-Protection', '0')
    try:
        text = show_quantities(int(nr.split('units')[1]))
        result, good_input = calc('', text)
    except ValueError:
        result = ('No data',)
    result = result[0].replace('<br>',''), '', '', '', ''
    return newform(result, '', '', action=None, button2='', otherbuttons='', show_top=True,
                   actualpref="Can't calculate on this page (just paste into main calculation)\n")

#run(host='localhost', port=8080, debug=True)
application = default_app()