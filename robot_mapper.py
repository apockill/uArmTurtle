from time import sleep

from uf.wrapper.swift_api import SwiftAPI


class FakeSwift:
    """ For testing without a robot """
    def __init__(self, *args, **kwargs): pass
    def set_position(self, *args, **kwargs):pass
    def set_polar(self, *args, **kwargs): pass
    def get_position(self, *args, **kwargs):
        return [0, 0, 0]
    def set_position(self, *args, **kwargs): pass
    def send_cmd_sync(self, *args, **kwargs): return 'ok'
    def get_is_moving(self, *args, **kwargs): return False


class RobotMapper:
    BOUNDS = (150, -80, 225, 80)
    MOVE_SPEED = 1500
    LASER_SPEED = 150
    # 180 > 150

    def __init__(self, dev_port, z_height=180):
        self.draw_height = z_height
        self.current_map = None
        self.running = False

        # Set up robot
        print("Connecting to robot")
        self.swift = SwiftAPI(dev_port=dev_port)
        sleep(2)
        print("Done Connecting")
        self.reset()


    def draw_map(self, map):
        """ Resize map and prep for use, then start running"""

        map = map.fit_to(self.BOUNDS)

        self.current_map = map
        self.swift.set_position(150, 0, self.draw_height, speed=self.MOVE_SPEED, wait=True)

        for cur_pt, next_pt, pen_down in self.current_map:
            if not pen_down: continue
            self.draw_line(cur_pt, next_pt)

        self.reset()

    def draw_line(self, from_pt, to_pt):
        # Make sure it's a valid request
        if from_pt == to_pt: return

        LASER_CMD = "G1 X{} Y{} Z{} F{}"

        # Get into the correct position before drawing the linn
        cur_pos = self.swift.get_position()[:2]
        if cur_pos != from_pt:
            print("Moving to", from_pt, "from", cur_pos)
            self.swift.set_position(x=from_pt[0], y=from_pt[1], z=self.draw_height, speed=self.MOVE_SPEED, wait=True)

        # Actually draw the line
        print("Drawing Line: ", from_pt, to_pt)
        to_pt = [int(round(to_pt[0])), int(round(to_pt[1]))]
        cmd = LASER_CMD.format(to_pt[0], to_pt[1], self.draw_height, self.LASER_SPEED)
        assert self.swift.send_cmd_sync(cmd) == "ok", "Unable to send robot to using laser command!"

        # Set the position normally, to turn off the laser
        self.swift.set_position(x=to_pt[0], y=to_pt[1], z=self.draw_height, speed=self.MOVE_SPEED, wait=True)


    def stop(self):
        self.running = False
        self.reset()

    def reset(self):
        """ Put the swift in a resting position """
        self.swift.set_polar(s=112, r=90, h=67, speed=self.MOVE_SPEED, wait=True)