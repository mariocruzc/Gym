from typing import Dict, Tuple

# The following is a map of environments which have been relocated
# to a different namespace. This map is important when reporting
# new versions of an environment outside of Gym.
# This map should be removed eventually once users
# are sufficiently aware of the environment relocations.
# The value of the mapping is (namespace, package,).
internal_env_relocation_map: Dict[str, Tuple[str, str]] = {
    "Adventure": ("ALE", "ale-py"),
    "AdventureDeterministic": (None, "ale-py"),
    "AdventureNoFrameskip": (None, "ale-py"),
    "Adventure-ram": ("ALE", "ale-py"),
    "Adventure-ramDeterministic": (None, "ale-py"),
    "Adventure-ramNoFrameskip": (None, "ale-py"),
    "AirRaid": ("ALE", "ale-py"),
    "AirRaidDeterministic": (None, "ale-py"),
    "AirRaidNoFrameskip": (None, "ale-py"),
    "AirRaid-ram": ("ALE", "ale-py"),
    "AirRaid-ramDeterministic": (None, "ale-py"),
    "AirRaid-ramNoFrameskip": (None, "ale-py"),
    "Alien": ("ALE", "ale-py"),
    "AlienDeterministic": (None, "ale-py"),
    "AlienNoFrameskip": (None, "ale-py"),
    "Alien-ram": ("ALE", "ale-py"),
    "Alien-ramDeterministic": (None, "ale-py"),
    "Alien-ramNoFrameskip": (None, "ale-py"),
    "Amidar": ("ALE", "ale-py"),
    "AmidarDeterministic": (None, "ale-py"),
    "AmidarNoFrameskip": (None, "ale-py"),
    "Amidar-ram": ("ALE", "ale-py"),
    "Amidar-ramDeterministic": (None, "ale-py"),
    "Amidar-ramNoFrameskip": (None, "ale-py"),
    "Assault": ("ALE", "ale-py"),
    "AssaultDeterministic": (None, "ale-py"),
    "AssaultNoFrameskip": (None, "ale-py"),
    "Assault-ram": ("ALE", "ale-py"),
    "Assault-ramDeterministic": (None, "ale-py"),
    "Assault-ramNoFrameskip": (None, "ale-py"),
    "Asterix": ("ALE", "ale-py"),
    "AsterixDeterministic": (None, "ale-py"),
    "AsterixNoFrameskip": (None, "ale-py"),
    "Asterix-ram": ("ALE", "ale-py"),
    "Asterix-ramDeterministic": (None, "ale-py"),
    "Asterix-ramNoFrameskip": (None, "ale-py"),
    "Asteroids": ("ALE", "ale-py"),
    "AsteroidsDeterministic": (None, "ale-py"),
    "AsteroidsNoFrameskip": (None, "ale-py"),
    "Asteroids-ram": ("ALE", "ale-py"),
    "Asteroids-ramDeterministic": (None, "ale-py"),
    "Asteroids-ramNoFrameskip": (None, "ale-py"),
    "Atlantis": ("ALE", "ale-py"),
    "AtlantisDeterministic": (None, "ale-py"),
    "AtlantisNoFrameskip": (None, "ale-py"),
    "Atlantis-ram": ("ALE", "ale-py"),
    "Atlantis-ramDeterministic": (None, "ale-py"),
    "Atlantis-ramNoFrameskip": (None, "ale-py"),
    "BankHeist": ("ALE", "ale-py"),
    "BankHeistDeterministic": (None, "ale-py"),
    "BankHeistNoFrameskip": (None, "ale-py"),
    "BankHeist-ram": ("ALE", "ale-py"),
    "BankHeist-ramDeterministic": (None, "ale-py"),
    "BankHeist-ramNoFrameskip": (None, "ale-py"),
    "BattleZone": ("ALE", "ale-py"),
    "BattleZoneDeterministic": (None, "ale-py"),
    "BattleZoneNoFrameskip": (None, "ale-py"),
    "BattleZone-ram": ("ALE", "ale-py"),
    "BattleZone-ramDeterministic": (None, "ale-py"),
    "BattleZone-ramNoFrameskip": (None, "ale-py"),
    "BeamRider": ("ALE", "ale-py"),
    "BeamRiderDeterministic": (None, "ale-py"),
    "BeamRiderNoFrameskip": (None, "ale-py"),
    "BeamRider-ram": ("ALE", "ale-py"),
    "BeamRider-ramDeterministic": (None, "ale-py"),
    "BeamRider-ramNoFrameskip": (None, "ale-py"),
    "Berzerk": ("ALE", "ale-py"),
    "BerzerkDeterministic": (None, "ale-py"),
    "BerzerkNoFrameskip": (None, "ale-py"),
    "Berzerk-ram": ("ALE", "ale-py"),
    "Berzerk-ramDeterministic": (None, "ale-py"),
    "Berzerk-ramNoFrameskip": (None, "ale-py"),
    "Bowling": ("ALE", "ale-py"),
    "BowlingDeterministic": (None, "ale-py"),
    "BowlingNoFrameskip": (None, "ale-py"),
    "Bowling-ram": ("ALE", "ale-py"),
    "Bowling-ramDeterministic": (None, "ale-py"),
    "Bowling-ramNoFrameskip": (None, "ale-py"),
    "Boxing": ("ALE", "ale-py"),
    "BoxingDeterministic": (None, "ale-py"),
    "BoxingNoFrameskip": (None, "ale-py"),
    "Boxing-ram": ("ALE", "ale-py"),
    "Boxing-ramDeterministic": (None, "ale-py"),
    "Boxing-ramNoFrameskip": (None, "ale-py"),
    "Breakout": ("ALE", "ale-py"),
    "BreakoutDeterministic": (None, "ale-py"),
    "BreakoutNoFrameskip": (None, "ale-py"),
    "Breakout-ram": ("ALE", "ale-py"),
    "Breakout-ramDeterministic": (None, "ale-py"),
    "Breakout-ramNoFrameskip": (None, "ale-py"),
    "Carnival": ("ALE", "ale-py"),
    "CarnivalDeterministic": (None, "ale-py"),
    "CarnivalNoFrameskip": (None, "ale-py"),
    "Carnival-ram": ("ALE", "ale-py"),
    "Carnival-ramDeterministic": (None, "ale-py"),
    "Carnival-ramNoFrameskip": (None, "ale-py"),
    "Centipede": ("ALE", "ale-py"),
    "CentipedeDeterministic": (None, "ale-py"),
    "CentipedeNoFrameskip": (None, "ale-py"),
    "Centipede-ram": ("ALE", "ale-py"),
    "Centipede-ramDeterministic": (None, "ale-py"),
    "Centipede-ramNoFrameskip": (None, "ale-py"),
    "ChopperCommand": ("ALE", "ale-py"),
    "ChopperCommandDeterministic": (None, "ale-py"),
    "ChopperCommandNoFrameskip": (None, "ale-py"),
    "ChopperCommand-ram": ("ALE", "ale-py"),
    "ChopperCommand-ramDeterministic": (None, "ale-py"),
    "ChopperCommand-ramNoFrameskip": (None, "ale-py"),
    "CrazyClimber": ("ALE", "ale-py"),
    "CrazyClimberDeterministic": (None, "ale-py"),
    "CrazyClimberNoFrameskip": (None, "ale-py"),
    "CrazyClimber-ram": ("ALE", "ale-py"),
    "CrazyClimber-ramDeterministic": (None, "ale-py"),
    "CrazyClimber-ramNoFrameskip": (None, "ale-py"),
    "Defender": ("ALE", "ale-py"),
    "DefenderDeterministic": (None, "ale-py"),
    "DefenderNoFrameskip": (None, "ale-py"),
    "Defender-ram": ("ALE", "ale-py"),
    "Defender-ramDeterministic": (None, "ale-py"),
    "Defender-ramNoFrameskip": (None, "ale-py"),
    "DemonAttack": ("ALE", "ale-py"),
    "DemonAttackDeterministic": (None, "ale-py"),
    "DemonAttackNoFrameskip": (None, "ale-py"),
    "DemonAttack-ram": ("ALE", "ale-py"),
    "DemonAttack-ramDeterministic": (None, "ale-py"),
    "DemonAttack-ramNoFrameskip": (None, "ale-py"),
    "DoubleDunk": ("ALE", "ale-py"),
    "DoubleDunkDeterministic": (None, "ale-py"),
    "DoubleDunkNoFrameskip": (None, "ale-py"),
    "DoubleDunk-ram": ("ALE", "ale-py"),
    "DoubleDunk-ramDeterministic": (None, "ale-py"),
    "DoubleDunk-ramNoFrameskip": (None, "ale-py"),
    "ElevatorAction": ("ALE", "ale-py"),
    "ElevatorActionDeterministic": (None, "ale-py"),
    "ElevatorActionNoFrameskip": (None, "ale-py"),
    "ElevatorAction-ram": ("ALE", "ale-py"),
    "ElevatorAction-ramDeterministic": (None, "ale-py"),
    "ElevatorAction-ramNoFrameskip": (None, "ale-py"),
    "Enduro": ("ALE", "ale-py"),
    "EnduroDeterministic": (None, "ale-py"),
    "EnduroNoFrameskip": (None, "ale-py"),
    "Enduro-ram": ("ALE", "ale-py"),
    "Enduro-ramDeterministic": (None, "ale-py"),
    "Enduro-ramNoFrameskip": (None, "ale-py"),
    "FishingDerby": ("ALE", "ale-py"),
    "FishingDerbyDeterministic": (None, "ale-py"),
    "FishingDerbyNoFrameskip": (None, "ale-py"),
    "FishingDerby-ram": ("ALE", "ale-py"),
    "FishingDerby-ramDeterministic": (None, "ale-py"),
    "FishingDerby-ramNoFrameskip": (None, "ale-py"),
    "Freeway": ("ALE", "ale-py"),
    "FreewayDeterministic": (None, "ale-py"),
    "FreewayNoFrameskip": (None, "ale-py"),
    "Freeway-ram": ("ALE", "ale-py"),
    "Freeway-ramDeterministic": (None, "ale-py"),
    "Freeway-ramNoFrameskip": (None, "ale-py"),
    "Frostbite": ("ALE", "ale-py"),
    "FrostbiteDeterministic": (None, "ale-py"),
    "FrostbiteNoFrameskip": (None, "ale-py"),
    "Frostbite-ram": ("ALE", "ale-py"),
    "Frostbite-ramDeterministic": (None, "ale-py"),
    "Frostbite-ramNoFrameskip": (None, "ale-py"),
    "Gopher": ("ALE", "ale-py"),
    "GopherDeterministic": (None, "ale-py"),
    "GopherNoFrameskip": (None, "ale-py"),
    "Gopher-ram": ("ALE", "ale-py"),
    "Gopher-ramDeterministic": (None, "ale-py"),
    "Gopher-ramNoFrameskip": (None, "ale-py"),
    "Gravitar": ("ALE", "ale-py"),
    "GravitarDeterministic": (None, "ale-py"),
    "GravitarNoFrameskip": (None, "ale-py"),
    "Gravitar-ram": ("ALE", "ale-py"),
    "Gravitar-ramDeterministic": (None, "ale-py"),
    "Gravitar-ramNoFrameskip": (None, "ale-py"),
    "Hero": ("ALE", "ale-py"),
    "HeroDeterministic": (None, "ale-py"),
    "HeroNoFrameskip": (None, "ale-py"),
    "Hero-ram": ("ALE", "ale-py"),
    "Hero-ramDeterministic": (None, "ale-py"),
    "Hero-ramNoFrameskip": (None, "ale-py"),
    "IceHockey": ("ALE", "ale-py"),
    "IceHockeyDeterministic": (None, "ale-py"),
    "IceHockeyNoFrameskip": (None, "ale-py"),
    "IceHockey-ram": ("ALE", "ale-py"),
    "IceHockey-ramDeterministic": (None, "ale-py"),
    "IceHockey-ramNoFrameskip": (None, "ale-py"),
    "Jamesbond": ("ALE", "ale-py"),
    "JamesbondDeterministic": (None, "ale-py"),
    "JamesbondNoFrameskip": (None, "ale-py"),
    "Jamesbond-ram": ("ALE", "ale-py"),
    "Jamesbond-ramDeterministic": (None, "ale-py"),
    "Jamesbond-ramNoFrameskip": (None, "ale-py"),
    "JourneyEscape": ("ALE", "ale-py"),
    "JourneyEscapeDeterministic": (None, "ale-py"),
    "JourneyEscapeNoFrameskip": (None, "ale-py"),
    "JourneyEscape-ram": ("ALE", "ale-py"),
    "JourneyEscape-ramDeterministic": (None, "ale-py"),
    "JourneyEscape-ramNoFrameskip": (None, "ale-py"),
    "Kangaroo": ("ALE", "ale-py"),
    "KangarooDeterministic": (None, "ale-py"),
    "KangarooNoFrameskip": (None, "ale-py"),
    "Kangaroo-ram": ("ALE", "ale-py"),
    "Kangaroo-ramDeterministic": (None, "ale-py"),
    "Kangaroo-ramNoFrameskip": (None, "ale-py"),
    "Krull": ("ALE", "ale-py"),
    "KrullDeterministic": (None, "ale-py"),
    "KrullNoFrameskip": (None, "ale-py"),
    "Krull-ram": ("ALE", "ale-py"),
    "Krull-ramDeterministic": (None, "ale-py"),
    "Krull-ramNoFrameskip": (None, "ale-py"),
    "KungFuMaster": ("ALE", "ale-py"),
    "KungFuMasterDeterministic": (None, "ale-py"),
    "KungFuMasterNoFrameskip": (None, "ale-py"),
    "KungFuMaster-ram": ("ALE", "ale-py"),
    "KungFuMaster-ramDeterministic": (None, "ale-py"),
    "KungFuMaster-ramNoFrameskip": (None, "ale-py"),
    "MontezumaRevenge": ("ALE", "ale-py"),
    "MontezumaRevengeDeterministic": (None, "ale-py"),
    "MontezumaRevengeNoFrameskip": (None, "ale-py"),
    "MontezumaRevenge-ram": ("ALE", "ale-py"),
    "MontezumaRevenge-ramDeterministic": (None, "ale-py"),
    "MontezumaRevenge-ramNoFrameskip": (None, "ale-py"),
    "MsPacman": ("ALE", "ale-py"),
    "MsPacmanDeterministic": (None, "ale-py"),
    "MsPacmanNoFrameskip": (None, "ale-py"),
    "MsPacman-ram": ("ALE", "ale-py"),
    "MsPacman-ramDeterministic": (None, "ale-py"),
    "MsPacman-ramNoFrameskip": (None, "ale-py"),
    "NameThisGame": ("ALE", "ale-py"),
    "NameThisGameDeterministic": (None, "ale-py"),
    "NameThisGameNoFrameskip": (None, "ale-py"),
    "NameThisGame-ram": ("ALE", "ale-py"),
    "NameThisGame-ramDeterministic": (None, "ale-py"),
    "NameThisGame-ramNoFrameskip": (None, "ale-py"),
    "Phoenix": ("ALE", "ale-py"),
    "PhoenixDeterministic": (None, "ale-py"),
    "PhoenixNoFrameskip": (None, "ale-py"),
    "Phoenix-ram": ("ALE", "ale-py"),
    "Phoenix-ramDeterministic": (None, "ale-py"),
    "Phoenix-ramNoFrameskip": (None, "ale-py"),
    "Pitfall": ("ALE", "ale-py"),
    "PitfallDeterministic": (None, "ale-py"),
    "PitfallNoFrameskip": (None, "ale-py"),
    "Pitfall-ram": ("ALE", "ale-py"),
    "Pitfall-ramDeterministic": (None, "ale-py"),
    "Pitfall-ramNoFrameskip": (None, "ale-py"),
    "Pong": ("ALE", "ale-py"),
    "PongDeterministic": (None, "ale-py"),
    "PongNoFrameskip": (None, "ale-py"),
    "Pong-ram": ("ALE", "ale-py"),
    "Pong-ramDeterministic": (None, "ale-py"),
    "Pong-ramNoFrameskip": (None, "ale-py"),
    "Pooyan": ("ALE", "ale-py"),
    "PooyanDeterministic": (None, "ale-py"),
    "PooyanNoFrameskip": (None, "ale-py"),
    "Pooyan-ram": ("ALE", "ale-py"),
    "Pooyan-ramDeterministic": (None, "ale-py"),
    "Pooyan-ramNoFrameskip": (None, "ale-py"),
    "PrivateEye": ("ALE", "ale-py"),
    "PrivateEyeDeterministic": (None, "ale-py"),
    "PrivateEyeNoFrameskip": (None, "ale-py"),
    "PrivateEye-ram": ("ALE", "ale-py"),
    "PrivateEye-ramDeterministic": (None, "ale-py"),
    "PrivateEye-ramNoFrameskip": (None, "ale-py"),
    "Qbert": ("ALE", "ale-py"),
    "QbertDeterministic": (None, "ale-py"),
    "QbertNoFrameskip": (None, "ale-py"),
    "Qbert-ram": ("ALE", "ale-py"),
    "Qbert-ramDeterministic": (None, "ale-py"),
    "Qbert-ramNoFrameskip": (None, "ale-py"),
    "Riverraid": ("ALE", "ale-py"),
    "RiverraidDeterministic": (None, "ale-py"),
    "RiverraidNoFrameskip": (None, "ale-py"),
    "Riverraid-ram": ("ALE", "ale-py"),
    "Riverraid-ramDeterministic": (None, "ale-py"),
    "Riverraid-ramNoFrameskip": (None, "ale-py"),
    "RoadRunner": ("ALE", "ale-py"),
    "RoadRunnerDeterministic": (None, "ale-py"),
    "RoadRunnerNoFrameskip": (None, "ale-py"),
    "RoadRunner-ram": ("ALE", "ale-py"),
    "RoadRunner-ramDeterministic": (None, "ale-py"),
    "RoadRunner-ramNoFrameskip": (None, "ale-py"),
    "Robotank": ("ALE", "ale-py"),
    "RobotankDeterministic": (None, "ale-py"),
    "RobotankNoFrameskip": (None, "ale-py"),
    "Robotank-ram": ("ALE", "ale-py"),
    "Robotank-ramDeterministic": (None, "ale-py"),
    "Robotank-ramNoFrameskip": (None, "ale-py"),
    "Seaquest": ("ALE", "ale-py"),
    "SeaquestDeterministic": (None, "ale-py"),
    "SeaquestNoFrameskip": (None, "ale-py"),
    "Seaquest-ram": ("ALE", "ale-py"),
    "Seaquest-ramDeterministic": (None, "ale-py"),
    "Seaquest-ramNoFrameskip": (None, "ale-py"),
    "Skiing": ("ALE", "ale-py"),
    "SkiingDeterministic": (None, "ale-py"),
    "SkiingNoFrameskip": (None, "ale-py"),
    "Skiing-ram": ("ALE", "ale-py"),
    "Skiing-ramDeterministic": (None, "ale-py"),
    "Skiing-ramNoFrameskip": (None, "ale-py"),
    "Solaris": ("ALE", "ale-py"),
    "SolarisDeterministic": (None, "ale-py"),
    "SolarisNoFrameskip": (None, "ale-py"),
    "Solaris-ram": ("ALE", "ale-py"),
    "Solaris-ramDeterministic": (None, "ale-py"),
    "Solaris-ramNoFrameskip": (None, "ale-py"),
    "SpaceInvaders": ("ALE", "ale-py"),
    "SpaceInvadersDeterministic": (None, "ale-py"),
    "SpaceInvadersNoFrameskip": (None, "ale-py"),
    "SpaceInvaders-ram": ("ALE", "ale-py"),
    "SpaceInvaders-ramDeterministic": (None, "ale-py"),
    "SpaceInvaders-ramNoFrameskip": (None, "ale-py"),
    "StarGunner": ("ALE", "ale-py"),
    "StarGunnerDeterministic": (None, "ale-py"),
    "StarGunnerNoFrameskip": (None, "ale-py"),
    "StarGunner-ram": ("ALE", "ale-py"),
    "StarGunner-ramDeterministic": (None, "ale-py"),
    "StarGunner-ramNoFrameskip": (None, "ale-py"),
    "Tennis": ("ALE", "ale-py"),
    "TennisDeterministic": (None, "ale-py"),
    "TennisNoFrameskip": (None, "ale-py"),
    "Tennis-ram": ("ALE", "ale-py"),
    "Tennis-ramDeterministic": (None, "ale-py"),
    "Tennis-ramNoFrameskip": (None, "ale-py"),
    "TimePilot": ("ALE", "ale-py"),
    "TimePilotDeterministic": (None, "ale-py"),
    "TimePilotNoFrameskip": (None, "ale-py"),
    "TimePilot-ram": ("ALE", "ale-py"),
    "TimePilot-ramDeterministic": (None, "ale-py"),
    "TimePilot-ramNoFrameskip": (None, "ale-py"),
    "Tutankham": ("ALE", "ale-py"),
    "TutankhamDeterministic": (None, "ale-py"),
    "TutankhamNoFrameskip": (None, "ale-py"),
    "Tutankham-ram": ("ALE", "ale-py"),
    "Tutankham-ramDeterministic": (None, "ale-py"),
    "Tutankham-ramNoFrameskip": (None, "ale-py"),
    "UpNDown": ("ALE", "ale-py"),
    "UpNDownDeterministic": (None, "ale-py"),
    "UpNDownNoFrameskip": (None, "ale-py"),
    "UpNDown-ram": ("ALE", "ale-py"),
    "UpNDown-ramDeterministic": (None, "ale-py"),
    "UpNDown-ramNoFrameskip": (None, "ale-py"),
    "Venture": ("ALE", "ale-py"),
    "VentureDeterministic": (None, "ale-py"),
    "VentureNoFrameskip": (None, "ale-py"),
    "Venture-ram": ("ALE", "ale-py"),
    "Venture-ramDeterministic": (None, "ale-py"),
    "Venture-ramNoFrameskip": (None, "ale-py"),
    "VideoPinball": ("ALE", "ale-py"),
    "VideoPinballDeterministic": (None, "ale-py"),
    "VideoPinballNoFrameskip": (None, "ale-py"),
    "VideoPinball-ram": ("ALE", "ale-py"),
    "VideoPinball-ramDeterministic": (None, "ale-py"),
    "VideoPinball-ramNoFrameskip": (None, "ale-py"),
    "WizardOfWor": ("ALE", "ale-py"),
    "WizardOfWorDeterministic": (None, "ale-py"),
    "WizardOfWorNoFrameskip": (None, "ale-py"),
    "WizardOfWor-ram": ("ALE", "ale-py"),
    "WizardOfWor-ramDeterministic": (None, "ale-py"),
    "WizardOfWor-ramNoFrameskip": (None, "ale-py"),
    "YarsRevenge": ("ALE", "ale-py"),
    "YarsRevengeDeterministic": (None, "ale-py"),
    "YarsRevengeNoFrameskip": (None, "ale-py"),
    "YarsRevenge-ram": ("ALE", "ale-py"),
    "YarsRevenge-ramDeterministic": (None, "ale-py"),
    "YarsRevenge-ramNoFrameskip": (None, "ale-py"),
    "Zaxxon": ("ALE", "ale-py"),
    "ZaxxonDeterministic": (None, "ale-py"),
    "ZaxxonNoFrameskip": (None, "ale-py"),
    "Zaxxon-ram": ("ALE", "ale-py"),
    "Zaxxon-ramDeterministic": (None, "ale-py"),
    "Zaxxon-ramNoFrameskip": (None, "ale-py"),
    "FetchSlide": (None, "gym-robotics"),
    "FetchPickAndPlace": (None, "gym-robotics"),
    "FetchReach": (None, "gym-robotics"),
    "FetchPush": (None, "gym-robotics"),
    "HandReach": (None, "gym-robotics"),
    "HandManipulateBlockRotateZ": (None, "gym-robotics"),
    "HandManipulateBlockRotateZTouchSensors": (None, "gym-robotics"),
    "HandManipulateBlockRotateZTouchSensors": (None, "gym-robotics"),
    "HandManipulateBlockRotateParallel": (None, "gym-robotics"),
    "HandManipulateBlockRotateParallelTouchSensors": (None, "gym-robotics"),
    "HandManipulateBlockRotateParallelTouchSensors": (None, "gym-robotics"),
    "HandManipulateBlockRotateXYZ": (None, "gym-robotics"),
    "HandManipulateBlockRotateXYZTouchSensors": (None, "gym-robotics"),
    "HandManipulateBlockRotateXYZTouchSensors": (None, "gym-robotics"),
    "HandManipulateBlockFull": (None, "gym-robotics"),
    "HandManipulateBlock": (None, "gym-robotics"),
    "HandManipulateBlockTouchSensors": (None, "gym-robotics"),
    "HandManipulateEggRotate": (None, "gym-robotics"),
    "HandManipulateEggRotateTouchSensors": (None, "gym-robotics"),
    "HandManipulateEggFull": (None, "gym-robotics"),
    "HandManipulateEgg": (None, "gym-robotics"),
    "HandManipulateEggTouchSensors": (None, "gym-robotics"),
    "HandManipulatePenRotate": (None, "gym-robotics"),
    "HandManipulatePenRotateTouchSensors": (None, "gym-robotics"),
    "HandManipulatePenFull": (None, "gym-robotics"),
    "HandManipulatePen": (None, "gym-robotics"),
    "HandManipulatePenTouchSensors": (None, "gym-robotics"),
    "FetchSlideDense": (None, "gym-robotics"),
    "FetchPickAndPlaceDense": (None, "gym-robotics"),
    "FetchReachDense": (None, "gym-robotics"),
    "FetchPushDense": (None, "gym-robotics"),
    "HandReachDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateZDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateZTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateZTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateParallelDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateParallelTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateParallelTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateXYZDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateXYZTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateBlockRotateXYZTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateBlockFullDense": (None, "gym-robotics"),
    "HandManipulateBlockDense": (None, "gym-robotics"),
    "HandManipulateBlockTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateEggRotateDense": (None, "gym-robotics"),
    "HandManipulateEggRotateTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulateEggFullDense": (None, "gym-robotics"),
    "HandManipulateEggDense": (None, "gym-robotics"),
    "HandManipulateEggTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulatePenRotateDense": (None, "gym-robotics"),
    "HandManipulatePenRotateTouchSensorsDense": (None, "gym-robotics"),
    "HandManipulatePenFullDense": (None, "gym-robotics"),
    "HandManipulatePenDense": (None, "gym-robotics"),
    "HandManipulatePenTouchSensorsDense": (None, "gym-robotics"),
}
