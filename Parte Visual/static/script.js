document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  let savedTheme = null;
  try { savedTheme = localStorage.getItem("senas-theme"); } catch (_) {}
  const systemDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    document.querySelectorAll(".theme-toggle").forEach(button => {
      const dark = theme === "dark";
      button.textContent = dark ? "☀" : "☾";
      button.setAttribute("aria-label", dark ? "Cambiar a modo claro" : "Cambiar a modo oscuro");
      button.setAttribute("title", dark ? "Cambiar a modo claro" : "Cambiar a modo oscuro");
    });
  };
  applyTheme(savedTheme || "dark");
  document.querySelectorAll(".theme-toggle").forEach(button => button.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem("senas-theme", next); } catch (_) {}
  }));

  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  if (toggle && nav) toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  document.querySelectorAll(".main-nav a").forEach(a => a.addEventListener("click", () => {
    nav?.classList.remove("nav-open");
    toggle?.setAttribute("aria-expanded", "false");
  }));
  document.querySelectorAll(".show-password").forEach(btn => btn.addEventListener("click", () => {
    const input = btn.parentElement.querySelector("input");
    const reveal = input.type === "password";
    input.type = reveal ? "text" : "password";
    btn.textContent = reveal ? "Ocultar" : "Ver";
    btn.setAttribute("aria-label", reveal ? "Ocultar contraseña" : "Mostrar contraseña");
  }));
  const video = document.getElementById("camera-video");
  if (video) {
    let stream = null;
    const start = document.getElementById("start-camera");
    const stop = document.getElementById("stop-camera");
    const status = document.getElementById("camera-status");
    const placeholder = document.getElementById("camera-placeholder");
    const hint = document.getElementById("camera-hint");
    start.addEventListener("click", async () => {
      if (!navigator.mediaDevices?.getUserMedia) {
        hint.textContent = "Tu navegador no permite acceder a la cámara aquí. Probá con HTTPS o localhost.";
        return;
      }
      try {
        stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: "user"}, audio: false});
        video.srcObject = stream;
        placeholder.hidden = true;
        video.classList.add("video-active");
        status.textContent = "Cámara activa";
        hint.textContent = "Vista previa activa. La interpretación de señas aún no está conectada.";
        start.disabled = true; stop.disabled = false;
      } catch (e) {
        hint.textContent = e.name === "NotAllowedError" ? "No diste permiso para usar la cámara. Podés habilitarlo desde el navegador." : "No se pudo abrir la cámara. Verificá que esté conectada y no la use otra aplicación.";
      }
    });
    const stopCamera = () => {
      if (stream) stream.getTracks().forEach(track => track.stop());
      stream = null; video.srcObject = null; video.classList.remove("video-active");
      placeholder.hidden = false; status.textContent = "Cámara apagada";
      hint.textContent = "Tu navegador te pedirá permiso para usar la cámara.";
      start.disabled = false; stop.disabled = true;
    };
    stop.addEventListener("click", stopCamera);
    window.addEventListener("beforeunload", () => { if (stream) stream.getTracks().forEach(t => t.stop()); });
  }
  document.querySelectorAll(".flash").forEach(el => setTimeout(() => el.remove(), 6500));
});
