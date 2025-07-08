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

        self.lastShotTime = None
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
        self.lastShotTime = None

    def update(self):
        currentTime = time.time()
        if self.lastUpdateTime is None:
            self.lastUpdateTime = currentTime
            return

        elapsed = currentTime - self.lastUpdateTime
        self.lastUpdateTime = currentTime
        self.lastShotTime = currentTime
        # Decay recoil timer
        self.recoilTimer -= self.recoilDecayRate * elapsed

        if self.recoilTimer < 0:
            self.recoilTimer = 0.0

    def shoot(self):
        currentTime = time.time()
        self.lastUpdateTime = currentTime
        if self.lastShotTime is None:
            self.lastShotTime = currentTime

        # Calculate time since last shot
        elapsed = currentTime - self.lastShotTime
        self.lastShotTime = currentTime

        # Apply recoil buildup based on real time
        self.recoilTimer += elapsed
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
        y_offset = progress * self.maxYOffset
        tilt_offset = progress * self.maxTiltOffset


        return recoil_angle, y_offset, tilt_offset, progress

