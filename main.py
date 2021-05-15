from abc import ABC, abstractmethod
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor as tpe
from queue import Queue


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
        """
        Абстрактний метод вмирання, що перезавантажується у класах нащадках
        :return:
        """
        pass

    @abstractmethod
    def breath(self):
        """
        Абстрактний метод дихання, що перезавантажується у класах нащадках
        :return:
        """
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
        self.components = []
        self.descendants = []
        self._alive = True
        self._hungry = True
        self._thirsty = True
        self._alive = True
        self._tired = True

    @property
    def thirsty(self):
        return self._thirsty

    @thirsty.setter
    def thirsty(self, value):
        self._thirsty = value

    @property
    def hungry(self):
        return self._hungry

    @hungry.setter
    def hungry(self, value):
        self._hungry = value

    @property
    def alive(self):
        if self.health in self.health_states[:-1]:
            return True
        else:
            return False

    @property
    def tired(self):
        return self._tired

    @tired.setter
    def tired(self, value):
        self._tired = value

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
            self.hungry = False
            return True

    def die(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        if self.health == 'ready_to_die':
            elements = self.decompose()
            self.parent.elements.put(elements)
            return True
        else:
            return False

    def decompose(self):
        """
        Перезавантаження абстрактного методу
        :return:
        """
        if not self.alive:
            return self.components
        else:
            return None

    def drink(self):
        """
        Метод пиття. Отримує воду від абіотичних факторів
        :return:
        """
        water = self.parent.subsystems['abiotics'].get_water()
        self.thirsty = False
        return True

    def eat_herb(self):
        """
        Метод поїдання трав. Отримує їх від консументів
        :return:
        """
        herbs = self.parent.subsystems['producers'].give_herb()

    def reproduce(self, pr):
        """
        Метод розмноження
        :param pr: партнер
        :return:
        """
        if self.hungry | self.thirsty:
            return False
        if self.health in self.health_states[1:]:
            return False
        if (self.fertilize()) & (self.get_descendant(pr)):
            self.tired = True
            return True
        else:
            return False

    def get_descendant(self, pr):
        """
        Отримання нащадка від партнера
        Додає до списку власних нащадків
        :param pr: партнер
        :return: нащадка
        """
        if desc := pr.give_descendant():
            self.descendants.append(desc)
        return True

    def give_descendant(self):
        """
        Метод, що дає нащадка партнерові
        :return:
        """
        return True

    def sleep(self):
        """
        Метод спати. Спрацьовує, якщо нічний час або втома
        :return:
        """
        while self.alive:
            if not daytime(datetime.now()) | self.tired:
                pass
            else:
                pass

    def breath(self):
        """
        Метод дихати
        :return:
        """
        while self.alive:
            pass

    def fertilize(self):
        """
        Метод дати елементи живлення
        :return:
        """
        return True

    def find_partner(self):
        """
        Метод пошуку партнера
        :return:
        """
        return Animals()

    def main_life_cycle(self):
        """
         Життєвий цикл консументу
        :return:
        """
        while self.alive:
            while self.thirsty:
                self.drink()
            while pr.hungry:
                self.eat()
            self.reproduce(self.find_partner())
        self.die()
        self.decompose()


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

    def breath(self):
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

    def hunt(self):
        return True

    def eat(self):
        if self.hunt():
            self.hungry = False
            return True
        else:
            return False


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

    def give_herb(self):
        pass

    def get_nutrients(self):
        if not self.parent.elements.empty():
            pass


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

        # елементи системи
        self.elements = Queue()

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
        """
        Схід сонця
        :return:
        """
        self.sun = True
        self.temp = 19

    def sunset(self):
        """
        Захід сонця
        :return:
        """
        self.sun = False
        self.temp = 17

    def crush(self):
        """
        Crush системи
        :return:
        """
        pass

    def check_requirements(self):
        """
        Перевірка вимог до підсистем
        :return:
        """
        # вимоги до підсистеми Consumers
        producers_weight = self.subsystems['producers'].weight()
        phytophages_weight = self.subsystems['consumers'].phytophages.weight()
        predators_weight = self.subsystems['consumers'].predators.weight()
        assert phytophages_weight == 0.1 * producers_weight
        assert predators_weight == 0.1 * phytophages_weight

        # вимоги до підсистеми AbioticFactors
        assert self.subsystems['abiotics'].daytemp() > 18
        assert self.subsystems['abiotics'].nighttemp() > 14
        assert self.subsystems['abiotics'].daytemp() < 20
        assert self.subsystems['abiotics'].nighttemp() < 16

    def light_photosyntesis_phase(self):
        """
        Перевіряє, чи фаза світлового фотосинтезу є поточною
        :return:
        """
        self.time = datetime.now()
        if (self.time.hour > 6) & (self.time.hour < 19):
            return True
        else:
            return False


def weight_calculate(lst):
    """
    Визначення сумарної маси
    :param lst: елементи системи
    :return: числове значення сумарної маси
    """
    return sum([item.weight for item in lst])


def daytime(time):
    """
    Повертає True, якщо переданий параметр є денним часом
    :param time: час, який треба визначити
    :return:
    """
    return True


if __name__ == '__main__':
    # створення екземплярів об'єктів
    f = Forest()
    herb1 = Herbs('Herb1', f)
    herb2 = Herbs('Herb2', f)
    pp = Phytophages('Миша', parent=None)
    pr = Predators('Вовк', parent=None)
    producer = Producers(f)
    consumer = Consumers(f)
    consumer.phytophages = [pp]
    consumer.predators = [pr]
    detr1 = Insects('Insect', f)
    detr2 = Worms('Worms', f)
    detrio = Detriophages(f, [detr1, detr2])
    abio = AbioticFactors(f)

    # відтворення життєвих циклів
    # на основі Sequence diagram
    # запуск в паралельному потоці життєвого циклу консументу
    th = Thread(target=pr.main_life_cycle, args=(pr, ))
    th.start()

    # відтворення життєвих циклів
    # на основі activity diagram
    with tpe(max_workers=3) as executor:
        executor.submit(pr.breath)
        executor.submit(pr.main_life_cycle)
        executor.submit(pr.sleep)








