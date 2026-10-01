# Integration

1. Create a separate UEFN XL Archipelago Island project named FNSoT.
2. Copy both Verse files into its Content/Verse folder and compile Verse.
3. Place a voyage_manager instance, three Button devices, a HUD Message device and a Score Manager device. Assign the editable references. Place AcceptVoyage and SellTreasure at the outpost; place DigTreasure on a separate island. Give the buttons clear interaction labels. Set the Score Manager to Add, enabled for all players, with unlimited activations. Gold currently uses session score, not persistent currency.
4. Place sloop_controller and assign one movable creative_prop hull with deck collision. Disable structural grid registration for the movable prop. Assign five Button devices and a HUD Message device. Controls currently operate from a stationary test station; they are not attached to the ship. The whole visible ship must be a single prop for this experiment. No ocean collision or obstacle avoidance is implemented.
5. Test movement first with one player, then two players standing and walking on the deck. If either slips, jitters or falls through, do not build additional systems on this movement method. Evaluate Scene Graph or a supported vehicle architecture instead.

# Runtime acceptance

## Current integration

Outpost XYZ is near (5665, 35032, 380) cm; recovery near (-35655, 34788, 380). Sloop starts offshore at (12000, 25000, 0). Controls remain on shore. Imported bow direction uses MeshForwardYawDegrees=-90; verify in a private session. Deck collision is a simple slab, without rails/cabin/cannon collision.

Source: Assets/Sloop/FNSOT_Sloop.blend and SM_FNSOT_Sloop.fbx. Native assets: /FNSoT/Verse/SM_FNSOT_Sloop and /FNSoT/CustomProps/Prop_SM_FNSOT_Sloop.

- Selling before digging awards nothing.
- Repeated accept cannot reset a voyage in progress.
- Digging twice cannot duplicate treasure.
- Selling twice awards exactly once.
- Two players have independent voyage states.
- Raising sail alone does not move an anchored ship.
- Raising anchor with sail up moves the prop; lowering sail stops it.
- Port/starboard commands change heading; anchoring stops movement within one movement step.
- Invalid hull/configuration does not enter a busy loop.
- Movement stays within MaxDistanceFromStart.

# Documentation used

- [Keyframed movement](https://dev.epicgames.com/documentation/fortnite/keyframed-movement-component-in-unreal-editor-for-fortnite)
- [Animating prop movement](https://dev.epicgames.com/documentation/fortnite/animating-prop-movement-in-verse)
- [Verse countdown device example](https://dev.epicgames.com/documentation/fortnite/making-a-custom-countdown-timer-using-verse)
- [Convert assets to Creative props](https://dev.epicgames.com/documentation/fortnite/converting-assets-into-props-in-unreal-editor-for-fortnite)

API signatures were also checked against the installed Epic Verse digests. None of these sources proves that a free-sailing crewed ship will behave correctly in multiplayer; that requires a session test.
