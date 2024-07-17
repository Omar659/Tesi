package it.visionlab.sapienza.pepper.hmd.controller;

import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@RestController
@RequestMapping("/user")
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/getUser")
    public User getUser(@RequestParam(required = true) String name) {
        return userService.getUser(name);
    }

    @GetMapping("/getUserExist")
    public boolean getUserExist(@RequestParam(required = true) String name) {
        return userService.getUserExist(name);
    }

    @PostMapping("/postCreateUser")
    public void createUser(@RequestBody User user) {
        userService.createUser(user);
    }
}
