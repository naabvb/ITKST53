import lxml.html
import lxml.html.clean
import slimit.ast
import slimit.parser
import lab6visitor

from debug import *

libcode = '''
<script>
    var sandbox_document = {
        getElementById: function(id) {
            var e = document.getElementById('sandbox-' + id);
            return {
                get onclick() { return e.onclick; },
                set onclick(h) { e.onclick = h; },
                get textContent() { return e.textContent; },
                set textContent(h) { e.textContent = h; },
            }
        },
    };

    function sandbox_setTimeout(f, time_in_ms) {
        // Only allow function-type parameters to avoid eval() with string params
        if (typeof f === 'function' ) { 
            setTimeout(f, time_in_ms);
        }
        return null;
    }

    function check_dangerous_words(x) {
        dangerous_words = ['__proto__', 'constructor', '__defineGetter__', '__defineSetter__'];

        for (i = 0; i < dangerous_words.length; i++) {
            if (x.toString() === dangerous_words[i]) return '__invalid__';
        }
        return x;
    }

    function check_brackets(x) {
        // Test for custom toString or valueOf functions
        if (isFunctionNative(x.toString) === false || isFunctionNative(x.valueOf) === false) return '__invalid__';
        // Also test for dangerous words
        return check_dangerous_words(x);
    }

    function check_functions(f) {
        // Check for eval() functions (defeats test-13)
        if (isFunctionNative(f) === true && f.name == 'eval') return '__invalid__';
        return f;
    }

    // https://stackoverflow.com/a/42595031
    // Tests if a function is native to browser (eg. if toString() is customized)
    // Doesn't work against apply() or bind() but that is not required for this lab 
    function isFunctionNative(f) {
        return (/\{\s*\[native code\]\s*\}/).test(f);
    }

    function this_check(x) {
        if (x === window) return null;
        return x;
    }

    // Do not change these functions.
    function sandbox_grader(url) {
        window.location = url;
    }
    function sandbox_grader2() {
        eval("1 + 1".toString());  // What could possibly go wrong...
    }
    function sandbox_grader3() {
        try {
            eval(its_okay_no_one_will_ever_define_this_variable);
        } catch (e) {
        }
    }
</script>
'''

def filter_html_cb(s, jsrewrite):
    cleaner = lxml.html.clean.Cleaner()
    cleaner.scripts = False
    cleaner.style = True
    doc = lxml.html.fromstring(s)
    clean = cleaner.clean_html(doc)
    for el in clean.iter():
        if el.tag == 'script':
            el.text = jsrewrite(el.text)
            for a in el.attrib:
                del el.attrib[a]
        if 'id' in el.attrib:
            el.attrib['id'] = 'sandbox-' + el.attrib['id']
    return lxml.html.tostring(clean)

@catch_err
def filter_js(s):
    parser = slimit.parser.Parser()
    tree = parser.parse(s)
    visitor = lab6visitor.LabVisitor()
    return visitor.visit(tree)

@catch_err
def filter_html(s):
    return libcode + filter_html_cb(s, filter_js)

