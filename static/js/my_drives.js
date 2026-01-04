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
            <h2>Fahrt nach ${drive.destination} am ${drive.date} um ${drive.time} Uhr von ${drive.startpoint}</h2>
            <p>Veranstalter: ${drive.organizer}</p>
            <p>Plätze: ${drive.seat_amount}</p>
            <p>Preis: ${drive.price} Euro</p>
        `;
        drivesList.appendChild(li);
    });
})