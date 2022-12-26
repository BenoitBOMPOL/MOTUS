#!/usr/bin/env python3
"""
    Générateur de MOTUS
"""
import random as rd

def create_dict(filename):
    """
        Liste les mots du dictionnaire
    """
    words = []
    with open(filename, "r", encoding="utf-8") as file:
        words = [word[:-1] for word in file.readlines()]
    sorted_words = {}
    for word in words:
        if len(word) in sorted_words:
            sorted_words[len(word)].add(word)
        else:
            sorted_words[len(word)] = {word}
    return sorted_words

def choose_word(allowed_words, size):
    """
        Choisit un mot aléatoirement
    """
    return rd.choice(list(allowed_words[size]))

def set_counter(word):
    """
        Compte la présence de chaque lettre
    """
    counter = {}
    for letter in word:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter

def get_feedback(secret, guess):
    """
        Renvoie le feedback pour un mot donné
    """
    corr = [None for _ in range(len(secret))]
    misp = [None for _ in range(len(secret))]
    inex = [None for _ in range(len(secret))]

    s_count = set_counter(secret)
    g_count = set_counter(guess)
    
    for ind, letter in enumerate(guess):
        if letter not in secret:
            # 1er cas : La lettre n'est pas présente. du tout
            corr[ind] = 0
            misp[ind] = 0
            inex[ind] = 1
            if letter in g_count:
                g_count.pop(letter)
    for ind, letter in enumerate(guess):
        if letter == secret[ind]:
            # 2è cas : La lettre est bien placée
            corr[ind] = 1
            misp[ind] = 0
            inex[ind] = 0
            s_count[letter] -= 1
            g_count[letter] -= 1
            if s_count[letter] == 0:
                s_count.pop(letter)
            if g_count[letter] == 0:
                g_count.pop(letter)
    for ind in range(len(guess)):
        if corr[ind] is None:
            corr[ind] = 0
    for ind, letter in enumerate(guess):
        if letter in g_count:
            if (letter != secret[ind]) and (letter not in s_count):
                misp[ind] = 0
                inex[ind] = 1
            elif letter == secret[ind]:
                misp[ind] = 0
                inex[ind] = 0
            else:
                misp[ind] = 1
                inex[ind] = 0
    return (corr, misp, inex)

def show_feedback(feedback, word):
    """
        Montre le feedback
    """
    available_feedback = ['🟩', '🟨', '⬛']
    string_builder = ""
    for ind in range(len(feedback[0])):
        for aux in range(3):
            if feedback[aux][ind] == 1:
                string_builder += available_feedback[aux]
    print(f"{string_builder} {word}")

def show_ansi_feedback(feedback, word):
    """
        Montre le feedback d'une autre manière
    """
    green = "\u001b[42;1m"
    yellow = "\u001b[43;1m"
    black = "\u001b[40;1m"

    available_feedback = [green, yellow, black]
    reset = "\u001b[0m"
    string_builder = ""
    for ind in range(len(feedback[0])):
        for aux in range(3):
            if feedback[aux][ind] == 1:
                string_builder = string_builder + f"{available_feedback[aux]} {word[ind]} {reset}"
    print(string_builder)

def get_possible_from_feedback(all_words, previous_guess, feedback):
    # Approche naïve : on ne compte que les cases vertes dans un premier temps
    word_length = len(feedback[0])
    correct_word_length = all_words[word_length]
    possible = []
    for word in correct_word_length:
        plausible = True
        # On enlève les mots qui "perdraient" des cases vertes
        for ind, value in enumerate(feedback[0]):
            letter = previous_guess[ind]
            if value and (letter != word[ind]):
                plausible = False
        # On enlève les mots qui ne contiennent pas les lettres jaunes
        for ind, value in enumerate(feedback[1]):
            letter = previous_guess[ind]
            if value and (letter not in word):
                plausible = False
        # On enlève les mots pour lesquels les lettres qui ne sont jamais apparues
        max_ceuxla = [previous_guess[ind] for ind in range(len(previous_guess)) if feedback[2][ind]]
        moin_ceula = [previous_guess[ind] for ind in range(len(previous_guess)) if feedback[0][ind]]
        a_verifier = [x for x in max_ceuxla if x not in moin_ceula]
        for char in a_verifier:
            if char in word:
                plausible = False

        
        if plausible:
            possible.append(word)
    return possible

def process(all_words, secret_word):
    count_guesses = 0
    guess = rd.choice(list(all_words[len(secret_word)]))
    first_guess = True
    possible_words = []
    while True:
        if first_guess:
            first_guess = False
        else:
            if guess in possible_words:
                possible_words.remove(guess)
            guess = rd.choice(list(possible_words))
        feedback = get_feedback(secret_word, guess)
        show_ansi_feedback(feedback, guess)
        possible_words = get_possible_from_feedback(all_words, guess, feedback)
        if guess == secret_word:
            return count_guesses
        count_guesses += 1

def main():
    """
        Main
    """
    all_words = create_dict("ods8.txt")
    secret_word_length = 14
    for secret_word in all_words[secret_word_length]:
        print(f"{secret_word} : {process(all_words, secret_word)}")

if __name__ == "__main__":
    main()