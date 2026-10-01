using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

voyage_stage := enum:
    Available
    Searching
    Returning

voyage_text<localizes>(Text:string):message = "{Text}"

# Session-only personal voyage. Physical cargo and crew sharing are later milestones.
voyage_manager := class(creative_device):
    @editable AcceptVoyage:button_device = button_device{}
    @editable DigTreasure:button_device = button_device{}
    @editable SellTreasure:button_device = button_device{}
    @editable Status:hud_message_device = hud_message_device{}
    @editable GoldAward:score_manager_device = score_manager_device{}
    @editable Reward:int = 250

    var Stages:[agent]voyage_stage = map{}

    OnBegin<override>()<suspends>:void =
        AcceptVoyage.InteractedWithEvent.Subscribe(Accept)
        DigTreasure.InteractedWithEvent.Subscribe(Dig)
        SellTreasure.InteractedWithEvent.Subscribe(Sell)

    StageFor(Agent:agent)<transacts>:voyage_stage =
        if (Stage := Stages[Agent]):
            return Stage
        return voyage_stage.Available

    Tell(Agent:agent, Text:string):void =
        Status.Show(Agent, voyage_text(Text), ?DisplayTime := 6.0)

    Accept(Agent:agent):void =
        if (StageFor(Agent) = voyage_stage.Available):
            if (set Stages[Agent] = voyage_stage.Searching):
                Tell(Agent, "Voyage accepted. Find the treasure station on the second island.")
        else:
            Tell(Agent, "Finish your current voyage first.")

    Dig(Agent:agent):void =
        if (StageFor(Agent) = voyage_stage.Searching):
            if (set Stages[Agent] = voyage_stage.Returning):
                Tell(Agent, "Treasure recovered. Return to the outpost merchant.")
        else:
            Tell(Agent, "Accept a voyage at the outpost before digging.")

    Sell(Agent:agent):void =
        if (StageFor(Agent) = voyage_stage.Returning):
            if (set Stages[Agent] = voyage_stage.Available):
                GoldAward.SetScoreAward(Reward)
                GoldAward.Activate(Agent)
                Tell(Agent, "Treasure sold for {Reward} gold. Another voyage awaits.")
        else:
            Tell(Agent, "Recover treasure before returning to the merchant.")
