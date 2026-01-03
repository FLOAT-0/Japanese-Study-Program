from Main import normalize_text
import random

def gamemode_translation(cycles, index, material):
    score = {'correct': 0, 'total': 0}
    loops = 0


    if cycles == -1:
        while True:
            loops += 1
            score = {'correct': 0, 'total': 0}
            game_translation_questions(index, material, score)

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
            game_translation_questions(index, material, score)

            current_score = score['correct']/score['total'] if score['total'] > 0 else 0
            print(
                f'Score: {score['correct']}/{score['total']} ({(current_score)*100:.2f}%)'
                f'Loop {loops} completed.\n'
            )
        

    else:
        for i in range(cycles):
            game_translation_questions(index, material, score)

            current_score = score['correct']/score['total'] if score['total'] > 0 else 0
            print(
                f'\nScore: {score['correct']}/{score['total']} ({(current_score)*100:.2f}%)'
                f'Cycle {i+1}/{cycles} completed.\n'
                )

def game_translation_questions(index, material, score):
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
