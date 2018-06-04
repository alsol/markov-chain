import random
from datatypes.dictogram import Dictogram

order = 2


class MarkovModel:
    def __init__(self):
        self.inner_dict = {}

    def __getitem__(self, item):
        if item in self.inner_dict:
            return Dictogram(self.inner_dict[item])
        return None

    def update_model(self, data):
        for i in range(0, len(data) - order):
            key = data[i] if order == 1 else tuple(data[i: i + order])
            if key in self.inner_dict:
                self.inner_dict[key].update([data[i + order]], )
            else:
                self.inner_dict[key] = Dictogram([data[i + order]])

    def get_random_start(self):
        if order == 1:
            return "*start*"
        else:
            possible_keys = [x for x in self.inner_dict.keys() if "*start*" in x]
            return random.choice(possible_keys)
