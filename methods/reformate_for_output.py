

def reformat(text):
    print(text)
    out = ''
    for i in text:
        i = [str(j) for j in list(i)]
        out = out + " ".join(i) + '\n'
    return out


def calendar(text):
    out = []
    for i in text:
        i = [str(j) for j in list(i)]
        out.append([i[3], i[2]])
    out.sort(key=lambda x: x[0])
    for i in range(1, len(out)):
        if out[i][0] == out[i - 1][0]:
            out[i] = ["   ", out[i][1]]
    out = [" ".join(i) for i in out]
    out = "\n".join(out)
    print(out)
    return out


def create_info(text):

    out = f"{text[0]}. название: {text[2]}\nдата: {text[3]}\nкатегория: {text[1]}\nКраткое описание:\n{text[4]}"
    return out
