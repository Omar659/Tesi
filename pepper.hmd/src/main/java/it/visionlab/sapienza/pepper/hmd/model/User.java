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
    @Id
    private String name;
    private LocalDate lastSeen;
    private Boolean tutorialSeen;

    public User(String name, LocalDate lastSeen, Boolean tutorialSeen) {
        this.name = name;
        this.lastSeen = lastSeen;
        this.tutorialSeen = tutorialSeen;
    }
}
