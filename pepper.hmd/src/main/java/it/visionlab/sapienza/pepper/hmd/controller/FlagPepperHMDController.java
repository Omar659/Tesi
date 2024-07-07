package it.visionlab.sapienza.pepper.hmd.controller;


import it.visionlab.sapienza.pepper.hmd.model.State;
import it.visionlab.sapienza.pepper.hmd.service.FlagPepperHMDService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/flagPepperHMD")
public class FlagPepperHMDController {

    private final FlagPepperHMDService flagPepperHMDService;

    @Autowired
    public FlagPepperHMDController(FlagPepperHMDService flagPepperHMDService) {
        this.flagPepperHMDService = flagPepperHMDService;
    }

    @GetMapping("/getState")
    public State getState() {
        return flagPepperHMDService.getState();
    }

    @PostMapping("/setState")
    public void setState(@RequestBody State state) {
        flagPepperHMDService.setState(state);
    }

    @PutMapping("/activate")
    public void activate(@RequestParam(required = true) String who) {
        flagPepperHMDService.activate(who);
    }

    @PutMapping("/deactivate")
    public void deactivate(@RequestParam(required = true) String who) {
        flagPepperHMDService.deactivate(who);
    }

    @PutMapping("/nextState")
    public void nextState(@RequestParam(required = true) String stateName) {
        flagPepperHMDService.nextState(stateName);
    }

}
