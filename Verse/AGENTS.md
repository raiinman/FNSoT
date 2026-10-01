# Purpose
Verse gameplay source for the FNSoT pirate adventure.

# Ownership
Owns voyage state, rewards, ship controls, damage and repair simulation.

# Local Contracts
- Copy source into the FNSoT Content/Verse folder before compiling.
- Use /UnrealEngine.com/Temporary/SpatialMath for creative_prop transforms (XYZ centimeters).
- Never report a prototype as playable until device wiring, compilation and a Fortnite session are verified.
- Runtime state is session-only until persistence is implemented and tested.

# Work Guidance
- Prefer editable references with explicit setup instructions.
- Keep one movement task per ship and validate props before accessing them.

# Verification
- Epic Verse language server via uefn_verse_check; a clean analysis does not replace an editor build.

# Child DOX Index
None.
