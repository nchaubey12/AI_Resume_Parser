const API = "http://127.0.0.1:5000";

/* =======================
   UPLOAD RESUME
======================= */
function uploadResume() {
    const fileInput = document.getElementById("resumeFile");

    if (!fileInput.files.length) {
        alert("Please select a PDF resume");
        return;
    }

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    fetch(API + "/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(res => {
        if (res.error) {
            alert(res.error);
            return;
        }
        fileInput.value = "";
        loadTable();
    })
    .catch(err => {
        console.error(err);
        alert("Upload failed");
    });
}

/* =======================
   LOAD TABLE DATA
======================= */
function loadTable() {
    fetch(API + "/data")
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#resumeTable tbody");
            tbody.innerHTML = "";

            if (!data.length) return;

            data.forEach(d => {
                if (!d.email) return; // safety guard

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${d.name || ""}</td>
                    <td>${d.email || ""}</td>
                    <td>${d.phone || ""}</td>
                    <td>${d.location || ""}</td>
                    <td>${(d.hard_skills || []).join(", ")}</td>
                    <td>${(d.soft_skills || []).join(", ")}</td>
                    <td>${(d.experience || []).join(", ")}</td>
                    <td>${d.linkedin ? `<a href="${formatLink(d.linkedin)}" target="_blank">Link</a>` : ""}</td>
                    <td>${d.github ? `<a href="${formatLink(d.github)}" target="_blank">Link</a>` : ""}</td>
                    <td>
                        <a href="${API}/resume/${d.resume_file}" target="_blank">
                            PDF
                        </a>
                    </td>
                    <td>
                        <button class="delete-btn" onclick="deleteRow('${d.email}')">
                            Delete
                        </button>
                    </td>
                `;

                tbody.appendChild(row);
            });
        });
}

/* =======================
   DELETE ENTRY
======================= */
function deleteRow(email) {
    if (!email) return;

    if (!confirm("Are you sure you want to delete this entry?")) return;

    fetch(API + "/delete/" + encodeURIComponent(email), {
        method: "DELETE"
    })
    .then(() => loadTable());
}

/* =======================
   UTILS
======================= */
function formatLink(link) {
    if (link.startsWith("http")) return link;
    return "https://" + link;
}

/* =======================
   INITIAL LOAD
======================= */
loadTable();
