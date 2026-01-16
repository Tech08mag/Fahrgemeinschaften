async function getmydrives() {
  try {
    const response = await fetch('/api/user/passenger/');

    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    return [];
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
        mitfahren
      </button>
      <button
  onclick="removePassenger(${drive.id_drive})"
  class="inline-block text-xs text-white bg-red-600 rounded-md px-3 py-1.5 border border-red-600 hover:bg-red-700 hover:border-red-700 transition">
        nicht mitfahren
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
    const response = await fetch(`/api/passenger/${driveId}`, {
      method: 'PUT'
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.error || 'Fehler beim Hinzufügen');
      return;
    }

    alert('Du wurdest als Passagier hinzugefügt!');
    location.reload();

  } catch (error) {
    console.error('Error:', error);
  }
}


async function removePassenger(driveId) {
  try {
    const response = await fetch(`/api/passenger/${driveId}`, {
      method: 'DELETE'
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.error || 'Du bist kein Passagier dieser Fahrt.');
      return;
    }

    alert('Du wurdest als Passagier entfernt!');
    location.reload();

  } catch (error) {
    console.error('Error:', error);
  }
}
