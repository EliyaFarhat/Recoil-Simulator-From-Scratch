import time


class WeaponRecoil:
    def __init__(self, timeToReachMaxRecoil, firstShotError, maxRecoilAngle, maxYOffset, recoilDecayRate, maxTiltOffset):
        """
        recoilDecayRate: how fast recoil timer decays per second (units/sec)
        """
        self.timeToReachMaxRecoil = timeToReachMaxRecoil
        self.maxRecoilAngle = maxRecoilAngle
        self.firstShotError = firstShotError
        self.maxYOffset = maxYOffset
        self.recoilDecayRate = recoilDecayRate
        self.maxTiltOffset = maxTiltOffset

        self.recoilTimer = 0.0
        self.lastUpdateTime = None

    def GetProgress(self):
        return self.recoilTimer / self.timeToReachMaxRecoil

    def ChangeWeapon(self, details):
        self.timeToReachMaxRecoil = details["timeToReachMaxRecoil"]
        self.maxRecoilAngle = details["maxRecoilAngle"]
        self.firstShotError = details["firstShotError"]
        self.maxYOffset = details["maxYOffset"]
        self.recoilDecayRate = details["recoilDecayRate"]
        self.maxTiltOffset = details["maxTiltOffset"]

        self.recoilTimer = 0.0
        self.lastUpdateTime = None

    def update(self):
        currentTime = time.time()
        if self.lastUpdateTime is None:
            self.lastUpdateTime = currentTime
            return

        elapsed = currentTime - self.lastUpdateTime
        self.lastUpdateTime = currentTime

        # Decay recoil timer
        self.recoilTimer -= self.recoilDecayRate * elapsed
        if self.recoilTimer < 0:
            self.recoilTimer = 0.0

    def shoot(self):
        if self.recoilTimer == 0:
            recoil_angle = self.firstShotError
            y_offset = 0.0
            tilt_offset = 0.0
            self.recoilTimer += self.timeToReachMaxRecoil / 10
            return recoil_angle, y_offset, tilt_offset, 0

        # Add recoil buildup
        self.recoilTimer += self.timeToReachMaxRecoil / 10
        if self.recoilTimer > self.timeToReachMaxRecoil:
            self.recoilTimer = self.timeToReachMaxRecoil

        progress = self.recoilTimer / self.timeToReachMaxRecoil

        # Custom easing: flat until threshold, then ramps up hard
        threshold = 0.3
        exponent = 3.5

        if progress <= threshold:
            eased_progress = 0.0
        else:
            eased_progress = ((progress - threshold) / (1 - threshold)) ** exponent

        recoil_angle = self.firstShotError + eased_progress * (self.maxRecoilAngle - self.firstShotError)

        # Keep offsets linear
        y_offset = progress * self.maxYOffset
        tilt_offset = progress * self.maxTiltOffset

        print(f"angle={recoil_angle:.2f}  progress={progress:.2f}")
        return recoil_angle, y_offset, tilt_offset, progress

