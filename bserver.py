# coding=utf-8

from bottle import get, post, run, request, response, static_file, default_app

"""
Module to tie the quantities, calculator, and form modules together into an online calculator.

The calculator is hosted on ktheis.pythonanywhere.com, but you could have a local server or run it
on other platforms. In the calculator, you define values of named physical quantities,
and then do arithmetic with them. The web server is implemented using web.py.

"""
from calculator import calc, State, markup_comments
from form import newform, printableLog, helpform


@get('/')
def index_get():
    known = [" -- nothing yet -- "]
    browser = request.environ.get('HTTP_USER_AGENT')
    mobile = ("ipad" in browser or "iphone" in browser or "ipod" in browser)
    if "ipod" in browser or "iphone" in browser or "android" in browser:
        mobile = "ipod"
    return newform("", "", "", known, "", mobile, False, "")


@post('/')
def index_post():
    # response.set_header('Content-Type', 'text/html; charset=utf-8')
    # response.set_header('X-XSS-Protection', '0')
    browser = request.environ.get('HTTP_USER_AGENT').lower()
    mobile = ("ipad" in browser or "iphone" in browser or "nexus" in browser)
    if "ipod" in browser or "iphone" in browser or "android" in browser:
        mobile = "ipod"
    try:
        if request.forms.get('sub') == "reset":
            return newform("", "", "", "", "", mobile, False, "")
    except:
        return newform("", "", "", "", "", mobile, False, "")
    oldsymbols = request.forms.get('memory')
    logbook = request.forms.get('logbook')
    inputlog = request.forms.get('inputlog')
    if request.forms.get('sub') == "export":
        allsymbols = State(oldsymbols, mobile)
        return printableLog(allsymbols, logbook, inputlog)
    if request.forms.get('sub') == "help":
        return helpform(mobile)
    commands = request.forms.get('commands')
    outp, logp, mem, known, oneline, good_input, linespace = calc(oldsymbols, commands, mobile)
    inputlog = inputlog + "\n" + good_input
    return newform(outp, logp, mem, known, logbook, mobile, oneline, inputlog, linespace=linespace)


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
    mobile = ("ipad" in browser or "iphone" in browser or "nexus" in browser)
    if "ipod" in browser or "iphone" in browser:
        mobile = "ipod"
    return newform("", "", "", known, "", mobile, False, "", prefill=prefill)

application = default_app()