from IntelligentNPC import IntelligentNPC
import re


class QuizMaster(IntelligentNPC):
    def __init__(self, name, questions_path,
                 conversation_template_str,
                 intent_model_path,
                 intent_tokenizer_path,
                 states,
                 rl_states):
        super().__init__(questions_path,
                         conversation_template_str,
                         intent_model_path,
                         intent_tokenizer_path,
                         states,
                         rl_states)

        self.name = name
        self.retrieval_input_variables = {}
        self.stuff_input_variables = {}

    def selectQuestion(self):
        difficulty = self.getRLStates()['difficulty']
        self.retrieval_input_variables.update({"difficulty": difficulty, "asked": "false"})
        question = self.retrieve_docs(self.retrieval_input_variables)
        self.deleteDocs(question)
        return question

    def askQuestion(self, user_input):
        question = self.selectQuestion()
        self.stuff_input_variables.update({'context': question, 'user_input': user_input})
        return self.respond(self.stuff_input_variables)

    def provide_feedback(self):
        pass

    def provide_hint(self):
        pass


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


class QuizGame:
    def __init__(self, quiz_master, player):
        self.quiz_master = quiz_master
        self.quiz_master.stuff_input_variables.update({"quiz_master": quiz_master.name, "player": player.name})
        self.player = player
        self.currentQuestion = None

    def extractQuestion(self, raw_response):
        question = {"Category": None, "Difficulty": None, "Question": None, "Options": None, "isDetected": False}
        pattern = re.compile(
            """[\s\S]*Category: [\s\S]*Difficulty: [\s\S]*Type: [\s\S]*Question: [\s\S]*Option A: [\s\S]*Option B: [\s\S]*Option C: [\s\S]*Option D: [\s\S]*"""
        )
        match = pattern.match(raw_response)
        if match:
            category_index = raw_response.find("Category: ")
            difficulty_index = raw_response.find("Difficulty: ")
            type_index = raw_response.find("Type: ")
            question_index = raw_response.find("Question: ")
            option_a_index = raw_response.find("Option A: ")
            option_b_index = raw_response.find("Option B: ")
            option_c_index = raw_response.find("Option C: ")
            option_d_index = raw_response.find("Option D: ")
            end_index = raw_response[option_d_index:-1].find('\n') + option_d_index

            options = {"A": raw_response[option_a_index + 10:option_b_index - 1],
                       "B": raw_response[option_b_index + 10:option_c_index - 1],
                       "C": raw_response[option_c_index + 10:option_d_index - 1],
                       "D": raw_response[option_d_index + 10:end_index]}

            question = {"Category": raw_response[10 + category_index:difficulty_index - 1],
                        "Difficulty": raw_response[12 + difficulty_index:type_index - 1],
                        "Type": raw_response[6 + type_index:question_index - 1],
                        "Question": raw_response[10 + question_index:option_a_index - 1],
                        "Options": options,
                        "isDetected": True}

            self.currentQuestion = question

            response = raw_response[0:category_index] + raw_response[end_index:-1]
        else:
            response = raw_response
        return question, response
