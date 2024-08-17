package it.visionlab.sapienza.pepper.hmd.service;

import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;

@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUser(String name) {
        return userRepository.getUser(name);
    }

    public boolean getUserExist(String name) {
        return userRepository.getUserExist(name);
    }

    public void createUser(User user) {
        userRepository.createUser(user);
    }

    public void updateUserLastSeen(String name) {
        userRepository.updateUserLastSeen(name);
    }

    public void updateUserTutorialSeen(String name) {
        userRepository.updateUserTutorialSeen(name);
    }
}
