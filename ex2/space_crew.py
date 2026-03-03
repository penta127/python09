from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    # "M"で始まらない場合はエラー
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        # crew内にcommanderまたはCaptainがいるかを確認する。
        has_leader = [
            member
            for member in self.crew
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
        ]
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        # 365日を超える長期ミッションのときだけ、経験者の割合を確認する。
        if self.duration_days > 365:
            experienced_count = sum(
                member.years_experience >= 5 for member in self.crew
            )
            if experienced_count * 2 < len(self.crew):
                raise ValueError(
                    "Long missions need at least 50% experienced crew "
                    "(5+ years)"
                )

        # crewの中に、is_active=Falseのメンバーがいないかを確認する。
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def display_mission(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) "
            f"- {member.specialization}"
        )


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)
    print("Valid mission created:")

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        crew=[
            CrewMember(
                member_id="C01",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=42,
                specialization="Mission Command",
                years_experience=15,
                is_active=True,
            ),
            CrewMember(
                member_id="C02",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=35,
                specialization="Navigation",
                years_experience=8,
                is_active=True,
            ),
            CrewMember(
                member_id="C03",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=31,
                specialization="Engineering",
                years_experience=6,
                is_active=True,
            ),
        ],
        mission_status="planned",
        budget_millions=2500.0,
    )
    display_mission(valid_mission)

    print()
    print("=" * 41)
    print("Expected validation error:")

    try:
        SpaceMission(
            mission_id="M2026_TEST",
            mission_name="Outer Rim Survey",
            destination="Europa",
            launch_date=datetime.now(),
            duration_days=120,
            crew=[
                CrewMember(
                    member_id="T01",
                    name="Riley West",
                    rank=Rank.OFFICER,
                    age=29,
                    specialization="Science",
                    years_experience=4,
                    is_active=True,
                ),
                CrewMember(
                    member_id="T02",
                    name="Mina Park",
                    rank=Rank.LIEUTENANT,
                    age=33,
                    specialization="Systems",
                    years_experience=7,
                    is_active=True,
                ),
            ],
            mission_status="planned",
            budget_millions=980.0,
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
