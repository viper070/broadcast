def splited(text: str):
    
    splited = []

    if len(text.splitlines()) == 1:
        sp = text.splitlines()
        if len(sp[0].split('|')) == 1:
            sp = sp[0].split('|')
            if len(sp[0].split('-')) == 1:
                return []
            else:
                sp = sp[0].split('-')
                for i in sp:
                    if i == '':
                        return []
                splited.append(sp)
        else:
            sp = sp[0].split('|')
            list = []
            for i in sp:
                if i == '':
                    return []
                sp = i.split('-')
                for i in sp:
                    if i == '':
                        return []
                list.append(sp)
            splited.append(list)
    else:
        sp = text.splitlines()
        for i in sp:
            sp = i.split('|')
            line_list = []
            if len(sp) == 1:
                if len(sp[0].split('-')) == 1:
                    return []
                else:
                    sp = sp[0].split('-')
                    for i in sp:
                        if i == '':
                            return []
                    line_list.append(sp)
            else:
                for i in sp:
                    if i == '':
                        return []
                    sp = i.split('-')
                    for i in sp:
                        if i == '':
                            return []
                    line_list.append(sp)
            splited.append(line_list)
    return splited
split = splited('s-s\na-a|a-a\nb-b')
print(split)
# print('s-s|'.split('|'))
