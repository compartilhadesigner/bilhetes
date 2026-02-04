// #target photoshop
// #include "reader.jsx"
// #include "utils.jsx"

if (!app.documents.length) {
    alert("Abra o PSD antes de rodar o script.");
    throw new Error("Nenhum documento aberto");
}

var doc = app.activeDocument;

// pasta externa screenshots
var scriptFolder = new File($.fileName).parent;
var screenshotsFolder = new Folder(scriptFolder.parent + "/screenshots");

if (!screenshotsFolder.exists) {
    alert("Pasta screenshots não encontrada.");
    throw new Error("screenshots ausente");
}

var data = readDataFile("dados.txt");

for (var i = 0; i < data.length; i++) {
    var item = data[i];

    // 1. pasta do customer
    var customerGroup = findLayerSet(doc, item.customer);
    if (!customerGroup) continue;

    // 2. TEXTO
    var textoGroup = findLayerSet(customerGroup, "TEXTO");
    if (textoGroup) {
        var retorno = findTextLayer(textoGroup, "RETORNO");
        if (retorno) retorno.textItem.contents = String(item.profit);

        var valor = findTextLayer(textoGroup, "VALOR");
        if (valor) valor.textItem.contents = String(item.betAmount);

        var pin = findTextLayer(textoGroup, "PIN");
        if (pin) pin.textItem.contents = String(item.code);
    }

    // 3. BILHETE
    var bilheteGroup = findLayerSet(customerGroup, "BILHETE");
    if (bilheteGroup) {
        var imgFile = new File(screenshotsFolder + "/" + item.print);
        replaceImageInGroup(bilheteGroup, imgFile);
    }
}

alert("Processo finalizado.");
