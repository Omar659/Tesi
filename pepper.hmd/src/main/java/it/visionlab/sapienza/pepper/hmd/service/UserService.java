package it.visionlab.sapienza.pepper.hmd.service;

import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;

@Service
public class UserService {

    // UserRepository is used to interact with the MongoDB repository for user operations.
    private final UserRepository userRepository;

    // Constructor-based dependency injection of UserRepository. Initializes 'userRepository'.
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Retrieves a User object from the repository based on the provided 'name'.
    public User getUser(String name) {
        return userRepository.getUser(name);
    }

    // Checks if a user exists in the repository based on the provided 'name'.
    public boolean getUserExist(String name) {
        return userRepository.getUserExist(name);
    }

    // Inserts a new User document into the repository.
    public void createUser(User user) {
        userRepository.createUser(user);
    }

    // Updates the 'lastSeen' field of the User document to one day ahead from the current date.
    public void updateUserLastSeen(String name) {
        userRepository.updateUserLastSeen(name);
    }

    // Updates the 'tutorialSeen' field of the User document to true, indicating that the tutorial has been seen.
    public void updateUserTutorialSeen(String name) {
        userRepository.updateUserTutorialSeen(name);
    }
}
