"""Headless checks for projectile_simulator.py (run: python test_projectile.py)."""
import math
import matplotlib

matplotlib.use("Agg")

import projectile_simulator as ps

# 1) Same case as the spreadsheet: 20 m/s, 45 deg, y0 = 0
assert math.isclose(ps.projectile_range(20, 45, 0), 40.8163265, rel_tol=1e-6)
assert math.isclose(ps.max_height(20, 45, 0), 10.2040816, rel_tol=1e-6)
assert math.isclose(ps.flight_time(20, 45, 0), 2.88615013, rel_tol=1e-6)

# 2) The projectile really is on the ground at the end of the flight
for angle, speed, height in [(45, 20, 0), (30, 15, 10), (0, 10, 20), (90, 12, 5), (60, 50, 50)]:
    T = ps.flight_time(speed, angle, height)
    x, y = ps.position(T, speed, angle, height)
    assert abs(y) < 1e-9, (angle, speed, height, y)
    assert math.isclose(x, ps.projectile_range(speed, angle, height), rel_tol=1e-9)

# 3) Horizontal launch from 20 m at 10 m/s: t = sqrt(2h/g)
T = ps.flight_time(10, 0, 20)
assert math.isclose(T, math.sqrt(2 * 20 / ps.G), rel_tol=1e-9)
assert ps.max_height(10, 0, 20) == 20

# 4) Max height matches the largest y along a fine sampling
import numpy as np
ts = np.linspace(0, ps.flight_time(25, 60, 8), 20001)
_, ys = ps.position(ts, 25, 60, 8)
assert math.isclose(ys.max(), ps.max_height(25, 60, 8), rel_tol=1e-6)

# 5) Edge case: angle 0 and height 0 -> nothing moves, must not crash
assert ps.projectile_range(10, 0, 0) == 0

# 6) Build the interface, move sliders, run a launch to the end, save a picture
sim = ps.Simulator()
sim.s_angle.set_val(35)
sim.s_speed.set_val(25)
sim.s_height.set_val(10)
sim._launch(None)
for _ in range(60):
    sim._tick(None)
sim.fig.savefig("/home/claude/preview_midflight.png", dpi=80)
for _ in range(400):
    sim._tick(None)
assert not sim.running
sim.fig.savefig("/home/claude/preview_landed.png", dpi=80)
sim._reset(None)
assert sim.s_angle.val == 45 and sim.s_speed.val == 20 and sim.s_height.val == 0
sim.s_angle.set_val(0)
sim.s_height.set_val(0)  # degenerate case through the UI
print("ALL CHECKS PASSED")