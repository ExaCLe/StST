<template>
  <UContainer class="home">
    <section class="welcome-section">
      <UCard class="welcome-card" elevated>
        <h1>Willkommen auf der ST-Umfragen Plattform!</h1>
        <p>Starten Sie mit unseren Umfragen oder verwalten Sie Inhalte, wenn Sie Zugriff als Administrator haben.</p>
        <UButton to="/surveys" color="primary" size="large" class="survey-button p-5" elevated>
          Zu den Umfragen
        </UButton>
      </UCard>
    </section>
    
    <section class="admin-section">
      <h2>Admin-Zugang</h2>
      <p>Nur für Administratoren: Bitte melden Sie sich mit den richtigen Zugangsdaten an, um auf diese Funktionen zuzugreifen.</p>
      <UDivider color="secondary" class="divider" />
      <div class="admin-links">
        <UCard class="admin-card">
          <UButton to="/admin/RequestResults" color="info" size="small">
            Ergebnisse Anfordern
          </UButton>
        </UCard>
        <UCard class="admin-card">
          <UButton to="/admin/UploadSurvey" color="warning" size="small">
            Umfrage Hochladen
          </UButton>
        </UCard>
      </div>
    </section>
  </UContainer>
</template>

<script setup>
// No additional setup required for this static page
</script>

<style scoped>
:root {
  --theme-color: #4a90e2; /* Set your primary theme color */
}

.home {
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.welcome-section {
  text-align: center;
  margin-bottom: 2rem;
}

.welcome-card {
  padding: 2rem;
  background-color: #e0f7fa;
  color: #004d40;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.welcome-card h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--theme-color);
}

.welcome-card p {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #00796b;
}

.survey-button {
  padding: 1.5rem 3rem !important; /* Extra padding for emphasis */
}

.admin-section {
  text-align: center;
  padding: 2rem;
  background-color: #fafafa;
  border-top: 3px solid var(--theme-color);
  border-radius: 10px;
  margin-top: 2rem;
}

.admin-section h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: var(--theme-color);
}

.admin-section p {
  font-size: 1rem;
  color: #333; /* Darker color for improved readability */
  margin-bottom: 1rem;
}

.divider {
  margin: 1.5rem 0;
}

.admin-links {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1rem;
}

.admin-card {
  padding: 0.5rem 1rem; /* Smaller padding for compact design */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f3f3f3;
}

.u-button[color="info"],
.u-button[color="warning"] {
  font-size: 0.9rem !important; /* Smaller font for compact admin buttons */
  padding: 0.5rem 1rem !important; /* Compact padding */
  color: #ffffff !important;
}
</style>
