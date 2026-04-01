let drivesState = [];

// ---------------- API ----------------

async function getMyDrives() {
  try {
    const res = await fetch('/api/my_drives');
    if (!res.ok) throw new Error();
    return await res.json();
  } catch (e) {
    console.error(e);
    return [];
  }
}

async function getPassengers(id) {
  try {
    const res = await fetch(`/api/passenger/${id}`);
    if (!res.ok) throw new Error();
    const data = await res.json();
    return data.passengers || [];
  } catch (e) {
    console.error(e);
    return [];
  }
}

// ---------------- STATE UPDATE ----------------

function updateDriveInState(id, updater) {
  const index = drivesState.findIndex(d => d.id_drive == id);
  if (index === -1) return;

  drivesState[index] = updater(drivesState[index]);
  renderDrive(drivesState[index]);
}

// ---------------- ACTIONS ----------------

async function addPassenger(id) {
  updateDriveInState(id, drive => ({
    ...drive,
    passengers: [...drive.passengers, currentUser]
  }));

  try {
    await fetch(`/api/passenger/add/${id}`, { method: 'POST' });
  } catch (e) {
    console.error(e);
  }
}

async function removePassenger(id) {
  updateDriveInState(id, drive => ({
    ...drive,
    passengers: drive.passengers.filter(p => p !== currentUser)
  }));

  try {
    await fetch(`/api/passenger/remove/${id}`, { method: 'POST' });
  } catch (e) {
    console.error(e);
  }
}

async function deleteDrive(id) {
  if (!confirm('Wirklich löschen?')) return;

  // sofort aus UI entfernen
  drivesState = drivesState.filter(d => d.id_drive != id);
  document.querySelector(`[data-drive-id="${id}"]`)?.remove();

  try {
    await fetch(`/api/drive/delete/${id}`, { method: 'DELETE' });
  } catch (e) {
    console.error(e);
  }
}

// ---------------- EVENT HANDLING ----------------

document.addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;

  const id = btn.dataset.id;

  if (btn.classList.contains('btn-add')) addPassenger(id);
  if (btn.classList.contains('btn-remove')) removePassenger(id);
  if (btn.classList.contains('btn-delete')) deleteDrive(id);
});

// ---------------- RENDER ----------------

function renderDrive(drive) {
  const existing = document.querySelector(`[data-drive-id="${drive.id_drive}"]`);

  const passengers = drive.passengers;
  const isPassenger = passengers.includes(currentUser);
  const isOrganizer = currentUser === drive.organizer;
  const isFull = passengers.length >= drive.seat_amount;

  const addDisabled = isPassenger || isOrganizer || isFull;
  const removeDisabled = !isPassenger || isOrganizer;

  const passengersText = passengers.length
    ? passengers.join(', ')
    : 'Keine Mitfahrer';

  const html = `
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
      <div class="p-6 space-y-2">

        <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
          Fahrt von 
          ${drive.start_street} ${drive.start_house_number}, ${drive.start_postal_code} ${drive.start_place}
          nach 
          ${drive.end_street} ${drive.end_house_number}, ${drive.end_postal_code} ${drive.end_place}
          am ${drive.date} um ${drive.time} Uhr
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

        <p class="text-gray-600 dark:text-gray-400">
          Mitfahrer:
          <span class="font-medium text-gray-800 dark:text-gray-200">
            ${passengersText}
          </span>
        </p>

        <div class="mt-4 flex gap-2">

          <button 
            class="btn-add text-xs text-white px-3 py-1.5 rounded-md border transition
            ${addDisabled 
              ? 'bg-gray-400 border-gray-400 cursor-not-allowed' 
              : 'bg-green-600 border-green-600 hover:bg-green-700'}"
            data-id="${drive.id_drive}"
            ${addDisabled ? 'disabled' : ''}>
            Mitfahren
          </button>

          <button 
            class="btn-remove text-xs text-white px-3 py-1.5 rounded-md border transition
            ${removeDisabled 
              ? 'bg-gray-400 border-gray-400 cursor-not-allowed' 
              : 'bg-red-600 border-red-600 hover:bg-red-700'}"
            data-id="${drive.id_drive}"
            ${removeDisabled ? 'disabled' : ''}>
            Nicht mitfahren
          </button>

          <a href="/drive/${drive.id_drive}"
            class="inline-block text-xs text-white bg-blue-600 rounded-md px-3 py-1.5 border border-blue-600 hover:bg-blue-700 transition">
            Bearbeiten
          </a>

          <button 
            class="btn-delete text-xs text-white bg-red-600 rounded-md px-3 py-1.5 border border-red-600 hover:bg-red-700 transition"
            data-id="${drive.id_drive}">
            Löschen
          </button>

        </div>
      </div>
    </div>
  `;

  if (existing) {
    existing.innerHTML = html;
  } else {
    const li = document.createElement('li');
    li.dataset.driveId = drive.id_drive;
    li.innerHTML = html;
    document.getElementById('drives-list').appendChild(li);
  }
}

// ---------------- INIT ----------------

(async () => {
  const list = document.getElementById('drives-list');
  list.innerHTML = `<p class="text-gray-500 italic">Lade Fahrten...</p>`;

  const drives = await getMyDrives();

  if (!drives.length) {
    list.innerHTML = `<p class="text-gray-500 italic">Keine Fahrten vorhanden</p>`;
    return;
  }

  // ⚡ parallel laden
  drivesState = await Promise.all(
    drives.map(async d => ({
      ...d,
      passengers: await getPassengers(d.id_drive)
    }))
  );

  list.innerHTML = '';

  drivesState.forEach(renderDrive);
})();