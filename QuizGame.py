from IntelligentNPC import IntelligentNPC


class QuizMaster(IntelligentNPC):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def selectQuestion(self, questions):
        pass

    def askQuestion(self, question):
        pass

    def provide_feedback(self):
        pass

    def provide_hint(self):
        pass


class Question:
    def __init__(self, question_text, options, correct_option):
        self.question_text = question_text
        self.options = options
        self.correct_option = correct_option

    def display_question(self):
        print(self.question_text)
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")

    def is_correct(self, selected_option):
        return selected_option == self.correct_option


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class QuizGame:
    def __init__(self, quizMaster, questions, player):
        self.quizMaster = quizMaster
        self.questions = questions
        self.player = player

    def play_round(self):
        pass

    def play_game(self):
        print(self.quizMaster.talk(f"Greetings, My name is {self.quizMaster.name}."))


