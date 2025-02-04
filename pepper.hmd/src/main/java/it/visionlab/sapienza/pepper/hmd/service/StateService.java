package it.visionlab.sapienza.pepper.hmd.service;

import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.model.types.Graph;
import it.visionlab.sapienza.pepper.hmd.model.types.PathWithWeight;
import it.visionlab.sapienza.pepper.hmd.repository.StateRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Service
public class StateService {

    // StateRepository is used to interact with the MongoDB repository for state operations.
    private final StateRepository stateRepository;

    // Constructor-based dependency injection of StateRepository. Initializes 'stateRepository'.
    @Autowired
    public StateService(StateRepository stateRepository) {
        this.stateRepository = stateRepository;
    }

    // Retrieves the current state from the repository.
    public State getState() {
        return stateRepository.getState();
    }

    // Retrieves the 'hmdOpen' flag value from the repository.
    public Boolean getHmdOpen() {
        return stateRepository.getHmdOpen();
    }

    // Retrieves the 'pepperAction' flag value from the repository.
    public Boolean getPepperAction() {
        return stateRepository.getPepperAction();
    }

    // Get the graph of the map.
    public Graph getGraph() {
        return stateRepository.getGraph();
    }

    // Get if a location is searchable.
    public boolean getIsKnownLocation(String location) {
        return stateRepository.getIsKnownLocation(location);
    }

    // Get the best path in the graph
    public List<PathWithWeight> getGraphBestPath(String start, String end) {
        return stateRepository.getGraphBestPath(start, end);
    }

    // Saves or updates the provided State object in the repository.
    public void setState(State state) {
        stateRepository.setState(state);
    }

    // Activates a feature (Pepper or HMD) based on the 'who' parameter.
    public void activate(String who) {
        stateRepository.activate(who);
    }

    // Deactivates a feature (Pepper or HMD) based on the 'who' parameter.
    public void deactivate(String who) {
        stateRepository.deactivate(who);
    }

    // Updates the 'stateName' field of the state in the repository to the provided 'stateName'.
    public void nextState(String stateName) {
        stateRepository.nextState(stateName);
    }

    // Sets the 'currentUser' field of the state in the repository to the provided User object.
    public void setCurrentUser(User user) {
        stateRepository.setCurrentUser(user);
    }

    // Updates the HMD open status based on the 'opened' value.
    public void hmdOpened(boolean opened) {
        stateRepository.hmdOpened(opened);
    }

    // Switch the value of the 'pepperAction' flag.
    public void switchFlagPepperAction(boolean pepperAction) {
        stateRepository.switchFlagPepperAction(pepperAction);
    }

    // Set the location target in the state
    public void setLocationTAG(String location) {
        stateRepository.setLocationTAG(location);
    }

    // Set the VR flag in the state
    public void setVr(boolean vrFlag) {
        stateRepository.setVr(vrFlag);
    }

    // Set the canTalk flag to true if the user can talk, false otherwise
    public void setCanTalk(Boolean canTalk) {
        stateRepository.setCanTalk(canTalk);
    }
}
