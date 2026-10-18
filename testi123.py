from vex import *

brain = Brain()

# First lift motor
lift_motor1 = Motor(
    Ports.PORT6,
    GearSetting.RATIO_18_1,
    False
)

# Second lift motor
# Change PORT9 to the real port.
lift_motor2 = Motor(
    Ports.PORT8,
    GearSetting.RATIO_18_1,
    True
)

brain.screen.clear_screen()
brain.screen.print("Nyt alkaa sit vittu tapahtumaan. Hakeudu suojaan")
brain.screen.new_line()
brain.screen.print("Nyt alkaa tapahtumaan. Viiden sekunnin kuluessa voi tapahtua mitä vain...")
wait(5, SECONDS)
# Test at moderate power first.
lift_motor1.spin(REVERSE, 20, PERCENT)
lift_motor2.spin(REVERSE, 20, PERCENT)

wait(2, SECONDS)
brain.screen.clear_screen()
lift_motor1.stop(HOLD)
lift_motor2.stop(HOLD)

brain.screen.clear_screen()
brain.screen.new_line
brain.screen.print("Testi valmis, selvisitkö?")
brain.screen.new_line()
brain.screen.print("Joo vituttaa pelkkä ajatus tästä robotista.")


while True:
    wait(100, MSEC)
