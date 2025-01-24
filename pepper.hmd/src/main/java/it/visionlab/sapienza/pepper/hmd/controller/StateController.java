package it.visionlab.sapienza.pepper.hmd.controller;


import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.model.types.Graph;
import it.visionlab.sapienza.pepper.hmd.model.types.PathWithWeight;
import it.visionlab.sapienza.pepper.hmd.service.StateService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/state")
public class StateController {

    // The service class that this controller will use to perform operations related to state management.
    private final StateService stateService;

    // Constructor-based dependency injection of the StateService. The 'stateService' is initialized here.
    @Autowired
    public StateController(StateService stateService) {
        this.stateService = stateService;
    }

    // Handles HTTP GET requests to "/state/getState". Returns the current state from the database.
    @GetMapping("/getState")
    public State getState() {
        return stateService.getState();
    }

    // Handles HTTP GET requests to "/state/getHmdOpen". Returns whether the HMD is currently open.
    @GetMapping("/getHmdOpen")
    public Boolean getHmdOpen() {
        return stateService.getHmdOpen();
    }

    // Handles HTTP GET requests to "/state/getPepperAction". Returns whether the pepper is doing an action.
    @GetMapping("/getPepperAction")
    public Boolean getPepperAction() {
        return stateService.getPepperAction();
    }

    // Handles HTTP GET requests to "/state/getGraph". Get the graph of the map.
    @GetMapping("/getGraph")
    public Graph getGraph() {
        return stateService.getGraph();
    }

    // Handles HTTP GET requests to "/state/getGraphBestPath". Get the best path from point to point in the graph of the map.
    @GetMapping("/getGraphBestPath")
    public List<PathWithWeight> getGraphBestPath(@RequestParam(required = true) String start, @RequestParam(required = true) String end) {
        return stateService.getGraphBestPath(start, end);
    }

    // Handles HTTP GET requests to "/state/getIsKnownLocation". Get if a location is searchable.
    @GetMapping("/getIsKnownLocation")
    public boolean getIsKnownLocation(@RequestParam(required = true) String location) {
        return stateService.getIsKnownLocation(location);
    }

    // Handles HTTP POST requests to "/state/setState". Accepts a State object in the request body and set the state.
    @PostMapping("/setState")
    public void setState(@RequestBody State state) {
        stateService.setState(state);
    }

    // Handles HTTP PUT requests to "/state/activate". Activates a pepper or the HMD based on the 'who' parameter.
    @PutMapping("/activate")
    public void activate(@RequestParam(required = true) String who) {
        stateService.activate(who);
    }

    // Handles HTTP PUT requests to "/state/deactivate". Deactivates a pepper or the HMD based on the 'who' parameter.
    @PutMapping("/deactivate")
    public void deactivate(@RequestParam(required = true) String who) {
        stateService.deactivate(who);
    }

    // Handles HTTP PUT requests to "/state/nextState". Transitions to the next state specified by the 'stateName' parameter.
    @PutMapping("/nextState")
    public void nextState(@RequestParam(required = true) String stateName) {
        stateService.nextState(stateName);
    }

    // Handles HTTP PUT requests to "/state/setCurrentUser". Accepts a User object in the request body and sets it as the current user.
    @PutMapping("/setCurrentUser")
    public void setCurrentUser(@RequestBody(required = true) User user) {
        stateService.setCurrentUser(user);
    }

    // Handles HTTP PUT requests to "/state/setHmdOpen". Updates the HMD open status based on 'opened' value.
    @PutMapping("/hmdOpened")
    public void hmdOpened(@RequestParam(required = true) boolean opened) {
        stateService.hmdOpened(opened);
    }

    // Handles HTTP PUT requests to "/state/switchFlagPepperAction". Switch the value of the 'pepperAction' flag.
    @PutMapping("/switchFlagPepperAction")
    public void switchFlagPepperAction(@RequestParam(required = true) boolean pepperAction) {
        stateService.switchFlagPepperAction(pepperAction);
    }

    // Handles HTTP PUT requests to "/state/setLocationTAG". Set the location TAG in the state
    @PutMapping("/setLocationTAG")
    public void setLocationTAG(@RequestParam(required = true) String location) {
        stateService.setLocationTAG(location);
    }

    // Handles HTTP PUT requests to "/state/setVr". Set the VR flag in the state
    @PutMapping("/setVr")
    public void setVr(@RequestParam(required = true) boolean vrFlag) {
        stateService.setVr(vrFlag);
    }

}
