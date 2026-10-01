using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }

# Kinematic movement experiment. Requires deck collision and multiplayer playtest.
sloop_controller := class(creative_device):
    @editable Hull:creative_prop = creative_prop{}
    @editable RaiseSail:button_device = button_device{}
    @editable LowerSail:button_device = button_device{}
    @editable Port:button_device = button_device{}
    @editable Starboard:button_device = button_device{}
    @editable Anchor:button_device = button_device{}
    @editable Status:hud_message_device = hud_message_device{}
    @editable Speed:float = 600.0
    @editable TurnDegrees:float = 10.0
    # Imported FBX bow points along local -Y, rather than Unreal's +X.
    @editable MeshForwardYawDegrees:float = -90.0
    @editable TickSeconds:float = 0.1
    @editable MaxDistanceFromStart:float = 70000.0

    var Sail:float = 0.0
    var Anchored:logic = true
    var Heading:float = 0.0

    OnBegin<override>()<suspends>:void =
        RaiseSail.InteractedWithEvent.Subscribe(Raise)
        LowerSail.InteractedWithEvent.Subscribe(Lower)
        Port.InteractedWithEvent.Subscribe(TurnPort)
        Starboard.InteractedWithEvent.Subscribe(TurnStarboard)
        Anchor.InteractedWithEvent.Subscribe(ToggleAnchor)
        if (Hull.IsValid[], TickSeconds > 0.0, Speed >= 0.0, MaxDistanceFromStart > 0.0):
            Start := Hull.GetTransform()
            Angles := Start.Rotation.GetYawPitchRollDegrees()
            if (Yaw := Angles[0]):
                set Heading = Yaw
            loop:
                if (not Hull.IsValid[]):
                    break
                if (Anchored = false, Sail > 0.0):
                    Rotation := MakeRotationFromYawPitchRollDegrees(Heading, 0.0, 0.0)
                    Current := Hull.GetTransform()
                    Direction := MakeRotationFromYawPitchRollDegrees(Heading + MeshForwardYawDegrees, 0.0, 0.0)
                    Target := Current.Translation + Direction.GetLocalForward() * Speed * Sail * TickSeconds
                    if (Distance(Target, Start.Translation) <= MaxDistanceFromStart):
                        Hull.MoveTo(Target, Rotation, TickSeconds)
                    else:
                        set Anchored = true
                        Sleep(TickSeconds)
                else:
                    Sleep(TickSeconds)

    Raise(Agent:agent):void =
        set Sail = 1.0
        Status.Show(Agent, voyage_text("Sail raised. Raise anchor to get underway."), ?DisplayTime := 3.0)

    Lower(Agent:agent):void =
        set Sail = 0.0
        Status.Show(Agent, voyage_text("Sail lowered."), ?DisplayTime := 3.0)

    TurnPort(Agent:agent):void =
        set Heading -= TurnDegrees

    TurnStarboard(Agent:agent):void =
        set Heading += TurnDegrees

    ToggleAnchor(Agent:agent):void =
        if (Anchored = true):
            set Anchored = false
            Status.Show(Agent, voyage_text("Anchor raised."), ?DisplayTime := 3.0)
        else:
            set Anchored = true
            Status.Show(Agent, voyage_text("Anchor dropped."), ?DisplayTime := 3.0)
