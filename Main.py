from Resources import resources
import random
import re
import itertools


# Main Menu
def menu():
    menu_ = main_menu()

    if menu_ == 1:
        gamemode = gamemodes()

        if gamemode != 0:
            unit = units()
            (time, cycles) = duration()
            
            if gamemode == 1 or gamemode == 2:
                gamemode_translation((cycles if time == 1 else -time + 1), ([0,1] if gamemode == 1 else [1,0]), resources[unit])


    elif menu_ == 2:
        pass


    else:
        return
    

    menu()




def main_menu():
    print(
        '\n--- Main Menu ---\n'
        'Play (1)\n'
        'Settings (2)\n'
        'Exit (0)\n'
    )
    return try_input(0, 2)

def gamemodes():
    print(
        '\n--- Gamemodes ---\n'
        'Japanese to English (1)\n'
        'English to Japanese (2)\n'
        'Kanji Recognition (3)\n' 
        'Particles Practice (4)\n'
        'Counters Practice (5)\n'
        'Sentence Structure Practice (6)\n'
        # New Section, Verbs
        'あ/い/う/え/お Form Practice (7)\n'
        'Verb Conversion Practice (8)\n'
        'Return to Menu(0)\n'
    )
    return try_input(0, 8)

def units():
    print(
        '\n--- Units ---\n'
        'Book 1 Unit 1 Lesson 1 - 6 (1.1.1 - 1.1.6)\n'
        'Book 1 Unit 9 Lesson 1 - 5 (1.9.1 - 1.9.5)\n'
        'Book 1 Unit 10 Lesson 1 - 5 (1.10.1 - 1.10.5)\n'
        'Book 1 Unit 11 Lesson 2 - 4 (1.11.2 - 1.11.5)\n'
        'Book 1 Unit 12 Lesson 1 - 5 (1.12.1 - 1.12.5)\n'
        'Book 2 Unit 1 Lesson 1 - 4 (2.1.1 - 2.1.4)\n'
        'Book 2 Unit 1 Lesson 1 - 4 (2.2.1 - 2.2.4)\n'
        'Book 2 Unit 3 Lesson 1 - 4 (2.3.1 - 2.3.4)\n'
        'Book 1 Full Units 1 - 12 (1.1.0 - 1.12.0)\n'
        'Book 2 Full Units 1 - 3 (2.1.0 - 2.3.0)\n'
        'Return to Menu (0)\n'
    )
    while True:
        unit = input('Select Unit:\n')
        if unit == '0':
            gamemode = 0
            break
        if unit in resources:
            break 
    return unit

def duration():
    print(
        '\n--- Duration ---\n'
        'Cycles (1)\n'
        'Until 100% Correct (2)\n'
        'Endless (3)\n'
        'Return to Menu (0)\n'
    )
    time = try_input(0, 3)
    cycles = 0
    if time == 1:
        while not cycles > 0:
            try:
                cycles = int(input('Enter number of cycles: \n'))
            except:
                pass
    return (time, cycles)




def gamemode_translation(cycles, index, material):
    score = {'correct': 0, 'total': 0}
    loops = 0


    if cycles == -1:
        while True:
            loops += 1
            score = {'correct': 0, 'total': 0}
            game_questions(index, material, score)

            current_score = score['correct']/score['total'] if score['total'] > 0 else 0
            print(f'Score: {score['correct']}/{score['total']} ({(current_score)*100:.2f}%)\n')
            if current_score != 1:
                print(f'Cycle {loops} completed.\n')
            else:
                print('Practice completed.\n')
                break


    elif cycles == -2:
        while True:
            loops += 1
            game_questions(index, material, score)

            current_score = score['correct']/score['total'] if score['total'] > 0 else 0
            print(
                f'Score: {score['correct']}/{score['total']} ({(current_score)*100:.2f}%)'
                f'Loop {loops} completed.\n'
            )
        

    else:
        for i in range(cycles):
            game_questions(index, material, score)

            current_score = score['correct']/score['total'] if score['total'] > 0 else 0
            print(
                f'\nScore: {score['correct']}/{score['total']} ({(current_score)*100:.2f}%)'
                f'Cycle {i+1}/{cycles} completed.\n'
                )

def game_questions(index, material, score):
    random.shuffle(material)
    for value in material:
        
        if isinstance(value[index[0]], list):
            question = normalize_text(value[index[0]])
            random.shuffle(question)
        else:
            question = value[index[0]]

        language = ['English', 'Japanese']
        user_input = input(f'\nWhat is the {language[index[0]]} for "{question[0]}"?\n')
        answer = value[index[1]]


        if user_input == 'exit':
            print('Game exited.\n')
            return


        valid_answers = normalize_text(answer)

        if user_input.strip() in valid_answers:
            print('Correct!\n')
            score['correct'] += 1
        else:
            print("Incorrect.")


            if isinstance(answer, list):
                print(f'The correct answers are: {', '.join(answer)}\n')
            else:
                print(f'The correct answer is: {answer}\n')
            

            while user_input not in valid_answers:
                user_input = input('Type the correct answer to continue:\n')
                if user_input == 'exit':
                        print('Game exited.\n')
                        return


        score['total'] += 1
    return score




def expand_slashes(text):
    parts = text.split()

    options = []
    for part in parts:
        if "/" in part:
            options.append(part.split("/"))
        else:
            options.append([part])

    return [" ".join(combo) for combo in itertools.product(*options)]

def normalize_text(answer):
    if isinstance(answer, list):
        normalized = []
        for a in answer:
            normalized.extend(expand_optional(a))
        return list(set(normalized))  # remove duplicates
    else:
        return expand_optional(answer)

def expand_optional(answer_str):
    PAREN_OPEN = r"[（(]"
    PAREN_CLOSE = r"[）)]"
    results = set()

    # --- Japanese mandatory OR: X「A/B」C ---
    jp_quote_pattern = r'(.*?)「([^」]+/[^」]+)」(.+)'
    jp_match = re.search(jp_quote_pattern, answer_str)

    if jp_match:
        prefix = jp_match.group(1)
        choices = jp_match.group(2).split('/')
        suffix = jp_match.group(3)

        for c in choices:
            results.add(prefix + c + suffix)

        return list(results)

    # --- Optional parentheses OR: (A/B)C ---
    prefix_pattern = rf'{PAREN_OPEN}([^）)]+/[^）)]+){PAREN_CLOSE}(.+)'
    prefix_match = re.search(prefix_pattern, answer_str)

    if prefix_match:
        prefixes = prefix_match.group(1).split('/')
        suffix = prefix_match.group(2)

        for p in prefixes:
            results.add(p + suffix)

        # optional removal allowed
        results.add(suffix)

        return list(results)

    # --- Optional parentheses elsewhere ---
    full_version = re.sub(rf'{PAREN_OPEN}|{PAREN_CLOSE}', '', answer_str).strip()
    short_version = re.sub(rf'\s*{PAREN_OPEN}.*?{PAREN_CLOSE}\s*', '', answer_str).strip()

    base_versions = {full_version, short_version}

    # --- English word-level slash handling ---
    for version in base_versions:
        if '/' in version:
            results.update(expand_slashes(version))
        else:
            results.add(version)

    return list(results)




def try_input(min, max):
    var = -1
    while not min <= var <= max:
        try:
            var = int(input('Select Option: \n'))
        except:
            pass
    return var


menu()