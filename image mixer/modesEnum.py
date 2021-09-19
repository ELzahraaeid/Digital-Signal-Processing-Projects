## enum for different operation modes

import enum

class Modes(enum.Enum):
    magnitudeAndPhase = "testMagAndPhaseMode"
    realAndImaginary = "testRealAndImagMode"
    unitmagnitudeAndPhase = "testUnitMagAndPhaseMode"
    magnitudeAndunitPhase ="testMagAndUnitPhaseMode"
    unitmagnitudeAndunitPhase ="testUnitMagAndUnitPhaseMode"

