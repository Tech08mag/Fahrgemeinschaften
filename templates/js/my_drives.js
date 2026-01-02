async function getmydrives() {
    try {
        const response = await fetch('/api/my_drives');
        if (response.ok) {
            const data = await response.json();
            window.myDrivesData = data;
            return data;
        } else {
            throw new Error('Failed to fetch data');
        }
    } catch (error) {
        console.error('Error:', error); 
    }
}

getmydrives()
.then((drives) => {
    const drivesList = document.getElementById('drives-list');
    drives.forEach(drive => {
        const li = document.createElement('li');
        li.innerHTML = `
            <h2>Drive to ${drive.destination} on ${drive.date} at ${drive.time}</h2>
            <p>Organizer: ${drive.organizer}</p>
            <p>Seats Available: ${drive.seats_available}</p>
        `;
        drivesList.appendChild(li);
    });
})