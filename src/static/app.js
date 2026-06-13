document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
        const participantsList = details.participants
          .map(participant => `
            <li>
              <span class="participant-email">${participant}</span>
              <button class="remove-participant" data-activity="${name}" data-email="${participant}" aria-label="Remove participant">✕</button>
            </li>`)
          .join("");

        activityCard.innerHTML = `
          <div class="activity-header">
            <h4>${details.name}</h4>
            <button class="toggle-details" aria-expanded="true" aria-label="Toggle details">▾</button>
          </div>
          <div class="activity-details">
            <p>${details.description}</p>
            <p><strong>Schedule:</strong> ${details.schedule}</p>
            <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
            <div class="participants-section">
              <strong>Signed Up (${details.participants.length}):</strong>
              <ul class="participants-list">
                ${participantsList}
              </ul>
            </div>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = details.name;
        activitySelect.appendChild(option);
      });
      
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        // Refresh activities list to show the new participant
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Delegate click for remove participant buttons and toggle (register once)
  activitiesList.addEventListener('click', async (event) => {
    const btn = event.target.closest('.remove-participant');
    if (btn) {
      const activityId = btn.getAttribute('data-activity');
      const email = btn.getAttribute('data-email');

      if (!activityId || !email) return;

      if (!confirm(`Unregister ${email} from this activity?`)) return;

      try {
        const res = await fetch(`/activities/${encodeURIComponent(activityId)}/signup?email=${encodeURIComponent(email)}`, { method: 'DELETE' });
        const result = await res.json();
        if (res.ok) {
          // Refresh activities list to reflect removal
          fetchActivities();
        } else {
          alert(result.detail || 'Failed to remove participant');
        }
      } catch (err) {
        console.error('Error removing participant:', err);
        alert('Error removing participant');
      }
      return;
    }

    // Toggle details (collapse/expand)
    const toggle = event.target.closest('.toggle-details');
    if (toggle) {
      const card = toggle.closest('.activity-card');
      if (!card) return;
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      toggle.textContent = expanded ? '▸' : '▾';
      card.classList.toggle('collapsed', expanded);
    }
  });

  // Initialize app
  fetchActivities();
});
