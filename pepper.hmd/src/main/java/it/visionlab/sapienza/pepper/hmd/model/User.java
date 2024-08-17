package it.visionlab.sapienza.pepper.hmd.model;


import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDate;

@Setter
@Getter
@ToString
@Document(collection = "user")
public class User {

    // Unique identifier for the user document, annotated with @Id to indicate it is the primary key in MongoDB.
    @Id
    private String name;

    // The date when the user was last seen. This helps in tracking user activity.
    private LocalDate lastSeen;

    // Flag indicating whether the user has seen the tutorial or not.
    private Boolean tutorialSeen;

    // Constructor to initialize a User object with all fields.
    public User(String name, LocalDate lastSeen, Boolean tutorialSeen) {
        this.name = name;
        this.lastSeen = lastSeen;
        this.tutorialSeen = tutorialSeen;
    }
}
