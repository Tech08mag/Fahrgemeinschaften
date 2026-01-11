document.addEventListener("DOMContentLoaded", async () => {
    // Fetch and populate the form
    async function getdrive() {
        try {
            const response = await fetch('/api/drive/' + DRIVE_ID);
            if (!response.ok) throw new Error('Failed to fetch drive data');

            const drive = await response.json();
            console.log('Drive Data:', drive);

            document.getElementById("date").value = drive.date;
            document.getElementById("time").value = drive.time;
            document.getElementById("startpoint").value = drive.startpoint;
            document.getElementById("destination").value = drive.destination;
            document.getElementById("seats").value = drive.seat_amount;
            document.getElementById("price").value = drive.price;

            return drive;

        } catch (error) {
            console.error(error);
            alert("Fehler beim Laden der Fahrt.");
        }
    }

    await getdrive();

    // Handle form submission
    document.getElementById("drive-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        

        const updatedDrive = {
            date: document.getElementById("date").value,
            time: document.getElementById("time").value,
            startpoint: document.getElementById("startpoint").value,
            destination: document.getElementById("destination").value,
            seats: document.getElementById("seats").value,
            price: document.getElementById("price").value
        };

        try {
            const res = await fetch(`/api/drive/${DRIVE_ID}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(updatedDrive)
            });

            if (res.ok) {
                alert("Fahrt erfolgreich aktualisiert!");
            } else {
                throw new Error("Update fehlgeschlagen");
            }
        } catch (error) {
            console.error(error);
            alert("Fehler beim Aktualisieren der Fahrt.");
        }
    });
});
