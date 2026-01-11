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
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
  <div class="p-6 space-y-2">
    <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
      Fahrt von 
      <span class="font-medium text-gray-700 dark:text-gray-300">${drive.startpoint}</span>
      nach 
      <span class="font-medium text-gray-700 dark:text-gray-300">${drive.destination}</span>
      am 
      <span class="font-medium text-gray-700 dark:text-gray-300">${drive.date}</span>
      um 
      <span class="font-medium text-gray-700 dark:text-gray-300">${drive.time}</span> Uhr
    </h2>

    <p class="text-gray-600 dark:text-gray-400">
      Veranstalter: 
      <span class="font-medium text-gray-800 dark:text-gray-200">${drive.organizer}</span>
    </p>

    <p class="text-gray-600 dark:text-gray-400">
      Plätze: 
      <span class="font-medium text-gray-800 dark:text-gray-200">${drive.seat_amount}</span>
    </p>

    <p class="text-gray-600 dark:text-gray-400">
      Preis: 
      <span class="font-medium text-gray-800 dark:text-gray-200">${drive.price} €</span>
    </p>

    <div class="mt-4">
      <button
        onclick="addPassenger(${drive.id_drive})"
        class="inline-block text-xs text-white bg-green-600 rounded-md px-3 py-1.5 border border-green-600 hover:bg-green-700 hover:border-green-700 transition"
      >
        Mitfahren
      </button>
    </div>
  </div>
</div>

        `;
        drivesList.appendChild(paragraph);
    });
})

async function addPassenger(driveId) {
    try {
        const response = await fetch(`/api/drive/passenger/${driveId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert('Du wurdest als Passagier hinzugefügt!');
        } else {
            alert('Du bist bereits als Passagier eingetragen.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}