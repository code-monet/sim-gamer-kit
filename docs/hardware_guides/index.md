# Hardware Guides

This guide captures known compatibility issues with controllers I have
myself verified, or that have been reported by users. Please contribute via
[GitHub Discussions](https://github.com/code-monet/sim-gamer-kit/discussions)!

## Thrustmaster

### Thrustmaster TMX

This device is likely on "stable" software.

1.  Some effects can be missing in certain games because this wheel will
    reject FFB effects with parameters out of spec (usually axis rotation).
    Seen in Burnout Paradise.

Issue can be fixed either with `FFFSake` or `IndirectInput`.

## TurtleBeach

### TurtleBeach Velocity One Race

As of this writing, TurtleBeach has promised a new firmware with some fixes.
With system firmware version 1.4.0, any of the [described issues](../game_guides/issues.md)
can kick in for games not in their list of official supported games e.g.

1.  Crew Motorfest game crash
2.  Crew 2 FPS drop
3.  Incorrect FFB in most Need for Speed games.
4.  Inability to combine or zero pedals and analog paddles

The wheel is also detected as "not a wheel" (unclear if this bug
is on the vendor or Microsoft) by some games (there's *some* argument to
differentiate), and a subset of these games then use a different
FFB logic meant as a fallback (this doesn't make sense to me at all). Usually
this results in missing FFB (Need for Speed Most Wanted 2012, Bus Simulator 21).

Fixing issues usually requires `FFFSake` with the `Reducer` engine, and sometimes
also needs `IndirectInput`. Combined pedals can be achieved using Joystick Gremlin.
