#! /usr/bin/python
"""
Prints out all 
"""

import sys, re

def location(str, pos):
    """Given a string str and an integer pos, find the line number and character in that line that correspond to pos"""
    lineno, charpos = 1, 1
    counter = 0
    for char in str:
        if counter == pos:
            return lineno, charpos
        elif char == '\n':
            lineno += 1
            charpos = 1
            counter += 1
        else:
            charpos += 1
            counter += 1

    return lineno, charpos
        
# Things that are OK:
GOOD_STRINGS = re.compile(
    r"""
          # django comment
       ( {%\ comment\ %}.*?{%\ endcomment\ %}

         # already translated text
        |{%\ ?blocktrans.*?{%\ ?endblocktrans\ ?%}

         # any django template function (catches {% trans ..) aswell
        |{%.*?%}

         # JS 
        |<script.*?</script>

         # A html title or value attribute that's been translated
        |(?:value|title|summary|alt)="{%\ ?trans.*?%}"

         # A html title or value attribute that's just a template var
        |(?:value|title|summary|alt)="{{.*?}}"

         # An <option> value tag
        |<option[^<>]+?value="[^"]*?"

         # Any html attribute that's not value or title
        |[a-z:-]+?(?<!alt)(?<!value)(?<!title)(?<!summary)="[^"]*?"

         # HTML opening tag
        |<[\w:]+

         # End of a html opening tag
        |>
        |/>

         # closing html tag
        |</.*?>

         # any django template variable
        |{{.*?}}

         # HTML doctype
        |<!DOCTYPE.*?>

         # IE specific HTML
        |<!--\[if.*?<!\[endif\]-->

         # HTML comment
        |<!--.*?-->

         # HTML entities
        |&[a-z]{1,10};

         # CSS style
        |<style.*?</style>

         # another common template comment
        |{\#.*?\#}
        )""",

    # MULTILINE to match across lines and DOTALL to make . include the newline
    re.MULTILINE|re.DOTALL|re.VERBOSE) 

# Stops us matching non-letter parts, e.g. just hypens, full stops etc.
LETTERS = re.compile("\w")

def non_translated_text(filename):

    template = open(filename).read()
    offset = 0

    # Find the parts of the template that don't match this regex
    # taken from http://www.technomancy.org/python/strings-that-dont-match-regex/
    for index, match in enumerate(GOOD_STRINGS.split(template)):
        if index % 2 == 0:

            # Ignore it if it doesn't have letters
            if LETTERS.search(match):
                lineno, charpos = location(template, offset)
                yield (lineno, charpos, match.replace("\n", "").replace("\r", "")[:120])
            

        offset += len(match)

if __name__ == '__main__':
    filename = sys.argv[1]
    full_text_lines = open(filename, 'r').readlines()
    for lineno, charpos, message in non_translated_text(filename):
        change = raw_input("Make '%s' translatable? [y/n] " % message)
        if change == 'y':
			real_lineno = lineno - 1
			left_part = full_text_lines[real_lineno][0 : charpos - 1]
			right_part = full_text_lines[real_lineno][charpos + len(message) - 1:]
			full_text_lines[lineno - 1] = left_part + ('{%% trans "%s" %%}' % message) + right_part
			
    full_text = "".join(full_text_lines)
    save_filename = filename.split(".")[0] + "_translated.html"
    open(save_filename, 'w').write(full_text)
    print "Fully translated! Saved as: %s" % save_filename
