/**
 * Keyboard Layout WebSocket Client
 * Handles real-time communication with the keyboard companion server
 */

const imageFolder = "/assets/";

class KeyboardLayoutClient {
  constructor() {
    this.websocket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.maxReconnectDelay = 30000;
    this.isConnecting = false;

    this.elements = {
      layoutImage: document.getElementById("layoutImage"),
      connectionStatus: document.getElementById("connectionStatus"),
      statusIndicator: document.getElementById("statusIndicator"),
      statusText: document.getElementById("statusText"),
      layoutContainer: document.getElementById("layoutContainer"),
      fullscreenButton: document.getElementById("fullscreenButton"),
    };

    this.init();
  }

  init() {
    this.connect();
    this.setupEventListeners();
    this.setupFullscreen();
  }

  connect() {
    if (
      this.isConnecting ||
      (this.websocket && this.websocket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.isConnecting = true;
    this.updateConnectionStatus("connecting", "Connecting...");

    try {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const wsUrl = `${protocol}//${window.location.host}/ws`;

      console.log(`Connecting to WebSocket: ${wsUrl}`);
      this.websocket = new WebSocket(wsUrl);

      this.websocket.onopen = this.onOpen.bind(this);
      this.websocket.onmessage = this.onMessage.bind(this);
      this.websocket.onclose = this.onClose.bind(this);
      this.websocket.onerror = this.onError.bind(this);
    } catch (error) {
      console.error("Failed to create WebSocket connection:", error);
      this.isConnecting = false;
      this.scheduleReconnect();
    }
  }

  onOpen() {
    console.log("WebSocket connection established");
    this.isConnecting = false;
    this.reconnectAttempts = 0;
    this.reconnectDelay = 1000;
    this.updateConnectionStatus("connected", "Connected");
  }

  onMessage(event) {
    try {
      const message = JSON.parse(event.data);
      if (message.all_layers) {
        return this.initializeImages(message.all_layers);
      }
      this.handleLayerUpdate(message);
    } catch (error) {
      console.error("Failed to parse WebSocket message:", error);
    }
  }

  initializeImages(layers) {
    for (const layer of layers) {
      if (layer.trim() === "") continue; // Skip empty layer names
      var img = new Image();
      img.src = `${imageFolder}${layer}`;
    }
    this.elements.layoutImage.src = `${imageFolder}${layers[0]}`;
  }

  onClose(event) {
    console.log("WebSocket connection closed:", event.code, event.reason);
    this.isConnecting = false;
    this.websocket = null;

    if (event.code !== 1000) {
      // Not a normal closure
      this.updateConnectionStatus("disconnected", "Disconnected");
      this.scheduleReconnect();
    }
  }

  onError(event) {
    console.error("WebSocket error:", event);
    this.isConnecting = false;
    this.updateConnectionStatus("disconnected", "Connection Error");
  }

  handleLayerUpdate(message) {
    const { layer, image } = message;
    console.log(`Layer changed to: ${layer}, Image: ${image}`);
    this.elements.layoutImage.src = `${imageFolder}${image}`;
  }

  updateConnectionStatus(status, text) {
    const indicator = this.elements.statusIndicator;
    const statusText = this.elements.statusText;

    indicator.classList.remove("connected", "disconnected", "connecting");
    indicator.classList.add(status);
    statusText.textContent = text;

    console.log(`Connection status: ${status} - ${text}`);
  }

  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log("Max reconnection attempts reached");
      this.updateConnectionStatus("disconnected", "Connection Failed");
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(
      this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1),
      this.maxReconnectDelay,
    );

    console.log(
      `Scheduling reconnection attempt ${this.reconnectAttempts} in ${delay}ms`,
    );
    this.updateConnectionStatus(
      "disconnected",
      `Reconnecting in ${Math.ceil(delay / 1000)}s...`,
    );

    setTimeout(() => {
      if (!this.websocket || this.websocket.readyState === WebSocket.CLOSED) {
        this.connect();
      }
    }, delay);
  }

  setupEventListeners() {
    document.addEventListener("visibilitychange", () => {
      if (
        !document.hidden &&
        (!this.websocket || this.websocket.readyState === WebSocket.CLOSED)
      ) {
        console.log("Page became visible, attempting to reconnect");
        this.connect();
      }
    });

    window.addEventListener("focus", () => {
      if (!this.websocket || this.websocket.readyState === WebSocket.CLOSED) {
        console.log("Window focused, attempting to reconnect");
        this.connect();
      }
    });

    window.addEventListener("beforeunload", () => {
      if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
        this.websocket.close(1000, "Page unloading");
      }
    });
  }

  reconnect() {
    if (this.websocket) {
      this.websocket.close();
    }
    this.reconnectAttempts = 0;
    this.connect();
  }

  getConnectionState() {
    if (!this.websocket) return "disconnected";

    switch (this.websocket.readyState) {
      case WebSocket.CONNECTING:
        return "connecting";
      case WebSocket.OPEN:
        return "connected";
      case WebSocket.CLOSING:
        return "disconnecting";
      case WebSocket.CLOSED:
        return "disconnected";
      default:
        return "unknown";
    }
  }

  setupFullscreen() {
    if (!this.elements.fullscreenButton) {
      console.warn("Fullscreen button not found");
      return;
    }

    this.elements.fullscreenButton.addEventListener("click", () => {
      this.toggleFullscreen();
    });

    document.addEventListener("fullscreenchange", () => {
      this.handleFullscreenChange();
    });

    document.addEventListener("webkitfullscreenchange", () => {
      this.handleFullscreenChange();
    });

    document.addEventListener("mozfullscreenchange", () => {
      this.handleFullscreenChange();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && this.isFullscreen()) {
        this.exitFullscreen();
      }
    });
  }

  toggleFullscreen() {
    if (this.isFullscreen()) {
      this.exitFullscreen();
    } else {
      this.enterFullscreen();
    }
  }

  enterFullscreen() {
    const container = this.elements.layoutContainer;

    try {
      if (container.requestFullscreen) {
        container.requestFullscreen();
      } else if (container.webkitRequestFullscreen) {
        container.webkitRequestFullscreen();
      } else if (container.mozRequestFullScreen) {
        container.mozRequestFullScreen();
      } else if (container.msRequestFullscreen) {
        container.msRequestFullscreen();
      } else {
        this.enterCSSFullscreen();
      }
    } catch (error) {
      console.warn("Fullscreen API not supported, using CSS fallback");
      this.enterCSSFullscreen();
    }
  }

  exitFullscreen() {
    try {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen();
      } else {
        this.exitCSSFullscreen();
      }
    } catch (error) {
      console.warn("Error exiting fullscreen, using CSS fallback");
      this.exitCSSFullscreen();
    }
  }

  enterCSSFullscreen() {
    document.body.classList.add("fullscreen-mode");
    this.updateFullscreenButton(true);
  }

  exitCSSFullscreen() {
    document.body.classList.remove("fullscreen-mode");
    this.updateFullscreenButton(false);
  }

  isFullscreen() {
    return !!(
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.mozFullScreenElement ||
      document.msFullscreenElement ||
      document.body.classList.contains("fullscreen-mode")
    );
  }

  handleFullscreenChange() {
    const isFullscreen = this.isFullscreen();
    this.updateFullscreenButton(isFullscreen);

    if (isFullscreen) {
      console.log("Entered fullscreen mode");
    } else {
      console.log("Exited fullscreen mode");
      document.body.classList.remove("fullscreen-mode");
    }
  }

  updateFullscreenButton(isFullscreen) {
    const button = this.elements.fullscreenButton;
    const icon = button.querySelector(".fullscreen-icon");

    if (isFullscreen) {
      button.title = "Exit fullscreen";
      icon.innerHTML =
        '<path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/>';
    } else {
      button.title = "Enter fullscreen";
      icon.innerHTML =
        '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>';
    }
  }
}

class App {
  constructor() {
    this.client = null;
    this.init();
  }

  init() {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => {
        this.start();
      });
    } else {
      this.start();
    }
  }

  start() {
    this.client = new KeyboardLayoutClient();
    this.setupGlobalEventHandlers();
  }

  setupGlobalEventHandlers() {
    window.addEventListener("keydown", (event) => {
      // Press 'R' to manually reconnect (for debugging)
      if (event.key === "r" && event.ctrlKey) {
        event.preventDefault();
        console.log("Manual reconnection triggered");
        if (this.client) {
          this.client.reconnect();
        }
      }
    });
  }
}

const app = new App();
