from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    COEFF_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_1 = 18
    RUN_COEFF_2 = 20

    def get_spent_calories(self) -> float:
        self.calories_running = ((self.RUN_COEFF_1 * self.get_mean_speed()
                                 - self.RUN_COEFF_2) * self.weight
                                 / self.M_IN_KM
                                 * self.duration * self.COEFF_MIN)
        return self.calories_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WL_CAL_COEFF_1 = 0.035
    WL_CAL_COEFF_2 = 2
    WL_CAL_COEFF_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height  # Pост

    def get_spent_calories(self) -> float:
        self.calories_sw = ((self.WL_CAL_COEFF_1 * self.weight + (self.get_mean_speed()
                            ** self.WL_CAL_COEFF_2 // self.height)
                            * self.WL_CAL_COEFF_3 * self.weight)
                            * self.duration*self.COEFF_MIN)
        return self.calories_sw


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SW_COEFF_1: float = 1.1
    SW_COEFF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        self.calories_sw = ((self.get_mean_speed() + self.SW_COEFF_1)
                            * self.SW_COEFF_2 * self.weight)
        return self.calories_sw


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    reed_dict = {'RUN': Running,
                 'WLK': SportsWalking,
                 'SWM': Swimming}
    return reed_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [1206, 12, 6]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
