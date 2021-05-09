def quote_list(items):
    output_items = [str(x) for x in items]
    return "> {items}".format(items ="\n> ".join(output_items))

def mark_down_link(title, url):
    return "[{title}](url)".format(title=title, url=url)