from red_black_tree import RedBlackTree, Contact
from trie import Trie
from visualizer import visualize_red_black_tree, visualize_trie


#gestioneaza toate operatiile aplicatiei
class ContactManager:
    def __init__(self):
        #creez cele doua structuri folosite in proiect
        self.rbt = RedBlackTree()
        self.trie = Trie()

    def add_contact(self):
        #citesc datele noului contact
        name = input("Name: ").strip().title()
        phone = input("Phone: ").strip()

        #verific daca utilizatorul a introdus date
        if name == "" or phone == "":
            print("Name and phone cannot be empty.")
            return

        #creez obiectul contact
        contact = Contact(name, phone)

        #adaug contactul in arbore
        inserted = self.rbt.insert(contact)

        if inserted:
            #adaug numele si in trie pentru autocomplete
            self.trie.insert(name)

            print("Contact added successfully.")

    def delete_contact(self):
        #citesc numele contactului care trebuie sters
        name = input("Name to delete: ").strip().title()

        deleted = self.rbt.delete(name)

        if deleted:
            #sterg si din trie
            self.trie.delete(name)

            print("Contact deleted successfully.")

    def search_contact(self):
        #citesc numele cautat
        name = input("Name to search: ").strip().title()

        #caut in arbore
        node = self.rbt.search(name)

        if node:
            print(f"Found contact: {node.contact.name} - {node.contact.phone}")
        else:
            print("Contact not found.")

    def display_contacts(self):
        #afisez toate contactele sortate
        print("\nAll contacts sorted alphabetically:")

        self.rbt.display()

    def autocomplete_contact(self):
        #citesc prefixul introdus
        prefix = input("Enter prefix: ").strip()

        #caut sugestii in trie
        suggestions = self.trie.autocomplete(prefix)

        if suggestions:
            print("\nSuggestions:")

            for name in suggestions:
                print(f"- {name}")
        else:
            print("No contacts found with this prefix.")

    def visualize_rbt(self):
        #afisez arborele red-black
        visualize_red_black_tree(self.rbt)

    def visualize_trie(self):
        #afisez trie-ul
        visualize_trie(self.trie)


#afiseaza meniul principal
def print_menu():
    print("\n===== SMART CONTACT MANAGER =====")
    print("1. Adauga contact")
    print("2. Sterge contact")
    print("3. Cauta contact")
    print("4. Afiseaza toate contactele")
    print("5. Autocomplare contacte dupa nume")
    print("6. Vizualizare Red-Black Tree")
    print("7. Vizualizare Trie")
    print("0. Iesire")


def main():
    #creez managerul aplicatiei
    manager = ContactManager()

    #meniul ruleaza pana cand utilizatorul inchide programul
    while True:
        print_menu()

        choice = input("Choose option: ").strip()

        if choice == "1":
            manager.add_contact()

        elif choice == "2":
            manager.delete_contact()

        elif choice == "3":
            manager.search_contact()

        elif choice == "4":
            manager.display_contacts()

        elif choice == "5":
            manager.autocomplete_contact()

        elif choice == "6":
            manager.visualize_rbt()

        elif choice == "7":
            manager.visualize_trie()

        elif choice == "0":
            print("Program closed.")
            break

        else:
            print("Invalid option. Try again.")


#punctul de pornire al programului
if __name__ == "__main__":
    main()