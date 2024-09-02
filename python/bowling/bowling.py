SPARE = -2
STRIKE = -1
MAX_TURN = 10
END_GAME = 0
PIN_NUMBER = 10

TOO_MUCH_PINS = "Invalid numbers of selected pins for the frame number %d ! The score would be %d + %d = %d !"
CANT_PLAY = "You can't play anymore !"
WRONG_PIN_NUMBER = "Invalid numbers of selected pins ! %d pins selected !"


class GameError(Exception):
    pass


class BowlingGame:
    def __init__(self):
        self.score_count = 0
        self.actual_frame_number = 1
        self.frames = tuple([] for _ in range(10))
        self.throw_functions = {
            0: self._first_throw,
            1: self._second_throw,
            2: self._third_throw
        }

    def is_last_frame(self):
        return self.actual_frame_number == MAX_TURN

    def is_game_end(self):
        return self.actual_frame_number == END_GAME

    def _first_throw(self, pins, actual_frame):
        if pins == PIN_NUMBER:
            actual_frame.append(STRIKE)
            self.next_frame()
        else:
            actual_frame.append(pins)

    def _second_throw(self, pins, actual_frame):
        actual_score = actual_frame[0]
        temp_score = actual_score + pins

        if self.is_last_frame() and actual_frame[0] == STRIKE and pins == PIN_NUMBER:
            actual_frame.append(STRIKE)
        elif temp_score > PIN_NUMBER:
            raise ValueError(TOO_MUCH_PINS % (
                self.actual_frame_number, actual_score, pins, temp_score))
        elif temp_score == PIN_NUMBER:
            actual_frame.append(SPARE)
        else:
            actual_frame.append(pins)

        self.next_frame()

    def _third_throw(self, pins, actual_frame):
        actual_score = actual_frame[1]
        temp_score = actual_score + pins
        if temp_score > PIN_NUMBER and actual_frame[0] == STRIKE and actual_frame[1] != STRIKE:
            raise ValueError(TOO_MUCH_PINS % (
                self.actual_frame_number, actual_score, pins, temp_score))
        actual_frame.append(pins)
        self.next_frame()

    def next_frame(self):

        if self.is_last_frame():
            final_frame = self.frames[-1]
            throw_count = len(final_frame)
            is_first_shot_is_strike = final_frame[0] == STRIKE and throw_count == 1

            try:
                is_third_shot_is_possible = (
                    (
                        final_frame[1] in (SPARE, STRIKE)
                        or final_frame[0] == STRIKE
                    )
                    and throw_count == 2
                )
            except IndexError:
                is_third_shot_is_possible = False

            if is_first_shot_is_strike or is_third_shot_is_possible:
                return

        self.actual_frame_number = (self.actual_frame_number+1) % (MAX_TURN+1)

    def roll(self, pins: int):
        if not END_GAME < self.actual_frame_number <= MAX_TURN:
            raise ValueError(CANT_PLAY)

        if not 0 <= pins <= PIN_NUMBER:
            raise ValueError(WRONG_PIN_NUMBER % pins)

        actual_frame = self.frames[self.actual_frame_number - 1]
        number_of_throw = len(actual_frame)

        if number_of_throw in self.throw_functions:
            self.throw_functions[number_of_throw](pins, actual_frame)

    def score(self):

        if not self.is_game_end():
            raise GameError(
                "You should finish the game before calculating your score." +
                f"\nCurrent frame = {self.actual_frame_number}.")

        last_frame = self.frames[-1]

        for index, number in enumerate(last_frame):
            if number == SPARE:
                last_frame[1] = PIN_NUMBER-last_frame[0]
            elif number == STRIKE:
                last_frame[index] = PIN_NUMBER

        flat_list = sum(self.frames, [])
        final_list = flat_list[::]
        for index in range(len(flat_list)-3, -1, -1):
            number = flat_list[index]
            head = flat_list[index+1]
            if number == SPARE:
                tail = 0
                if index > 0:
                    tail = flat_list[index-1]
                flat_list[index] = PIN_NUMBER-tail
                final_list[index] = flat_list[index]+head
            elif number == STRIKE:
                next_head = flat_list[index+2]
                flat_list[index] = PIN_NUMBER
                final_list[index] = flat_list[index]+head+next_head

        return sum(final_list)