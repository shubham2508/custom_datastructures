'''
USEFUL LINKS:
https://medium.com/100-days-of-algorithms/day-34-aho-corasick-4b9f439d4712
https://www.toptal.com/algorithms/aho-corasick-algorithm
'''
from collections import deque, defaultdict
import logging

class AhoCorasickNode:

    def __init__(self, state, character, suffixNode):

        self.state = state
        #state is unique across state machine i.e. its a key

        #alphabet/key
        self.char = character

        self.children = {}
        #this is goto state will hold value as "character: AhoCorasickNode Node"

        self.suffixLink = suffixNode
        #this is fail state i.e. suffix which is a prefix by default it is root Node

        self.isWord = False
        #property of Trie to denote whether it's a word

    def add_child(self, ch, ch_val):
        self.children[ch] = ch_val

    def set_suffix_link(self, suffixLink):
        self.suffixLink = suffixLink

    def set_word_flag(self):
        self.isWord = True

    def is_word(self):
        return self.isWord

class AhoCorasick:

    def __init__(self):

        self.root = AhoCorasickNode(0, None, None)
        self.root.set_suffix_link(self.root)
        self.available_state = 1
        self.output = defaultdict(set)

    def increment_available_state(self):
        self.available_state += 1

    def get_count_of_words(self):
        return self.available_state - 1

    def add_word(self, word):

        logging.debug(f'Add word : {word}')
        node = self.root

        for ch in word:

            if ch in node.children:
                node = node.children[ch]
            else:
                child = AhoCorasickNode(self.available_state, ch, self.root)
                node.add_child(ch, child)
                self.increment_available_state()
                node = child

        node.set_word_flag()
        self.output[node.state].add((word, len(word)))

    def build_aho_corasick_tree(self):

        queue = deque(child_node for ch, child_node in self.root.children.items())

        
        while queue:

            node = queue.popleft()

            for ch,  child_node in node.children.items():
                suffixNode = node.suffixLink

                #set suffix Link for child_node
                while suffixNode != self.root and ch not in suffixNode.children:
                    suffixNode = suffixNode.suffixLink

                suffixNode = suffixNode.children[ch] if ch in suffixNode.children else self.root
                child_node.set_suffix_link(suffixNode)

                self.output[child_node.state].update(self.output[suffixNode.state])
                queue.append(child_node)


    def search_words(self, text):

        node = self.root
        answer = set()

        for i, ch in enumerate(text):

            while node != self.root and ch not in node.children:
                node = node.suffixLink

            node = node.children[ch] if ch in node.children else self.root
            if self.output[node.state]:
                logging.info(f'Ending at {i} words are {self.output[node.state]}')
                answer.update(self.output[node.state])

        return answer

if __name__== "__main__":
    AC = AhoCorasick()
    AC.add_word('bar')
    AC.add_word('ara')
    AC.add_word('bara')
    AC.add_word('barbara')
    AC.build_aho_corasick_tree()

    text = 'barbarian barbara said: barabum'
    logging.info(f'text: {text}')
    AC.search_words(text)





















