// Fetch all drives
async function getMyDrives() {
  try {
    const response = await fetch('/api/user/passenger/');
    if (!response.ok) throw new Error('Failed to fetch drives');
    return await response.json();
  } catch (error) {
    console.error('Error fetching drives:', error);
    return [];
  }
}

// Fetch passengers for a specific drive
async function getPassengers(driveId) {
  try {
    const response = await fetch(`/api/passenger/${driveId}`);
    if (!response.ok) throw new Error('Failed to fetch passengers');
    const data = await response.json();
    return data.passengers || [];
  } catch (error) {
    console.error(`Error fetching passengers for drive ${driveId}:`, error);
    return [];
  }
}

// Render passengers HTML
function renderPassengers(passengers) {
  if (!passengers.length) {
    return `<p class="text-gray-500 dark:text-gray-500 italic">Keine Mitfahrer</p>`;
  }
  return passengers.map(p => `
    <p class="text-gray-600 dark:text-gray-400">
      Mitfahrer: 
      <span class="font-medium text-gray-800 dark:text-gray-200">${p}</span>
    </p>
  `).join('');
}

// Render a single drive card
function renderDriveCard(drive, passengers, currentUser) {
  const passengersHtml = renderPassengers(passengers);
  const seatsAvailable = drive.seat_amount - passengers.length;
  const isUserPassenger = passengers.includes(currentUser);

  // Determine if buttons should be disabled
  const addDisabled = isUserPassenger || seatsAvailable === 0;
  const removeDisabled = !isUserPassenger;

  return `
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 mb-4">
      <div class="p-6 space-y-2">
        <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
          Fahrt von 
          <span class="font-medium text-gray-700 dark:text-gray-300">${drive.start_street} ${drive.start_house_number}, ${drive.start_postal_code} ${drive.start_place}</span>
          nach 
          <span class="font-medium text-gray-700 dark:text-gray-300">${drive.end_street} ${drive.end_house_number}, ${drive.end_postal_code} ${drive.end_place}</span>
          am 
          <span class="font-medium text-gray-700 dark:text-gray-300">${drive.date}</span>
          um 
          <span class="font-medium text-gray-700 dark:text-gray-300">${drive.time}</span> Uhr
        </h2>

        <p class="text-gray-600 dark:text-gray-400">Veranstalter: <span class="font-medium text-gray-800 dark:text-gray-200">${drive.organizer}</span></p>
        <p class="text-gray-600 dark:text-gray-400">Plätze: <span class="font-medium text-gray-800 dark:text-gray-200">${drive.seat_amount}</span></p>
        <p class="text-gray-600 dark:text-gray-400">Preis: <span class="font-medium text-gray-800 dark:text-gray-200">${drive.price} €</span></p>
        ${passengersHtml}

        <div class="mt-4 space-x-2">
          <button 
            onclick="addPassenger(${drive.id_drive})" 
            class="inline-block text-xs text-white bg-green-600 rounded-md px-3 py-1.5 border border-green-600 hover:bg-green-700 hover:border-green-700 transition ${addDisabled ? 'opacity-50 cursor-not-allowed' : ''}"
            ${addDisabled ? 'disabled' : ''}>
            mitfahren
          </button>
          <button 
            onclick="removePassenger(${drive.id_drive})" 
            class="inline-block text-xs text-white bg-red-600 rounded-md px-3 py-1.5 border border-red-600 hover:bg-red-700 hover:border-red-700 transition ${removeDisabled ? 'opacity-50 cursor-not-allowed' : ''}"
            ${removeDisabled ? 'disabled' : ''}>
            nicht mitfahren
          </button>
        </div>
      </div>
    </div>
  `;
}

// Load drives and passengers in parallel
async function loadDrives() {
  const drivesList = document.getElementById('drives-list');
  drivesList.innerHTML = ''; // clear previous content

  const drives = await getMyDrives();

  // Fetch passengers for all drives in parallel
  const passengersArray = await Promise.all(drives.map(d => getPassengers(d.id_drive)));

  drives.forEach((drive, index) => {
    const passengers = passengersArray[index];
    drivesList.innerHTML += renderDriveCard(drive, passengers, currentUser);
  });
}

// Add a passenger
async function addPassenger(driveId) {
  try {
    const response = await fetch(`/api/passenger/${driveId}`, { method: 'PUT' });
    const data = await response.json();
    if (!response.ok) {
      alert(data.error || 'Fehler beim Hinzufügen');
      return;
    }
    alert('Du wurdest als Passagier hinzugefügt!');
    loadDrives(); // Refresh UI without reload
  } catch (error) {
    console.error('Error adding passenger:', error);
  }
}

// Remove a passenger
async function removePassenger(driveId) {
  try {
    const response = await fetch(`/api/passenger/${driveId}`, { method: 'DELETE' });
    const data = await response.json();
    if (!response.ok) {
      alert(data.error || 'Du bist kein Passagier dieser Fahrt.');
      return;
    }
    alert('Du wurdest als Passagier entfernt!');
    loadDrives(); // Refresh UI without reload
  } catch (error) {
    console.error('Error removing passenger:', error);
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadDrives);