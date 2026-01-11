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
            <a href="/edit_drive/${drive.id}">
  <button class="inline-flex items-center gap-2 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white
         hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
         transition">
         bearbeiten
         </button></a>
        <a href="/delete_drive/${drive.id}" class="inline-flex items-center gap-2 rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white
         hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition"> löschen </button></a>
        `;
        drivesList.appendChild(li);
    });
})