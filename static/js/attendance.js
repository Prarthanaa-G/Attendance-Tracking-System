

// Store attendance data persistently
const attendanceStatus = {}; // { name: { lastExit: timestamp, entranceTime: timestamp, id: rowId } }

async function fetchAttendance() {
    try {
        const response = await fetch('/attendance');
        const data = await response.json();

        const tableBody = document.querySelector("#attendanceTable tbody");

        data.forEach(record => {
            const utcTime = new Date(record.timestamp + ' UTC');  // Ensure it's in UTC
            const istOffset = 13 * 60 * 60 * 1000;  // IST is UTC +5:30
            const istTime = new Date(utcTime.getTime() + istOffset);  // Convert UTC to IST

            let attendance = "Present"; // Default to Present
            let attendanceColor = "green";

            if (record.name === "Unknown") {
                attendance = "NIL";
            } else if (attendanceStatus[record.name]) {
                const lastExitTime = new Date(attendanceStatus[record.name].lastExit);
                const timeDifference = (istTime - lastExitTime) / (1000 * 60); // Convert to minutes

                if (timeDifference < 30) {
                    // Mark as Absent, but DO NOT create a new entry
                    attendance = "Absent";
                    attendanceColor = "red";

                    // Update lastExit but keep entrance time unchanged
                    attendanceStatus[record.name].lastExit = istTime;

                    // Update the existing row instead of adding a new one
                    let existingRow = document.querySelector(`#attendanceTable tr[data-id="${attendanceStatus[record.name].id}"]`);
                    if (existingRow) {
                        existingRow.querySelector(".exitTime").textContent = formatTime(istTime);
                        existingRow.querySelector(".attendance").textContent = attendance;
                        existingRow.querySelector(".attendance").style.color = attendanceColor;
                    }

                    return; // Prevents adding a duplicate "Present" entry
                }
            }

            // If more than 30 minutes have passed OR it's the first entry
            if (!attendanceStatus[record.name] || timeDifference >= 30) {
                attendanceStatus[record.name] = {
                    id: record.id,
                    entranceTime: attendanceStatus[record.name]?.entranceTime || istTime, // Preserve entrance time if exists
                    lastExit: istTime,
                };

                // Find if a row already exists for this person
                let existingRow = document.querySelector(`#attendanceTable tr[data-id="${record.id}"]`);

                if (existingRow) {
                    // Update existing row
                    existingRow.querySelector(".exitTime").textContent = formatTime(istTime);
                    existingRow.querySelector(".attendance").textContent = attendance;
                    existingRow.querySelector(".attendance").style.color = attendanceColor;
                } else {
                    // Insert new row if it does not exist
                    const row = `<tr data-id="${record.id}">
                                    <td>${record.id}</td>
                                    <td>${record.name}</td>
                                    <td class="exitTime">${formatTime(istTime)}</td>
                                    <td class="entranceTime">${formatTime(attendanceStatus[record.name].entranceTime)}</td>
                                    <td class="attendance" style="color: ${attendanceColor};">${attendance}</td>
                                </tr>`;
                    tableBody.insertAdjacentHTML('afterend', row);
                }
            }
        });
    } catch (error) {
        console.error('Error fetching attendance data:', error);
    }
}

// Function to format time correctly
function formatTime(time) {
    return new Intl.DateTimeFormat('en-IN', {
        timeZone: 'Asia/Kolkata',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    }).format(time);
}

window.onload = fetchAttendance;

