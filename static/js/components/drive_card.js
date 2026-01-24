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