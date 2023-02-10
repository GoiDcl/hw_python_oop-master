from dataclasses import dataclass
from typing import Dict
from typing import Type
import traceback
import logging

@dataclass
class InfoMessage:
    """Massage dataclass."""
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
        """Return training info."""
        return (
            f'Training type: {self.training_type}; '
            f'Duration: {self.duration:.3f} ч.; '
            f'Distance: {self.distance:.3f} км; '
            f'Mean speed: {self.speed:.3f} км/ч; '
            f'Calories spent: {self.calories:.3f}.'
        )


class Training:
    """Base training class."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

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
        """Calculate covered distance."""
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Base method for calculate mean speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Template of method for calculate calories."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Collects training data using dataclass."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )
        return info


class Running(Training):
    """
    Base running training class.
    Mean speed present in km/h.
    """
    CAL_MULT: int = 18
    CAL_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Unique method for calculate calories for running."""
        MIN_IN_H = self.duration * 60
        return (
                (self.CAL_MULT * self.get_mean_speed()
                 + self.CAL_SHIFT) * self.weight
                 / Training.M_IN_KM * MIN_IN_H
        )


class SportsWalking(Training):
    """
    Base walking training class.
    Using different multiplayers.
    Additionally using height of the user in sm.
    Mean speed present in m/s.
    """
    CAL_MULT: float = 0.035
    CAL_SHIFT: float = 0.029
    MS: float = 0.278
    SANT: int = 100
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self) -> float:
        """Unique method for calculate calories for walking."""
        return (
                (self.CAL_MULT * self.weight
                + ((self.get_mean_speed() * self.MS)**2 / (self.height / self.SANT))
                * self.CAL_SHIFT * self.weight) * self.duration * self.MIN_IN_H
        )


class Swimming(Training):
    """
    Base swimming training class.
    Using different base step constant and multiplayers.
    """
    LEN_STEP: float = 1.38
    CAL_MULT: float = 1.1
    CAL_SHIFT: int = 2

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
        """Unique method for calculate mean speed for swiming."""
        return (self.length_pool * self.count_pool / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Unique method for calculate calories for swiming."""
        return ((self.get_mean_speed() + self.CAL_MULT)
                * self.CAL_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Method for unpacking data package coming from sensors."""
    check_type: Dict[str, Type[Trainig]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return check_type[workout_type](*data)
    except Exception as e:
        print(
            'Only works with training types such as SWM for swiming,'
            'RUN for running and WLK for walking'
        )

def main(training: Training) -> None:
    """Main funcion"""
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

