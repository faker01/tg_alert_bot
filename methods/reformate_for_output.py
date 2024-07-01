

def reformat(text):
    print(text)
    out = ''
    for i in text:
        i = [str(j) for j in list(i)]
        out = out + " ".join(i) + '\n'
    return out


def calendar(text, user_intrests, categories):
    user_intrests = list(list(user_intrests[0])[1])
    user_intrests = [categories[int(_)] for _ in user_intrests]
    if text[1] in user_intrests:
        out = f'{text[3]}: {text[2]}'
    else:
        out = False
    return out


def create_info(text, user, categories):
    user = list(user[0])[1]
    user = [categories[int(_)] for _ in user]
    if text[1] in user:
        out = f"{text[0]}. название: {text[2]}\nдата: {text[3]}\nкатегория: {text[1]}\nКраткое описание:\n{text[4]}"
    else:
        out = False
    return out
