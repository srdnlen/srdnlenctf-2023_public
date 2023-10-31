// WebAssembly loading function
async function loadWebAssembly() {
  imports = {
    env: asmLibraryArg,
    wasi_snapshot_preview1: asmLibraryArg,
  };

  const wasmModule = new WebAssembly.Module(
    await fetch("/static/js/wasm.wasm").then((response) =>
      response.arrayBuffer(),
    ),
  );

  await WebAssembly.instantiate(wasmModule, imports);
}

// Switch tab function
async function switchTab() {
  if (window.location.hash != "") {
    await loadWebAssembly();

    // Shared memory;
    Module.writeAsciiToMemory(
      decodeURIComponent(document.baseURI.split("#")[1]),
      Module._tabID,
    );

    var value = Module.ccall("sanitize_value", "string", [], []);

    window.location.hash = value;

    // Removed old
    $(".tab").removeClass("u-tab-active");
    $(".tab-button").removeClass("active");

    // Update
    var button = $("a[href*='" + value + "']");
    button.addClass("active");

    var table = $("div[id*='" + value + "']");
    table.addClass("u-tab-active");

    return false;
  }
}

$(document).ready(() => {
  $(".tab-button").click(function() {
    var tabID = $(this).data("tab");

    window.location.hash = tabID;
  });

  $(window).on("hashchange", function() {
    switchTab();
  });

  // Since the event is only triggered when the hash changes, we need to trigger
  // the event now, to handle the hash the page may have loaded with.
  $(window).trigger("hashchange");
});
