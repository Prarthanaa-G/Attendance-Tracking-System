# Attendance Tracking System using Gait Recognition

### Overview

This project is a Flask-based web application that uses a gait recognition model to mark attendance. Users can upload a walking pattern file, and the system will predict the person's identity and record their attendance in an SQLite database.
Gait pattern recognition, combined with video analysis, offers a promising solution by enabling contactless and non-intrusive identification.

![attend_iden](https://github.com/user-attachments/assets/fea7e8a7-bd6d-4510-b8a9-992172759802)


### Features


-Upload gait data for recognition

-Predict the identity of the person based on their walking pattern

-Store attendance records in an SQLite database

-View attendance records via a web interface

-Marks absent for the student who exits the class within 30 minutes of entry

![image (2)](https://github.com/user-attachments/assets/c51fcccf-c31d-498a-9aa7-bcb2fc554e2d)

### Proposed architecture

![image](https://github.com/user-attachments/assets/509415a2-9069-4b2c-b9c5-9054ed0d2a21)


## Why Gait-Based Attendance Tracking is Better?


**Unique Identification**: Gait is unique to each individual, making it difficult to fake or duplicate (unlike cards or QR codes).

**Non-Invasive**: No physical contact is required, avoiding hygiene concerns and enhancing user convenience.

**Works in All Conditions**: Unlike face recognition, gait patterns are not affected by masks, facial obstructions, or poor lighting.

**Reduced Proxy Risk**s: Cannot be easily spoofed, as walking patterns are intrinsic to the individual.

**Cost-Effective**: Once trained, gait-based systems can leverage existing video surveillance infrastructure, reducing additional costs.

**Privacy-Friendly**: Gait-based systems do not require sensitive biometric data (like fingerprints or iris scans) to be stored.


## Where else can it be used other than Educational Institutions?


**Corporate Offices**: Organizations can integrate this system at office entry points to enhance security and streamline employee check-ins.

**Healthcare Facilities**: Hospitals and rehabilitation centers can use gait recognition to monitor and track patients and staff.

**High-Security Zones**: Military bases, government buildings, and research facilities can implement gait-based authentication for enhanced security access.

**Factories and Warehouses**: Ensures automated and hands-free attendance tracking in industrial environments where fingerprint scanning might not be feasible due to dirt or gloves.


