package it.visionlab.sapienza.pepper.hmd.constants;

import it.visionlab.sapienza.pepper.hmd.model.User;
import it.visionlab.sapienza.pepper.hmd.model.types.Graph;

// This class defines a collection of constants used across the application.
// Constants are typically defined as 'public static final' to ensure that their values remain unchanged and are accessible throughout the application.

public class Constants {

    // The ID of the state, set to "104". This could be used to identify a particular state or condition in the application.
    public static final String stateId = "104";

    // A flag indicating whether the Pepper device is active or not. Set to true.
    public static final Boolean flagPepper = true;

    // A flag indicating whether the HMD (Head-Mounted Display) is active or not. Set to false.
    public static final Boolean flagHMD = false;

    // The name associated with the starting state. This is set to "start".
    public static final String stateName = "start";

    // This variable is intended to hold the name of a chosen place, but it is currently set to null, indicating no place is selected.
    public static final String chosenPlace = null;

    // This variable is intended to hold the information of the current user, but it is currently set to null, indicating no user is set.
    public static final User currentUser = null;

    // A flag indicating whether the HMD is currently open. Set to false.
    public static final Boolean hmdOpen = false;

    // The name associated with the HMD flag. This is set to "HMD".
    public static final String hmdFlagName = "HMD";

    // The name associated with the Pepper flag. This is set to "pepper".
    public static final String pepperFlagName = "pepper";

    // The name associated with the Pepper flag. This is set to "pepper".
    public static final boolean pepperAction = false;

    public static Graph mapGraph = null;
}
