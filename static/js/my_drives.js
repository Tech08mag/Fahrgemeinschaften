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

async function get_passengers(drive_id) {
    try {
        const response = await fetch(`/api/passenger/${drive_id}`);
        if (response.ok) {
            const data = await response.json();
            return data.passengers;
        } else {
            throw new Error('Failed to fetch passengers');
        }
    } catch (error) {
        console.error('Error:', error); 
    }
}

getmydrives().then(async (drives) => {
  const drivesList = document.getElementById('drives-list');

  for (const drive of drives) {
    const li = document.createElement('li');

    // fetch passengers (assumed async)
    const passengers = await get_passengers(drive.id_drive);

    // build passenger HTML
    const passengersHtml = passengers.length > 0
      ? passengers.map(passenger => `
          <p class="text-gray-600 dark:text-gray-400">
            Mitfahrer: 
            <span class="font-medium text-gray-800 dark:text-gray-200">
              ${passenger}
            </span>
          </p>
        `).join('')
      : `
        <p class="text-gray-500 dark:text-gray-500 italic">
          Keine Mitfahrer
        </p>
      `;

    li.innerHTML = `
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
        <div class="p-6 space-y-2">
          <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
            Fahrt von 
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.start_street}</span>
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.start_house_number}</span>
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.start_postal_code}</span>
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.start_place}</span>
            nach 
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.end_street}</span>
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.end_house_number}</span>
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.end_postal_code}</span>
            <span class="font-medium text-gray-700 dark:text-gray-300">${drive.end_place}</span>
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

          ${passengersHtml}

          <div class="mt-4 flex gap-2">
            <a href="/drive/${drive.id_drive}"
               class="inline-block text-xs text-white bg-blue-600 rounded-md px-3 py-1.5 border border-blue-600 hover:bg-blue-700 transition">
              Bearbeiten
            </a>

            <a href="/api/drive/delete/${drive.id_drive}"
               class="inline-block text-xs text-white bg-red-600 rounded-md px-3 py-1.5 border border-red-600 hover:bg-red-700 transition">
              Löschen
            </a>
          </div>
        </div>
      </div>
    `;

    drivesList.appendChild(li);
  }
});