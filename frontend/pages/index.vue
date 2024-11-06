<template>
  <div class="min-h-screen bg-white overflow-hidden">
    <div class="container mx-auto px-4 py-16 relative">
      <!-- Decorative blobs -->
      <div class="absolute top-0 left-0 w-64 h-64 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
      <div class="absolute top-0 right-0 w-64 h-64 bg-yellow-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-20 w-64 h-64 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>

      <div class="relative">
        <div class="text-center mb-16">
          <h1 class="text-5xl font-extrabold text-gray-900 mb-4">
            Willkommen bei St-Surveys
          </h1>
          <p class="text-xl text-gray-600 mb-8">
            Entdecken Sie unsere Umfragen und tragen Sie zu wertvoller Forschung bei!
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <NuxtLink to="/surveys" class="group">
            <div class="bg-gradient-to-br from-purple-400 to-indigo-600 rounded-xl p-8 text-white transition-all duration-300 transform hover:scale-105 hover:shadow-lg">
              <UIcon name="i-heroicons-clipboard-document" class="w-12 h-12 mb-4" />
              <h2 class="text-2xl font-bold mb-2">Verfügbare Umfragen</h2>
              <p class="mb-4">Entdecken und nehmen Sie an unseren neuesten Umfragen teil</p>
              <span class="inline-flex items-center text-sm font-medium">
                Umfragen anzeigen
                <span class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform">→</span>
              </span>
            </div>
          </NuxtLink>

          <div class="bg-gradient-to-br from-pink-400 to-red-600 rounded-xl p-8 text-white">
            <UIcon name="i-heroicons-lock-closed" class="w-12 h-12 mb-4" />
            <h2 class="text-2xl font-bold mb-2">Admin-Bereich</h2>
            <p class="mb-4">Geschützter Bereich für Umfrageverwaltung</p>
            <div class="space-y-2">
              <NuxtLink to="/admin/UploadSurvey" class="block group">
                <span class="inline-flex items-center text-sm font-medium">
                  Umfrage hochladen
                  <span class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform">→</span>
                </span>
              </NuxtLink>
              <NuxtLink to="/admin/RequestResults" class="block group">
                <span class="inline-flex items-center text-sm font-medium">
                  Ergebnisse abrufen
                  <span class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform">→</span>
                </span>
              </NuxtLink>
            </div>
            <p class="mt-4 text-xs text-white text-opacity-80">
              Hinweis: Admin-Passwort erforderlich für den Zugriff
            </p>
          </div>
        </div>

        <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div class="text-center">
            <div class="bg-yellow-100 rounded-full p-4 inline-block mb-4">
              <UIcon name="i-heroicons-users" class="w-8 h-8 text-yellow-600" />
            </div>
            <h3 class="text-xl font-semibold mb-2">Benutzerfreundlich</h3>
            <p class="text-gray-600">Einfach zu bedienende Oberfläche für alle Teilnehmer</p>
          </div>
          <div class="text-center">
            <div class="bg-green-100 rounded-full p-4 inline-block mb-4">
              <UIcon name="i-heroicons-chart-bar" class="w-8 h-8 text-green-600" />
            </div>
            <h3 class="text-xl font-semibold mb-2">Aufschlussreiche Analysen</h3>
            <p class="text-gray-600">Umfassende Datenanalyse und Berichterstattung</p>
          </div>
          <div class="text-center">
            <div class="bg-blue-100 rounded-full p-4 inline-block mb-4">
              <UIcon name="i-heroicons-shield-check" class="w-8 h-8 text-blue-600" />
            </div>
            <h3 class="text-xl font-semibold mb-2">Sicher & Privat</h3>
            <p class="text-gray-600">Ihre Daten sind geschützt und vertraulich</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
</style>

<script setup>
</script>
