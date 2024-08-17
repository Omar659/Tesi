package it.visionlab.sapienza.pepper.hmd.model;


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
    @Id
    private String stateId;
    private Boolean flagPepper;
    private Boolean flagHMD;
    private String stateName;
    private String chosenPlace;
    private User currentUser;
    private Boolean hmdOpen;

    public State(String stateId, Boolean flagPepper, Boolean flagHMD, String stateName, String chosenPlace, User currentUser, Boolean hmdOpen) {
        this.stateId = stateId;
        this.flagPepper = flagPepper;
        this.flagHMD = flagHMD;
        this.stateName = stateName;
        this.chosenPlace = chosenPlace;
        this.currentUser = currentUser;
        this.hmdOpen = hmdOpen;
    }
}
