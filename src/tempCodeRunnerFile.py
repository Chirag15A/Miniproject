def add_content_from(listfrom, listto):
    content = []
    for i in listfrom:
        if type(i) == list:
            add_content_from(i, content)
        else:
            content.append(i)
    for i in content:
        listto.append(i)