package it.visionlab.sapienza.pepper.hmd.controller;

import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@RestController
@RequestMapping("/user")
public class UserController {

    // The service class that this controller will use to perform operations related to user management.
    private final UserService userService;

    // Constructor-based dependency injection of the UserService. The 'userService' is initialized here.
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // Handles HTTP GET requests to "/user/getUser". Retrieves a User object based on the provided 'name' parameter.
    @GetMapping("/getUser")
    public User getUser(@RequestParam(required = true) String name) {
        return userService.getUser(name);
    }

    // Handles HTTP GET requests to "/user/getUserExist". Checks if a user exists based on the provided 'name' parameter.
    @GetMapping("/getUserExist")
    public boolean getUserExist(@RequestParam(required = true) String name) {
        return userService.getUserExist(name);
    }

    // Handles HTTP PUT requests to "/user/putLastSeen". Updates the last seen timestamp for the user identified by the 'name' parameter.
    @PutMapping("/putLastSeen")
    public void updateUserLastSeen(@RequestParam(required = true) String name) {
        userService.updateUserLastSeen(name);
    }

    // Handles HTTP PUT requests to "/user/putTutorialSeen". Updates the tutorialSeen flag to true of the user identified by the 'name' parameter.
    @PutMapping("/putTutorialSeen")
    public void updateUserTutorialSeen(@RequestParam(required = true) String name) {
        userService.updateUserTutorialSeen(name);
    }

    // Handles HTTP POST requests to "/user/postCreateUser". Creates a new user with the details provided in the request body.
    @PostMapping("/postCreateUser")
    public void createUser(@RequestBody User user) {
        userService.createUser(user);
    }
}
