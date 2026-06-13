#Trie-folosit pentru cautare dupa prefix
#ma ajuta sa fac autocomplete la numele contactelor

#un nod din trie
class TrieNode:
    
    def __init__(self):
        self.children = {}    # copiii nodului curent
        self.is_end = False   # marcheaza sfarsitul unui nume
        self.end_count = 0    # folosit pentru inserari repetate


class Trie:
    #trie in care salvez numele contactelor
    def __init__(self):
        self.root = TrieNode()

    #inserare: 

    def insert(self, word):
        #adaug un nume in trie
        word_lower = word.lower()
        node = self.root

        #merg litera cu litera prin nume
        for char in word_lower:
            #creez nod nou daca nu exista deja
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        #nu adaug acelasi nume de doua ori
        if node.is_end:
            return False

        node.is_end = True
        node.end_count += 1
        return True

    #cautare:

    def search(self, word):
        #caut un nume exact
        word_lower = word.lower()
        node = self.root

        #verific fiecare litera
        for char in word_lower:
            #daca lipseste o litera, numele nu exista
            if char not in node.children:
                return False

            node = node.children[char]

        #verific daca am ajuns la un nume complet
        return node.is_end

    #prefix 

    def starts_with(self, prefix):
        #verific daca exista nume care incep cu prefixul dat
        prefix_lower = prefix.lower()
        node = self.root

        for char in prefix_lower:
            if char not in node.children:
                return False

            node = node.children[char]

        #toate literele prefixului exista
        return True

    #stergere:

    def delete(self, word):
        #sterg un nume din trie
        #elimin si nodurile care nu mai sunt folosite
        word_lower = word.lower()

        if not self.search(word_lower):
            print(f"  [!] Name '{word}' not found in Trie.")
            return False

        self._delete_helper(self.root, word_lower, 0)
        return True

    def _delete_helper(self, node, word, depth):
        #functie folosita pentru stergere recursiva

        #am ajuns la finalul numelui
        if depth == len(word):
            node.is_end = False
            node.end_count = 0

            #pot sterge nodul daca nu mai are copii
            return len(node.children) == 0

        char = word[depth]

        #numele nu exista
        if char not in node.children:
            return False

        should_delete_child = self._delete_helper(
            node.children[char],
            word,
            depth + 1
        )

        if should_delete_child:
            #sterg legatura catre copil
            del node.children[char]

            #verific daca si nodul curent poate fi sters
            return len(node.children) == 0 and not node.is_end

        return False

    #autocomplete:

    def autocomplete(self, prefix):
        #returneaza toate numele care incep cu prefixul dat
        prefix_lower = prefix.lower()
        node = self.root

        #merg pana la ultimul caracter din prefix
        for char in prefix_lower:
            #nu exista contacte cu acest prefix
            if char not in node.children:
                return []

            node = node.children[char]

        results = []

        #adun toate numele care pornesc cu prefixul dat
        self._collect_words(node, prefix_lower, results)

        #sortez rezultatele pentru afisare
        return sorted(name.capitalize() for name in results)

    def _collect_words(self, node, current_prefix, results):
        #parcurg toate ramurile si adun numele complete

        if node.is_end:
            results.append(current_prefix)

        for char, child in node.children.items():
            self._collect_words(
                child,
                current_prefix + char,
                results
            )

    #afisare:

    def get_all_words(self):
        #returneaza toate numele din trie
        results = []
        self._collect_words(self.root, "", results)

        return sorted(name.capitalize() for name in results)

    def display(self):
        #afiseaza toate numele din trie
        words = self.get_all_words()

        if not words:
            print("  (Trie is empty)")
            return

        print("  Names in Trie:")

        for word in words:
            print(f"    - {word}")