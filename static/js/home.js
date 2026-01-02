async function getmydrives() {
    try {
        const response = await fetch('/api/all_drives');
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
        const paragraph = document.createElement('p');
        paragraph.innerHTML = `
            <div id="drives-list" class="text-sm font-bold leading-tight tracking-tight text-gray-900 dark:text-white border border-gray-300 dark:border-gray-600 rounded p-3">
            <h2>Fahrt nach ${drive.destination} am ${drive.date} um ${drive.time} Uhr von ${drive.startpoint}</h2>
            <p>Veranstalter: ${drive.organizer}</p>
            <p>Plaetze: ${drive.seat_amount}</p>
            <p>Preis: ${drive.price} Euro</p>
            <p>Link: <a href="/drive/${drive.id_drive}">Details</a></p>
            </div>
        `;
        drivesList.appendChild(paragraph);
    });
})