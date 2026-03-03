# 日付・時刻を扱うモジュール
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


# BaseModel を継承すると、Field を使った検証を定義できる。
class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
    print("Valid station created:")

    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.now(),
        is_operational=True,
        notes="Primary orbital research station.",
    )

    status = "Operational" if station.is_operational else "Offline"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")

    print()
    print("=" * 40)
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=23,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes="Primary orbital research station.",
        )

    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
