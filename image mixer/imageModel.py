## This is the abstract class that the students should implement

from modesEnum import Modes
import numpy as np
import cv2 as cv


class ImageModel():

    def __init__(self, imgPath: str):
        self.imgPath = imgPath

        self.imgByte =cv.imread(imgPath, 0)
        self.dft = np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)

    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float,mode: 'Modes') -> np.ndarray:
        if mode==Modes.magnitudeAndPhase:

            magnitude1 = (magnitudeOrRealRatio) * (self.magnitude) + (
                    (1-magnitudeOrRealRatio)  * (imageToBeMixed.magnitude))
            phase1 = ((phaesOrImaginaryRatio) * (imageToBeMixed.phase)) + (
                    (1-phaesOrImaginaryRatio)  * (self.phase))

            vec = np.vectorize(complex)
            total = (magnitude1) * (np.exp(vec(0, phase1)))

        elif mode==Modes.realAndImaginary:
             Real1 = (magnitudeOrRealRatio) * (self.real) + (
                (1-magnitudeOrRealRatio) * (imageToBeMixed.real))
             imaginary1 = ((phaesOrImaginaryRatio) * (imageToBeMixed.imaginary)) + (
                (1-phaesOrImaginaryRatio) * (self.imaginary))

             vec = np.vectorize(complex)
             total = (Real1) + vec(0, imaginary1)

        elif mode==Modes.magnitudeAndunitPhase:
            magnitude = (magnitudeOrRealRatio) * (self.magnitude) + (
                    (1-magnitudeOrRealRatio)  * (imageToBeMixed.magnitude))


            uphase = np.zeros(self.imgByte.shape)

            vec = np.vectorize(complex)
            total = (magnitude) * (np.exp(vec(0, uphase)))

        elif mode == Modes.unitmagnitudeAndPhase:
            umagnitude = np.ones(self.imgByte.shape)

            phase = (phaesOrImaginaryRatio) * (imageToBeMixed.phase) + (
                    (1-phaesOrImaginaryRatio) * (self.phase))

            vec = np.vectorize(complex)
            total = (umagnitude) * (np.exp(vec(0, phase)))

        else:
            u_mag = np.ones(self.imgByte.shape)
            u_phase = np.zeros(self.imgByte.shape)

            vec = np.vectorize(complex)
            total = (u_mag) * (np.exp(vec(0, u_phase)))

        inf = np.fft.ifft2(total)

        plot = np.real(inf)
        return (plot)


