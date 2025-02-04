package it.visionlab.sapienza.pepper.hmd.model;


import it.visionlab.sapienza.pepper.hmd.model.types.Graph;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Setter
@Getter
@ToString
@Document(collection = "state")
public class State {

    // Unique identifier for the state document, annotated with @Id to indicate it is the primary key in MongoDB.
    @Id
    private String stateId;

    // Flag indicating whether the Pepper device is active or not.
    private Boolean flagPepper;

    // Flag indicating whether the HMD (Head-Mounted Display) is active or not.
    private Boolean flagHMD;

    // Name of the current state, used for descriptive purposes.
    private String stateName;

    // The name of the place currently chosen or relevant to the state. Can be null if no place is chosen.
    private String chosenPlace;

    // The current user associated with the state, if any. This can be null if no user is set.
    private User currentUser;

    // Flag indicating whether the HMD is currently open or closed.
    private Boolean hmdOpen;

    // Flag indicating whether pepper is able to do an action (used for coordinate pepper and hmd).
    private Boolean pepperAction;

    // Graph representing the building
    private Graph graph;

    // Flag to know if the user is in VR or MR mode
    private Boolean vr;

    // Used for inform user if he can talk in VR environment
    private Boolean canTalk;

    // Constructor to initialize a State object with all fields.
    public State(String stateId, Boolean flagPepper, Boolean flagHMD, String stateName, String chosenPlace, User currentUser, Boolean hmdOpen, Boolean pepperAction, Graph graph, Boolean vr, Boolean canTalk) {
        this.stateId = stateId;
        this.flagPepper = flagPepper;
        this.flagHMD = flagHMD;
        this.stateName = stateName;
        this.chosenPlace = chosenPlace;
        this.currentUser = currentUser;
        this.hmdOpen = hmdOpen;
        this.pepperAction = pepperAction;
        this.graph = graph;
        this.vr = vr;
        this.canTalk = canTalk;
    }
}
