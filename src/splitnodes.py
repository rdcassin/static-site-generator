from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes = node
        else:
            new_nodes = create_new_nodes(node.text, delimiter, text_type)
        new_nodes_list.append(new_nodes)
    if len(old_nodes) == 1:
        return new_nodes_list[0]
    return new_nodes_list

def create_new_nodes(node_text, delimiter, text_type):
    open_delim = False
    delim_counter = 0
    new_nodes = []
    current_value = ""

    for i in range(0,len(node_text)):
        if node_text[i] == delimiter:
            delim_counter += 1
            if len(current_value) > 0:
                new_node = create_new_node(open_delim, current_value, text_type)
                new_nodes.append(new_node)
                current_value = ""
            open_delim = not open_delim
        else:
            current_value += node_text[i]
            if i == len(node_text) - 1:
                new_node = create_new_node(open_delim, current_value, text_type)
                new_nodes.append(new_node)
                current_value = ""
    
    if delim_counter % 2 == 0:
        return new_nodes
    raise Exception("invalid Markdown syntax")

def create_new_node(open_delim, current_value, text_type):
    if open_delim:
        return TextNode(current_value, text_type)
    else:
        return TextNode(current_value, TextType.TEXT)