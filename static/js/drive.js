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
            document.getElementById("start_street").value = drive.start_street;
            document.getElementById("start_house_number").value = drive.start_house_number;
            document.getElementById("start_postal_code").value = drive.start_postal_code;
            document.getElementById("start_place").value = drive.start_place;
            
            document.getElementById("end_street").value = drive.end_street;
            document.getElementById("end_house_number").value = drive.end_house_number;
            document.getElementById("end_postal_code").value = drive.end_postal_code;
            document.getElementById("end_place").value = drive.end_place;
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
            start_street: document.getElementById("start_street").value,
            start_house_number: document.getElementById("start_house_number").value,
            start_postal_code: document.getElementById("start_postal_code").value,
            start_place: document.getElementById("start_place").value,
            end_street: document.getElementById("end_street").value,
            end_house_number: document.getElementById("end_house_number").value,
            end_postal_code: document.getElementById("end_postal_code").value,
            end_place: document.getElementById("end_place").value,
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
