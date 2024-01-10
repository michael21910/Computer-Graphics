class Rect:
    def __init__(self, player, x=0, y=0, w=1, h=1):
        self.center = [x, y]
        self.width = w
        self.height = h
        self.player = player

    def checkCollWithPlayer(self, playerPos, playerWidth):
        return self.center[0] + 1.5 + playerWidth > playerPos.x > self.center[0] - 1.5 - playerWidth and \
                self.center[2] + 1.5 + playerWidth > playerPos.z > self.center[2] - 1.5 - playerWidth

    def handleCollisionWithPlayer(self, player):
        norm = self.player.camera.cam_pos - Vec3(temp[0], 0, temp[1])
        if abs(norm.x) > abs(norm.z):
            if norm.x > 0:
                norm = Vec3(1, 0, 0)
            else:
                norm = Vec3(-1, 0, 0)
        else:
            if norm.z > 0:
                norm = Vec3(0, 0, 1)
            else:
                norm = Vec3(0, 0, -1)

        temp = norm ** dir
        self.player.camera.cam_pos -= dir * self.player.currentSpeed
        self.player.camera.cam_pos += (temp ** norm).normalize() * self.player.currentSpeed

        if self.player.left and not self.player.right:
            if center[0] + 1.5 + r > player.x > center[0] - 1.5 - r and center[2] + 1.5 + r > player.z > center[
                2] - 1.5 - r:
                self.player.camera.cam_pos += (norm + ((temp ** norm) - dir)).normalize() * self.player.currentSpeed

        elif not self.player.left and self.player.right:
            if center[0] + 1.5 + r > player.x > center[0] - 1.5 - r and center[2] + 1.5 + r > player.z > center[
                2] - 1.5 - r:
                self.player.camera.cam_pos += (norm + ((temp ** norm) - dir)).normalize() * self.player.currentSpeed