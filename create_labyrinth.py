def mirror(s):
    return s[0:len(s)-1] + s[::-1]


def create_labyrinth(text, remainder):
    width = remainder * 2 + 1           # width of a row
    mirrored_text = mirror(text[::-1])  # note reverse text first!
    start = len(mirrored_text) // 2 + 1 # get middle of text 
    rows = len(text) - width // 2       # get # of rows
    offset = width // 2 + 1             # how much offset
    result = []
    for i in range(0, rows):
        x = mirrored_text[start - offset - i : start - i]
        result.append(mirror(x))
    return result

text = 'FLORENTIUMINDIGNUMMEMORARE'

print("\n".join(create_labyrinth(text, 13)))
