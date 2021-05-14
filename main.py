from abc import ABC, abstractmethod
from datetime import datetime


class NatureEntity(ABC):
    """
    Абстрактний клас сутностей природи
    """
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    @abstractmethod
    def eat(self):
        """
        Абстрактний метод споживання, що пізніще буде перезавантажений у класах - нащадках
        :return:
        """
        pass

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def decompose(self):
        """
        Розкладення на органічні сполуки.
        Притаманне усім сутностям природи. Але набір елементів для різних груп різний
        :return:
        """
        pass


class Animals(NatureEntity):
    """
    Абстрактний клас тварин
    """
    health_states = ('good', 'poor', 'ready_to_die')

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self.population = 0
        self.health = self.health_states[0]
        self.alive = True
        self.hungry = True
        self.thirsty = True

    def move(self):
        """
        Загальний метод класу, відображаючи здатність рухатись
        :return: None
        """
        pass

    def eat(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        if self.thirsty:
            return False
        else:
            return True

    def die(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        if self.health == 'ready_to_die':
            return True
        else:
            return False

    def decompose(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        if not self.alive:
            return True
        else:
            return False

    def drink(self):
        pass

    def eat_herb(self):
        pass

    def reproduce(self):
        if self.hungry | self.thirsty:
            return False
        return True

    def live(self):
        pass

    def sleep(self):
        pass

    @abstractmethod
    def multiply(self):
        """
        Розмножування. Притаманне усім тваринам.
        Але у різний спосіб. Тому метод повинен бути перезавантажений у конкретних класів тварин
        :return:
        """
        pass


class Plants(NatureEntity):
    """
    Абстрактний клас рослин
    """

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent
        self._weight = 0

    @property
    def weight(self):
        return self._weight

    @weight.getter
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    def grow(self):
        """
        Загальний метод класу, що відтворю здатність рослин рости
        """
        pass

    def eat(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        pass

    def die(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        pass

    def decompose(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        pass


class Herbs(Plants):
    """
    Клас травин, успадкований від абстрактного класу рослин
    """
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent


class Trees(Plants):
    """
    Клас дерев, успадкований від абстрактного класу рослин
    """
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent

    def produce(self):
        pass


class Predators(Animals):
    """
    Клас хижаків, успадкований від абстрактного класу тварин
    """
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent

    def multiply(self):
        """
        Перезавантаження методу розмноження
        :return:
        """
        pass

    def hunt(self):
        pass


class Phytophages(Animals):
    """
    Клас тварин - фітофагів, успадкований від абстрактного класу тварин
    """
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent

    def multiply(self):
        """
        Перезавантаження методу розмноження
        :return:
        """
        pass


class Worms(Animals):
    """
    Клас черв'яків, успадкований від абстрактного класу тварин
    """
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.parent = parent

    def multiply(self):
        """
        Перезавантаження методу розмноження
        :return:
        """
        pass


class Insects(Animals):
    """
    Клас комах, успадкований від абстрактного класу тварин
    """
    def __init__(self, name, parent):
        super(Insects, self).__init__(name, parent)
        self.parent = parent

    def multiply(self):
        """
        Перезавантаження методу розмноження
        :return:
        """
        pass


class Producers:
    """
    Клас продуцентів
    """

    def __init__(self, parent):
        """
        Конструктор класу продуцентів
        """
        self.parent = parent
        self.herbs = []
        self.trees = []

        self._weight = 0

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if (value < self.parent.weight() * 0.1) | (value > self.parent.weight() * 0.3):
            raise ValueError
        self._weight = value

    @weight.getter
    def weight(self):
        return self._weight

    def weight_ratio(self):
        return weight_calculate(self.trees) / weight_calculate(self.herbs)

    def check_weights(self):
        assert self.weight_ratio() == 0.2

    def add_herb(self, herb):
        self.herbs.append(herb)

    def add_tree(self, tree):
        self.trees.append(tree)


class Consumers:
    """
    Клас консументів
    """
    phases = ('born', 'adult', 'old', 'died')

    def __init__(self, parent, phytophages=None, predators=None):
        """
        Констрактор класу консументів
        :param phytophages: звірі-фітофаги
        :param predators: звірі-хижаки
        """
        self.phytophages = phytophages
        self.predators = predators

        self._biomass_weight = 0

    @property
    def biomass_weight(self):
        return self._biomass_weight

    @biomass_weight.getter
    def biomass_weight(self):
        return self._biomass_weight

    @biomass_weight.setter
    def biomass_weight(self, value):
        self._biomass_weight = value


class Detriophages:
    """
    Клас детріофагів
    """
    decompose_factor = 0.96

    def __init__(self, parent, members):
        """
        Конструктор класу детріофагів
        :param members: список (list) членів класу
        """
        # перевірка типу параметру, що був переданий конструктору
        if not isinstance(members, list):
            raise TypeError
        self.members = members
        self._biomass_weight = 0

    @property
    def biomass_weight(self):
        return self._biomass_weight

    @biomass_weight.getter
    def biomass_weight(self):
        return self._biomass_weight

    @biomass_weight.setter
    def biomass_weight(self, value):
        self._biomass_weight = value

    def active_decompose(self, weight):
        """
        Активна декомпозиція (розклад) сутностей природи
        :param weight: маса сутності природи, що розкладається детріофагами
        :return: час декомпозиції, сукупна маса декомпозованих речовин
        """
        decompose_time = 0
        return decompose_time, self.decompose_factor * weight


class AbioticFactors:
    """
    Клас абіотичних факторів
    """

    def __init__(self, parent, **factors):
        """
        Конструктор класу абіотичних факторів
        :param factors: словник факторів
        """
        self.factors = factors
        self.parent = parent
        self._daytemp = 0
        self._nighttemp = 0

    @property
    def daytemp(self):
        return self._daytemp

    @daytemp.setter
    def daytemp(self, value):
        self._daytemp = value

    @property
    def nighttemp(self):
        return self._nighttemp

    @nighttemp.setter
    def nighttemp(self, value):
        self._nighttemp = value

    def give_water(self, consumer):
        """
        Задовільнити потребу у воді
        :param consumer: споживач, чия потреба у воді задовільняється
        :return:
        """

    def get_temp(self):
        return self.parent.temp


class Forest:
    """
    Клас ліс
    """
    sun = True

    def __init__(self, **systems):
        """
        Конструктор класу ліс
        """
        self.subsystems = systems

        # властивості системи
        self._weight = 0
        self._balance = True

        # параметри системи
        self.time = datetime.now()
        self.temp = 0

    @property
    def weight(self):
        return self._weight

    @weight.getter
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def balance(self):
        return self._balance

    @balance.getter
    def balance(self):
        return self._balance

    def sunrise(self):
        self.sun = True
        self.temp = 19

    def sunset(self):
        self.sun = False
        self.temp = 17

    def crush(self):
        pass

    def check_requirements(self):
        # вимоги до підсистеми Consumers
        producers_weight = self.subsystems['producers'].weight()
        phytophages_weight = self.subsystems['consumers'].phytophages.weight()
        predators_weight = self.subsystems['consumers'].predators.weight()
        assert phytophages_weight == 0.1 * producers_weight
        assert predators_weight == 0.1 * phytophages_weight

        # вимоги до підсистеми Detriophages

        # вимоги до підсистеми AbioticFactors
        assert self.subsystems['abiotics'].daytemp() > 18
        assert self.subsystems['abiotics'].nighttemp() > 14
        assert self.subsystems['abiotics'].daytemp() < 20
        assert self.subsystems['abiotics'].nighttemp() < 16

    def light_photosyntesis_phase(self):
        self.time = datetime.now()
        if (self.time.hour > 6) & (self.time.hour < 19):
            return True
        else:
            return False


def weight_calculate(lst):
    return sum([item.weight for item in lst])


if __name__ == '__main__':
    f = Forest()
    herb1 = Herbs('Herb1', f)
    herb2 = Herbs('Herb2', f)
    producers = Producers(f)
    consumers = Consumers(f)
    detr1 = Insects('Insect', f)
    detr2 = Worms('Worms', f)
    detrio = Detriophages(f, [detr1, detr2])
    abio = AbioticFactors(f)
