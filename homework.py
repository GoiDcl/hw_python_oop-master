class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        MIN_IN_H = self.duration * 60

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )
        return info


class Running(Training):
    CAL_MULT = 18
    CAL_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        MIN_IN_H = self.duration * 60
        return (
                (self.CAL_MULT
                 * self.get_mean_speed()
                 + self.CAL_SHIFT) * self.weight
                 / Training.M_IN_KM * MIN_IN_H
        )


class SportsWalking(Training):
    CAL_MULT = 0.035
    CAL_SHIFT = 0.029
    MS = 0.278
    SANT = 100
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self) -> float:
        return (
                (self.CAL_MULT * self.weight
                + ((self.get_mean_speed() * self.MS)**2 / (self.height / self.SANT))
                * self.CAL_SHIFT * self.weight) * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    LEN_STEP = 1.38
    CAL_MULT = 1.1
    CAL_SHIFT = 2

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                length_pool: int,
                count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool


    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CAL_MULT)
                * self.CAL_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    check_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return check_type[workout_type](*data)

def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

