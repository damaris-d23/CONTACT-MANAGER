#arbore red-black folosit pentru stocarea contactelor
#contactele sunt pastrate in ordine alfabetica dupa nume

RED = "RED"
BLACK = "BLACK"


class Contact:
    #retine datele unui contact
    def __init__(self, name, phone):
        self.name = name      
        #dupa nume fac comparatiile in arbore
        self.phone = phone

    def __str__(self):
        return f"{self.name} | {self.phone}"

#un nod din arbore
class RedBlackNode:
  
    def __init__(self, contact, color=RED):
        self.contact = contact
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        #nod special folosit in loc de None
        #apare la toate frunzele arborelui
        self.NIL = RedBlackNode(contact=None, color=BLACK)
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL

        #la inceput arborele este gol
        self.root = self.NIL

    #rotatii:

    #rotatie la stanga in jurul nodului x
    def left_rotate(self, x):
        
        y = x.right
        x.right = y.left

        #mut subarborele lui y la x
        if y.left != self.NIL:
            y.left.parent = x

        #y ia locul lui x
        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        #x devine copilul stang al lui y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        #rotatie la dreapta in jurul nodului y
        x = y.left
        y.left = x.right

        # ut subarborele lui x la y
        if x.right != self.NIL:
            x.right.parent = y

        #x ia locul lui y
        x.parent = y.parent

        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        #y devine copilul drept al lui x
        x.right = y
        y.parent = x

    #inseare:

    def insert(self, contact):
        #creez nodul nou si il colorez initial rosu
        new_node = RedBlackNode(contact)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.color = RED

        parent = self.NIL
        current = self.root

        #caut pozitia unde trebuie adaugat noul contact
        while current != self.NIL:
            parent = current

            #compar numele fara sa tin cont de litere mari/mici
            if contact.name.lower() < current.contact.name.lower():
                current = current.left
            elif contact.name.lower() > current.contact.name.lower():
                current = current.right
            else:
                #nu permit doua contacte cu acelasi nume
                print(f"  [!] Contact '{contact.name}' already exists.")
                return False

        new_node.parent = parent

        #daca arborele era gol, nodul nou devine radacina
        if parent == self.NIL:
            self.root = new_node
        elif contact.name.lower() < parent.contact.name.lower():
            parent.left = new_node
        else:
            parent.right = new_node

        #reechilibrez arborele daca este nevoie
        self.insert_fixup(new_node)
        return True

    def insert_fixup(self, z):
        #repar arborele dupa inserare
        #problema apare cand parintele nodului nou este rosu
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right

                if uncle.color == RED:
                    #cazul 1 recolorez parintele, unchiul si bunicul
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        #cazul 2 fac rotatie la stanga
                        z = z.parent
                        self.left_rotate(z)

                    #cazul 3 recolorez si fac rotatie la dreapta
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                #aceleasi cazuri, dar invers
                uncle = z.parent.parent.left

                if uncle.color == RED:
                    #cazul 1 recolorez
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        #cazul 2 fac rotatie la dreapta
                        z = z.parent
                        self.right_rotate(z)

                    #cazul 3 recolorez si fac rotatie la stanga
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)

        #radacina trebuie sa fie mereu neagra
        self.root.color = BLACK

    #cautare:

    def search(self, name):
        #caut un contact dupa nume
        current = self.root

        while current != self.NIL:
            if name.lower() == current.contact.name.lower():
                return current
            elif name.lower() < current.contact.name.lower():
                current = current.left
            else:
                current = current.right

        return None

#stergere:

    def minimum(self, node):
        #gasesc cel mai mic nod dintr-un subarbore
        while node.left != self.NIL:
            node = node.left
        return node

    def transplant(self, u, v):
        #inlocuiesc subarborele u cu subarborele v
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def delete(self, name):
        #sterg contactul cu numele dat
        node = self.search(name)

        if node is None:
            print(f"  [!] Contact '{name}' not found.")
            return False

        self._delete_node(node)
        return True

    def _delete_node(self, z):
        #sterg efectiv nodul gasit
        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            #cazul 1 nodul nu are copil stang
            x = z.right
            self.transplant(z, z.right)

        elif z.right == self.NIL:
            #cazul 2 nodul nu are copil drept
            x = z.left
            self.transplant(z, z.left)

        else:
            #cazul 3 nodul are doi copii
            #caut succesorul lui
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        #daca am sters un nod negru, trebuie reparat arborele
        if y_original_color == BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x):
        #repar arborele dupa stergerea unui nod negru
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right

                if w.color == RED:
                    #cazul 1 fratele este rosu
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    #cazul 2 copiii fratelui sunt negri
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        #cazul 3 copilul drept al fratelui este negru
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right

                    #cazul 4 recolorez si rotesc
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                #aceleasi cazuri, dar in oglinda
                w = x.parent.left

                if w.color == RED:
                    #cazul 1 fratele este rosu
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    #cazul 2 copiii fratelui sunt negri
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        #cazul 3 copilul stang al fratelui este negru
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left

                    #cazul 4 recolorez si rotesc
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root

        #la final nodul curent trebuie sa fie negru
        x.color = BLACK

    #parcurgere si afisare:

    def inorder_traversal(self, node, result):
        #parcurgere inordine: stanga, nod, dreapta
        #asa obtin contactele in ordine alfabetica
        if node != self.NIL:
            self.inorder_traversal(node.left, result)
            result.append(node.contact)
            self.inorder_traversal(node.right, result)

    def get_all_contacts(self):
        #returnez toate contactele sortate
        contacts = []
        self.inorder_traversal(self.root, contacts)
        return contacts

    def display(self):
        #afisez contactele intr-un tabel simplu
        contacts = self.get_all_contacts()

        if not contacts:
            print("  (no contacts in the tree)")
            return

        print(f"  {'Name':<20} {'Phone':<15}")
        print(f"  {'-' * 20} {'-' * 15}")

        for c in contacts:
            print(f"  {c.name:<20} {c.phone:<15}")