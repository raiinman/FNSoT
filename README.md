# FNSoT

UEFN pirate adventure targeting cooperative sailing, island voyages, treasure recovery and naval combat. Uses original or appropriately licensed content. This is an early foundation, not a complete Sea of Thieves recreation.

## Source

- `Verse/voyage_manager.verse`: accept, recover, sell; per-agent session state and score reward.
- `Verse/sloop_controller.verse`: bounded kinematic ship movement experiment with sail, steering and anchor controls.
- [Setup](docs/SETUP.md)
- [Current status and acceptance milestones](docs/STATUS.md)

The native UEFN project is saved locally as FNSoT/FNSoT.uefnproject. This repository tracks authored Verse, original Blender/FBX ship assets, the generator, setup and build evidence. Native project checkpoints should use Epic revision control; a completed checkpoint is not yet verified. Do not commit derived caches, credentials or unrelated assets.

Regenerate the ship using Blender background mode and tools/build_sloop.py. Import the FBX and convert it to a Wood Creative prop; disable structural registration and damage, then assign Hull.
