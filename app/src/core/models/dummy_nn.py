class DummyNN:
    def __init__(self):
        print("NN initiated! Wow cool!")

    def train(self, step_data):
        print("Training model on step data:")
        print(step_data)

    def spit(self, include_metadata=False):
        print("Outputting generated hip hop")
        return "This is some dummy output\nIt is not based on input"

    def get_state(self):
        print("Outputting state.")
        return "Here's some state!"

    def load_state(self, state):
        print("State received: " + state)
        print("Thanks for the state!")
