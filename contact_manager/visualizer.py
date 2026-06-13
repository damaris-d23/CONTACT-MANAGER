import matplotlib.pyplot as plt


#deschide fereastra pentru afisarea arborelui red-black
def visualize_red_black_tree(tree):
    #nu afisez nimic daca arborele este gol
    if tree.root == tree.NIL:
        print("Red-Black Tree is empty.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Red-Black Tree - Contact Manager")
    ax.axis("off")

    positions = {}

    #calculez pozitia fiecarui nod
    _set_rbt_positions(tree, tree.root, 0, 0, 4, positions)

    #desenez arborele
    _draw_rbt(tree, tree.root, ax, positions)

    plt.show()


#stabilesc coordonatele nodurilor din arbore
def _set_rbt_positions(tree, node, x, y, gap, positions):
    if node == tree.NIL:
        return

    positions[node] = (x, y)

    #merg recursiv pe stanga si dreapta
    _set_rbt_positions(tree, node.left, x - gap, y - 1.5, gap / 2, positions)
    _set_rbt_positions(tree, node.right, x + gap, y - 1.5, gap / 2, positions)


#desenez arborele red-black
def _draw_rbt(tree, node, ax, positions):
    if node == tree.NIL:
        return

    x, y = positions[node]

    #desenez ramura din stanga
    if node.left != tree.NIL:
        child_x, child_y = positions[node.left]

        ax.plot([x, child_x], [y, child_y], color="gray")

        _draw_rbt(tree, node.left, ax, positions)

    #desenez ramura din dreapta
    if node.right != tree.NIL:
        child_x, child_y = positions[node.right]

        ax.plot([x, child_x], [y, child_y], color="gray")

        _draw_rbt(tree, node.right, ax, positions)

    #aleg culoarea nodului
    node_color = "red" if node.color == "RED" else "#222222"

    #desenez cercul nodului
    circle = plt.Circle((x, y), 0.35, color=node_color)
    ax.add_patch(circle)

    #afisez numele contactului in nod
    ax.text(
        x,
        y,
        node.contact.name,
        color="white",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

    ax.set_xlim(-6, 6)
    ax.set_ylim(-7, 1)


#deschide fereastra pentru afisarea trie-ului
def visualize_trie(trie):
    #nu afisez nimic daca trie-ul este gol
    if not trie.root.children:
        print("Trie is empty.")
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_title("Trie - Contact Name Autocomplete")
    ax.axis("off")

    positions = {}
    counter = [0]

    #calculez pozitia fiecarui nod
    _set_trie_positions(trie.root, 0, 0, positions, counter)

    #desenez trie-ul
    _draw_trie(trie.root, ax, positions, "ROOT")

    plt.show()


#stabilesc coordonatele nodurilor din trie
def _set_trie_positions(node, depth, y, positions, counter):
    current_x = counter[0]
    positions[node] = (current_x, -depth)

    #daca este frunza merg la urmatoarea pozitie
    if not node.children:
        counter[0] += 1
        return

    child_positions = []

    #procesez toti copiii nodului curent
    for char in sorted(node.children.keys()):
        child = node.children[char]

        _set_trie_positions(child, depth + 1, y, positions, counter)

        child_positions.append(positions[child][0])

    #pozitionez parintele intre copii
    if child_positions:
        avg_x = sum(child_positions) / len(child_positions)
        positions[node] = (avg_x, -depth)


#desenez trie-ul
def _draw_trie(node, ax, positions, label):
    x, y = positions[node]

    #desenez toate ramurile
    for char, child in sorted(node.children.items()):
        child_x, child_y = positions[child]

        ax.plot([x, child_x], [y, child_y], color="gray")

        _draw_trie(child, ax, positions, char)

    #aleg culoarea nodului
    if label == "ROOT":
        node_color = "#a378df"
        text = "ROOT"

    elif node.is_end:
        #verde pentru sfarsitul unui nume
        node_color = "#639265"
        text = label + "\n"

    else:
        node_color = "#dddddd"
        text = label

    #desenez cercul nodului
    circle = plt.Circle((x, y), 0.28, color=node_color)
    ax.add_patch(circle)

    text_color = "white" if label == "ROOT" or node.is_end else "black"

    #afisez litera din nod
    ax.text(
        x,
        y,
        text,
        color=text_color,
        ha="center",
        va="center",
        fontsize=8,
        fontweight="bold"
    )

    #stabilesc limitele ferestrei
    all_x = [pos[0] for pos in positions.values()]
    all_y = [pos[1] for pos in positions.values()]

    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, 1)