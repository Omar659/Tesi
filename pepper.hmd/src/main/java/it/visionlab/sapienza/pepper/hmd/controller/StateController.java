package it.visionlab.sapienza.pepper.hmd.controller;


import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.service.StateService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/state")
public class StateController {

    private final StateService stateService;

    @Autowired
    public StateController(StateService stateService) {
        this.stateService = stateService;
    }

    @GetMapping("/getState")
    public State getState() {
        return stateService.getState();
    }

    @PostMapping("/setState")
    public void setState(@RequestBody State state) {
        stateService.setState(state);
    }

    @PutMapping("/activate")
    public void activate(@RequestParam(required = true) String who) {
        stateService.activate(who);
    }

    @PutMapping("/deactivate")
    public void deactivate(@RequestParam(required = true) String who) {
        stateService.deactivate(who);
    }

    @PutMapping("/nextState")
    public void nextState(@RequestParam(required = true) String stateName) {
        stateService.nextState(stateName);
    }

}
